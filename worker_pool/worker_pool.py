from concurrent.futures import (
    ThreadPoolExecutor,
    wait,
    FIRST_COMPLETED,
    CancelledError,
)
from threading import Event, Lock
import logging
import time


# Configure logging once for the application.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(threadName)s %(message)s",
)
logger = logging.getLogger(__name__)


class TemporaryError(Exception):
    """An error that may succeed if retried."""
    pass


class Metrics:
    """Thread-safe counters and duration measurements."""

    def __init__(self):
        self.lock = Lock()
        self.counters = {
            "submitted": 0,
            "succeeded": 0,
            "failed": 0,
            "timed_out": 0,
            "cancelled": 0,
            "retries": 0,
            "attempts": 0,
        }
        self.total_duration = 0.0
        self.completed_durations = 0

    def increment(self, name, amount=1):
        with self.lock:
            self.counters[name] += amount

    def record_duration(self, duration):
        with self.lock:
            self.total_duration += duration
            self.completed_durations += 1

    def snapshot(self):
        with self.lock:
            counters = self.counters.copy()
            total_duration = self.total_duration
            duration_count = self.completed_durations

        average_duration = (
            total_duration / duration_count
            if duration_count
            else 0.0
        )

        return {
            **counters,
            "average_duration_seconds": round(average_duration, 4),
            "total_duration_seconds": round(total_duration, 4),
        }


def check_cancelled(job_cancel: Event, deadline: float):
    if job_cancel.is_set():
        raise RuntimeError("Job cancelled")

    if time.monotonic() >= deadline:
        raise TimeoutError("Job timed out")


def process(
    value: int,
    job_cancel: Event,
    deadline: float,
    attempt: int,
):
    check_cancelled(job_cancel, deadline)

    # Simulate a transient failure for input 7.
    if value == 7 and attempt < 3:
        raise TemporaryError("Temporary service failure")

    # Simulate work that cooperatively checks cancellation.
    for _ in range(5):
        check_cancelled(job_cancel, deadline)
        time.sleep(0.02)

    check_cancelled(job_cancel, deadline)

    if value < 0:
        raise ValueError("Negative input")

    return value * value


def process_with_retries(
    value: int,
    job_cancel: Event,
    deadline: float,
    metrics: Metrics,
    max_retries=3,
    base_delay=0.5,
):
    logger.info("Job started: input=%s", value)

    for attempt in range(1, max_retries + 2):
        check_cancelled(job_cancel, deadline)
        metrics.increment("attempts")

        logger.info(
            "Job attempt: input=%s attempt=%s",
            value,
            attempt,
        )

        try:
            result = process(
                value,
                job_cancel,
                deadline,
                attempt,
            )

            return {
                "result": result,
                "attempts": attempt,
            }

        except TemporaryError:
            if attempt > max_retries:
                raise

            check_cancelled(job_cancel, deadline)

            delay = base_delay * (2 ** (attempt - 1))
            remaining = deadline - time.monotonic()

            if remaining <= 0:
                raise TimeoutError("Job timed out")

            metrics.increment("retries")

            logger.warning(
                "Retrying job: input=%s attempt=%s delay=%.2fs",
                value,
                attempt,
                delay,
            )

            # Backoff can end early when cancellation is requested.
            if job_cancel.wait(min(delay, remaining)):
                raise RuntimeError("Job cancelled")

            check_cancelled(job_cancel, deadline)


