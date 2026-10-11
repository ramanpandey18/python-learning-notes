
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
logger = logging.getLogger(__name__)


class ProcessorState(Enum):
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


@dataclass
class JobOutcome:
    job_id: str
    success: bool
    result: Any = None
    error: Exception | None = None


class JobProcessor:
    """
    In-memory, bounded producer-consumer job processor.

    - Fixed number of worker threads.
    - Bounded pending-job queue.
    - Thread-safe submission and shutdown.
    - Per-job Future for results and exceptions.
    - Failed jobs do not terminate workers.
    """

    _STOP = object()

    def __init__(
        self,
        workers: int = 4,
        queue_size: int = 20,
    ):
        if workers < 1:
            raise ValueError("workers must be >= 1")
        if queue_size < 1:
            raise ValueError("queue_size must be >= 1")

        self._worker_count = workers
        self._queue: queue.Queue = queue.Queue(maxsize=queue_size)

        self._condition = threading.Condition()
        self._state = ProcessorState.NEW
        self._threads: list[threading.Thread] = []

        # Counts accepted jobs that haven't finished processing.
        self._pending = 0

        # These counters are protected by _condition.
        self._succeeded = 0
        self._failed = 0

    def start(self) -> None:
        with self._condition:
            if self._state is not ProcessorState.NEW:
                raise RuntimeError("Processor can only be started once")

            self._state = ProcessorState.RUNNING

            try:
                for index in range(self._worker_count):
                    thread = threading.Thread(
                        target=self._worker,
                        name=f"job-worker-{index + 1}",
                        daemon=False,
                    )
                    self._threads.append(thread)
                    thread.start()
            except BaseException:
                # Roll back safely if starting a worker fails.
                self._state = ProcessorState.CLOSING
                for _ in self._threads:
                    self._queue.put(self._STOP)

                # Do not leave partially started workers behind.
                started = [
                    thread for thread in self._threads
                    if thread.ident is not None
                ]
                self._condition.release()
                try:
                    for thread in started:
                        thread.join()
                finally:
                    self._condition.acquire()

                self._state = ProcessorState.CLOSED
                self._condition.notify_all()
                raise

    def submit(
        self,
        fn: Callable[..., Any],
        *args: Any,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> Future:
        """
        Accept a job, waiting at most `timeout` seconds for queue capacity.

        The timeout applies to queue insertion, not job execution.
        """
        future = Future()
        job = Job(
            job_id=str(uuid.uuid4()),
            fn=fn,
            args=args,
            kwargs=kwargs,
        )

        deadline = (
            None if timeout is None
            else time.monotonic() + timeout
        )

        # Holding the condition across put() prevents shutdown from
        # inserting stop markers before an accepted submission.
        with self._condition:
            if self._state is not ProcessorState.RUNNING:
                raise ProcessorClosedError(
                    "Processor is not accepting jobs"
                )

            while True:
                remaining = (
                    None if deadline is None
                    else deadline - time.monotonic()
                )

                if remaining is not None and remaining <= 0:
                    raise TimeoutError("Timed out waiting for queue capacity")

                try:
                    self._queue.put(
                        (job, future),
                        timeout=remaining,
                    )
                    break
                except queue.Full:
                    raise TimeoutError(
                        "Timed out waiting for queue capacity"
                    )

            self._pending += 1
            return future

    def _worker(self) -> None:
        while True:
            item = self._queue.get()

            try:
                if item is self._STOP:
                    return

                job, future = item

                # A caller may cancel a job that hasn't started yet.
                if not future.set_running_or_notify_cancel():
                    continue

                try:
                    result = job.fn(*job.args, **job.kwargs)
                except Exception as exc:
                    future.set_exception(exc)
                    with self._condition:
                        self._failed += 1

                    logger.exception(
                        "Job %s failed", job.job_id
                    )
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
        """Wait until all accepted jobs finish, without closing workers."""
        deadline = (
            None if timeout is None
            else time.monotonic() + timeout
        )

        with self._condition:
            while self._pending:
                remaining = (
                    None if deadline is None
                    else deadline - time.monotonic()
                )

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
                "succeeded": self._succeeded,
                "failed": self._failed,
                "workers": self._worker_count,
            }

    def shutdown(self, wait: bool = True) -> None:
        """
        Stop accepting jobs, drain accepted jobs, then stop workers.

        wait=False initiates shutdown in a separate coordinator thread.
        """
        with self._condition:
            if self._state is ProcessorState.CLOSED:
                return

            if self._state is ProcessorState.NEW:
                self._state = ProcessorState.CLOSED
                self._condition.notify_all()
                return

            if self._state is ProcessorState.RUNNING:
                self._state = ProcessorState.CLOSING

        if not wait:
            threading.Thread(
                target=self._finish_shutdown,
                name="job-shutdown",
                daemon=False,
            ).start()
            return

        self._finish_shutdown()

    def _finish_shutdown(self) -> None:
        # Queue.join() waits until every accepted job has been
        # acknowledged, including failed and cancelled jobs.
        self._queue.join()

        # No new submissions are allowed after CLOSING.
        # Workers can now be stopped.
        for _ in self._threads:
            self._queue.put(self._STOP)

        for thread in self._threads:
            thread.join()

        with self._condition:
            self._state = ProcessorState.CLOSED
            self._condition.notify_all()

    def __enter__(self) -> JobProcessor:
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.shutdown(wait=True)


# ---------------- Example workload ----------------

def process_job(job_id: int) -> dict:
    time.sleep(0.2)  # Simulate blocking I/O

    if job_id == 4:
        raise ValueError("Simulated job failure")

    return {
        "job_id": job_id,
        "processed": True,
    }


if __name__ == "__main__":
    with JobProcessor(workers=3, queue_size=20) as processor:
        futures: list[tuple[int, Future]] = []

        for job_id in range(10):
            future = processor.submit(
                process_job,
                job_id,
                timeout=5,
            )
            futures.append((job_id, future))

        # Consume outcomes instead of retaining them inside the
        # processor indefinitely.
        for job_id, future in futures:
            try:
                print("SUCCESS:", future.result(timeout=10))
            except Exception as exc:
                print(f"FAILED job={job_id}: {exc}")

        print("STATS:", processor.stats())

    print("Processor shut down.")
