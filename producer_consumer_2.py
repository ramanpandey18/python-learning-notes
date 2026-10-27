from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from threading import Event
import time


class TemporaryError(Exception):
    """An error that may succeed if retried."""
    pass


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

    # Simulate a temporary failure for input 7.
    if value == 7 and attempt < 3:
        raise TemporaryError("Temporary service failure")

    # Simulate work that periodically checks cancellation.
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
    max_retries=3,
    base_delay=0.5,
):
    for attempt in range(1, max_retries + 2):
        check_cancelled(job_cancel, deadline)

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

            # Don't begin a retry wait beyond the deadline.
            if remaining <= 0:
                raise TimeoutError("Job timed out")

            print(
                f"Input {value}: attempt {attempt} failed; "
                f"retrying in {delay}s"
            )

            # Wait only as long as the remaining deadline allows.
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
    submission_limit = worker_count + max_pending

    # future -> job metadata
    futures = {}
    next_index = 0

    pool = ThreadPoolExecutor(max_workers=worker_count)

    try:
        while next_index < len(inputs) or futures:

            # Submit only up to the configured limit.
            while (
                next_index < len(inputs)
                and len(futures) < submission_limit
            ):
                index = next_index
                job_cancel = Event()

                # Timeout includes time spent waiting in the queue.
                deadline = time.monotonic() + job_timeout

                future = pool.submit(
                    process_with_retries,
                    inputs[index],
                    job_cancel,
                    deadline,
                )

                futures[future] = {
                    "index": index,
                    "cancel": job_cancel,
                    "deadline": deadline,
                }

                next_index += 1

            if not futures:
                break

            # Detect expired jobs without losing track of running futures.
            for future, info in list(futures.items()):
                if (
                    not future.done()
                    and results[info["index"]] is None
                    and time.monotonic() >= info["deadline"]
                ):
                    info["cancel"].set()

                    results[info["index"]] = {
                        "input": inputs[info["index"]],
                        "result": None,
                        "attempts": None,
                        "error": "Job timed out",
                    }

            # Wait briefly so we can check deadlines and react to Ctrl+C.
            pending = set(futures)
            completed, _ = wait(
                pending,
                timeout=0.05,
                return_when=FIRST_COMPLETED,
            )

            for future in completed:
                info = futures.pop(future)
                index = info["index"]

                # A timeout may already have been recorded.
                if results[index] is not None:
                    continue

                try:
                    outcome = future.result()

                    results[index] = {
                        "input": inputs[index],
                        "result": outcome["result"],
                        "attempts": outcome["attempts"],
                        "error": None,
                    }

                except Exception as exc:
                    results[index] = {
                        "input": inputs[index],
                        "result": None,
                        "attempts": None,
                        "error": str(exc),
                    }

    except KeyboardInterrupt:
        print("Shutdown requested...")

        # Signal all jobs, including jobs waiting in retry backoff.
        for info in futures.values():
            info["cancel"].set()

        for future in futures:
            future.cancel()

    finally:
        # Pending tasks are cancelled; running threads are awaited.
        pool.shutdown(wait=True, cancel_futures=True)

    return results


if __name__ == "__main__":
    inputs = [4, -2, 7, 3, -1, 8]

    results = run(
        inputs,
        worker_count=3,
        max_pending=3,
        job_timeout=2.0,
    )

    for index, item in enumerate(results):
        if item is None:
            print(f"Job {index}: not completed")
        elif item["error"] is not None:
            print(f"Job {index}: error: {item['error']}")
        else:
            print(
                f"Job {index}: result = {item['result']}, "
                f"attempts = {item['attempts']}"
            )

# This simple implementation sleeps inside a worker thread during backoff. That worker cannot process another job while waiting. For a small worker pool, frequent retries can reduce throughput.
# A more advanced design schedules retries for later instead of keeping a worker occupied. For now, this version is a good way to learn and explain retry behavior in an interview.
