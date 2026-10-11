"""
Bounded thread-based producer/consumer job processor.

Teaching goals:
- fixed worker count
- bounded queue / backpressure
- thread-safe submit API
- per-job Future result/exception
- ordinary job failure isolation
- drain-and-stop shutdown

This is a learning example, not a production task queue. In particular,
lifecycle edge cases deserve additional tests before production use.
"""
from __future__ import annotations

import logging
import queue
import threading
import time
import uuid
from concurrent.futures import Future, TimeoutError
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(threadName)s: %(message)s",
)
log = logging.getLogger(__name__)


class State(Enum):
    NEW = auto()
    RUNNING = auto()
    CLOSING = auto()
    CLOSED = auto()


class ProcessorClosedError(RuntimeError):
    pass


@dataclass(frozen=True)
class Job:
    job_id: str
    fn: Callable[..., Any]
    args: tuple
    kwargs: dict


class JobProcessor:
    _STOP = object()

    def __init__(self, workers: int = 3, queue_size: int = 5):
        if workers < 1 or queue_size < 1:
            raise ValueError("workers and queue_size must be positive")

        self._queue: queue.Queue = queue.Queue(maxsize=queue_size)
        self._worker_count = workers
        self._threads: list[threading.Thread] = []
        self._condition = threading.Condition()
        self._state = State.NEW
        self._pending = 0
        self._active_submitters = 0
        self._succeeded = 0
        self._failed = 0
        self._cancelled = 0
        self._shutdown_started = False
        self._shutdown_done = threading.Event()

    def start(self) -> None:
        with self._condition:
            if self._state is not State.NEW:
                raise RuntimeError("start() may be called only once")
            self._state = State.RUNNING
            for index in range(self._worker_count):
                thread = threading.Thread(
                    target=self._worker,
                    name=f"worker-{index + 1}",
                    daemon=False,
                )
                self._threads.append(thread)
                thread.start()

    def submit(
        self,
        fn: Callable[..., Any],
        *args: Any,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> Future:
        """Wait up to timeout for queue capacity; return a Future if accepted."""
        future = Future()
        job = Job(str(uuid.uuid4()), fn, args, kwargs)
        deadline = None if timeout is None else time.monotonic() + timeout

        # Reserve pending work while admission is allowed. Never hold the
        # lifecycle lock while blocking on queue.put().
        with self._condition:
            if self._state is not State.RUNNING:
                raise ProcessorClosedError("processor is not accepting jobs")
            self._active_submitters += 1
            self._pending += 1

        accepted = False
        try:
            remaining = None if deadline is None else max(0, deadline - time.monotonic())
            try:
                self._queue.put((job, future), timeout=remaining)
                accepted = True
            except queue.Full:
                raise TimeoutError("timed out waiting for queue capacity")
        finally:
            with self._condition:
                if not accepted:
                    self._pending -= 1
                self._active_submitters -= 1
                self._condition.notify_all()

        return future

    def _worker(self) -> None:
        while True:
            item = self._queue.get()
            try:
                if item is self._STOP:
                    return

                job, future = item
                if not future.set_running_or_notify_cancel():
                    with self._condition:
                        self._cancelled += 1
                    continue

                try:
                    result = job.fn(*job.args, **job.kwargs)
                except Exception as exc:
                    future.set_exception(exc)
                    with self._condition:
                        self._failed += 1
                    log.exception("Job %s failed", job.job_id)
                else:
                    future.set_result(result)
                    with self._condition:
                        self._succeeded += 1
            finally:
                if item is not self._STOP:
                    with self._condition:
                        self._pending -= 1
                        self._condition.notify_all()
                self._queue.task_done()

    def wait_idle(self, timeout: float | None = None) -> bool:
        deadline = None if timeout is None else time.monotonic() + timeout
        with self._condition:
            while self._pending or self._active_submitters:
                remaining = None if deadline is None else deadline - time.monotonic()
                if remaining is not None and remaining <= 0:
                    return False
                self._condition.wait(remaining)
            return True

    def stats(self) -> dict[str, Any]:
        with self._condition:
            return {
                "state": self._state.name,
                "pending": self._pending,
                "queued": self._queue.qsize(),
                "active_submitters": self._active_submitters,
                "succeeded": self._succeeded,
                "failed": self._failed,
                "cancelled": self._cancelled,
                "workers": self._worker_count,
            }

    def shutdown(self, wait: bool = True) -> None:
        with self._condition:
            if self._state is State.NEW:
                self._state = State.CLOSED
                self._shutdown_done.set()
                return
            if self._state is State.CLOSED:
                return
            if self._state is State.RUNNING:
                self._state = State.CLOSING

            if not self._shutdown_started:
                self._shutdown_started = True
                threading.Thread(
                    target=self._finish_shutdown,
                    name="shutdown-coordinator",
                    daemon=False,
                ).start()

        if wait:
            if threading.current_thread() in self._threads:
                raise RuntimeError("worker cannot call shutdown(wait=True)")
            self._shutdown_done.wait()

    def _finish_shutdown(self) -> None:
        try:
            with self._condition:
                while self._active_submitters:
                    self._condition.wait()

            # No more submissions can be admitted. Drain every accepted job.
            self._queue.join()

            # Stop markers are inserted only after accepted work is drained.
            for _ in self._threads:
                self._queue.put(self._STOP)
            for thread in self._threads:
                thread.join()

            with self._condition:
                self._state = State.CLOSED
                self._condition.notify_all()
        finally:
            self._shutdown_done.set()

    def __enter__(self) -> "JobProcessor":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.shutdown(wait=True)


def process_job(job_id: int) -> dict[str, Any]:
    time.sleep(0.2)  # Simulate blocking I/O
    if job_id == 4:
        raise ValueError("simulated failure for job 4")
    return {"job_id": job_id, "processed": True}


def main() -> None:
    with JobProcessor(workers=3, queue_size=5) as processor:
        futures: list[tuple[int, Future]] = []
        for job_id in range(10):
            future = processor.submit(process_job, job_id, timeout=5)
            futures.append((job_id, future))

        for job_id, future in futures:
            try:
                print("SUCCESS:", future.result(timeout=10))
            except Exception as exc:
                print(f"FAILED job={job_id}: {exc}")

        processor.wait_idle(timeout=10)
        print("STATS before shutdown:", processor.stats())

    print("STATS after shutdown:", processor.stats())


if __name__ == "__main__":
    main()
