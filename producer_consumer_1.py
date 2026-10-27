from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from threading import Event
import time


class TemporaryError(Exception):
    """An error that may succeed if retried."""
    pass


def process(value: int, stop_event: Event, attempt: int):
    if stop_event.is_set():
        raise RuntimeError("Job cancelled")

    # Simulate a temporary failure for input 7.
    # It fails twice, then succeeds on attempt 3.
    if value == 7 and attempt < 3:
        raise TemporaryError("Temporary service failure")

    # Simulate processing.
    for _ in range(5):
        if stop_event.is_set():
            raise RuntimeError("Job cancelled")
        time.sleep(0.02)

    if value < 0:
        raise ValueError("Negative input")

    return value * value


def process_with_retries(
    value: int,
    stop_event: Event,
    max_retries=3,
    base_delay=0.5,
):
    for attempt in range(1, max_retries + 2):
        try:
            result = process(value, stop_event, attempt)

            return {
                "result": result,
                "attempts": attempt,
            }

        except TemporaryError:
            # No retries left: let the error propagate.
            if attempt > max_retries:
                raise

            # Exponential backoff: 0.5s, 1s, 2s...
            delay = base_delay * (2 ** (attempt - 1))
            print(
                f"Input {value}: attempt {attempt} failed; "
                f"retrying in {delay}s"
            )

            # Wait can be interrupted by a shutdown request.
            if stop_event.wait(delay):
                raise RuntimeError("Job cancelled during retry wait")


def run(inputs: list, worker_count=3, max_pending=3):
    if worker_count < 1:
        raise ValueError("worker_count must be positive")
    if max_pending < 1:
        raise ValueError("max_pending must be positive")

    results = [None] * len(inputs)
    stop_event = Event()
    submission_limit = worker_count + max_pending
    futures = {}
    next_index = 0

    pool = ThreadPoolExecutor(max_workers=worker_count)

    try:
        while next_index < len(inputs) or futures:
            while (
                next_index < len(inputs)
                and len(futures) < submission_limit
            ):
                future = pool.submit(
                    process_with_retries,
                    inputs[next_index],
                    stop_event,
                )
                futures[future] = next_index
                next_index += 1

            if not futures:
                break

            completed, _ = wait(
                futures,
                return_when=FIRST_COMPLETED,
            )

            for future in completed:
                index = futures.pop(future)

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
        stop_event.set()

        for future in futures:
            future.cancel()

    finally:
        pool.shutdown(wait=True, cancel_futures=True)

    return results


if __name__ == "__main__":
    inputs = [4, -2, 7, 3, -1, 8]
    results = run(inputs, worker_count=3, max_pending=3)

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