def run(
    inputs: list,
    worker_count=3,
    max_pending=3,
    job_timeout=2.0,
):
    if worker_count < 1:
        raise ValueError("worker_count must be positive")
    if max_pending < 1:
        raise ValueError("max_pending must be positive")
    if job_timeout <= 0:
        raise ValueError("job_timeout must be positive")

    results = [None] * len(inputs)
    metrics = Metrics()

    submission_limit = worker_count + max_pending
    futures = {}
    next_index = 0

    pool = ThreadPoolExecutor(max_workers=worker_count)

    try:
        while next_index < len(inputs) or futures:

            # Submit jobs only while below the outstanding-job limit.
            while (
                next_index < len(inputs)
                and len(futures) < submission_limit
            ):
                index = next_index
                job_cancel = Event()
                submitted_at = time.monotonic()
                deadline = submitted_at + job_timeout

                future = pool.submit(
                    process_with_retries,
                    inputs[index],
                    job_cancel,
                    deadline,
                    metrics,
                )

                futures[future] = {
                    "index": index,
                    "cancel": job_cancel,
                    "deadline": deadline,
                    "submitted_at": submitted_at,
                }

                metrics.increment("submitted")
                logger.info(
                    "Job submitted: index=%s input=%s",
                    index,
                    inputs[index],
                )

                next_index += 1

            if not futures:
                break

            # Detect expired jobs without losing track of running futures.
            for future, info in list(futures.items()):
                index = info["index"]

                if (
                    not future.done()
                    and results[index] is None
                    and time.monotonic() >= info["deadline"]
                ):
                    info["cancel"].set()

                    results[index] = {
                        "input": inputs[index],
                        "result": None,
                        "attempts": None,
                        "error": "Job timed out",
                    }

                    metrics.increment("timed_out")
                    duration = time.monotonic() - info["submitted_at"]
                    metrics.record_duration(duration)

                    logger.error(
                        "Job timed out: index=%s input=%s duration=%.2fs",
                        index,
                        inputs[index],
                        duration,
                    )

            # Wake periodically to check deadlines and cancellation.
            completed, _ = wait(
                set(futures),
                timeout=0.05,
                return_when=FIRST_COMPLETED,
            )

            for future in completed:
                info = futures.pop(future)
                index = info["index"]

                # The timeout may already have been recorded.
                if results[index] is not None:
                    continue

                duration = time.monotonic() - info["submitted_at"]
                metrics.record_duration(duration)

                try:
                    outcome = future.result()

                    results[index] = {
                        "input": inputs[index],
                        "result": outcome["result"],
                        "attempts": outcome["attempts"],
                        "error": None,
                    }

                    metrics.increment("succeeded")
                    logger.info(
                        "Job succeeded: index=%s attempts=%s duration=%.2fs",
                        index,
                        outcome["attempts"],
                        duration,
                    )

                except CancelledError:
                    results[index] = {
                        "input": inputs[index],
                        "result": None,
                        "attempts": None,
                        "error": "Job cancelled",
                    }

                    metrics.increment("cancelled")
                    logger.warning("Job cancelled: index=%s", index)

                except Exception as exc:
                    error = str(exc)
                    was_cancelled = (
                        isinstance(exc, RuntimeError)
                        and "cancelled" in error.lower()
                    )

                    results[index] = {
                        "input": inputs[index],
                        "result": None,
                        "attempts": None,
                        "error": error,
                    }

                    if was_cancelled:
                        metrics.increment("cancelled")
                        logger.warning(
                            "Job cancelled: index=%s reason=%s",
                            index,
                            error,
                        )
                    else:
                        metrics.increment("failed")
                        logger.error(
                            "Job failed: index=%s error=%s duration=%.2fs",
                            index,
                            error,
                            duration,
                        )

    except KeyboardInterrupt:
        logger.warning("Shutdown requested by user")

        for info in futures.values():
            info["cancel"].set()

        for future in futures:
            future.cancel()

    finally:
        pool.shutdown(wait=True, cancel_futures=True)

    # Mark jobs not collected because of interruption.
    for index, item in enumerate(results):
        if item is None:
            results[index] = {
                "input": inputs[index],
                "result": None,
                "attempts": None,
                "error": "Cancelled or not completed",
            }

            metrics.increment("cancelled")
            logger.warning("Job not completed: index=%s", index)

    logger.info("Final metrics: %s", metrics.snapshot())

    return results, metrics.snapshot()


if __name__ == "__main__":
    inputs = [4, -2, 7, 3, -1, 8]

    results, metrics = run(
        inputs,
        worker_count=3,
        max_pending=3,
        job_timeout=2.0,
    )

    print("\n--- Job Results ---")

    for index, item in enumerate(results):
        if item["error"] is not None:
            print(f"Job {index}: error: {item['error']}")
        else:
            print(
                f"Job {index}: result={item['result']}, "
                f"attempts={item['attempts']}"
            )

    print("\n--- Metrics ---")
    for name, value in metrics.items():
        print(f"{name}: {value}")

