"""
03_multiprocessing_pool.py

Demonstrates:
1. Fixed number of worker processes
2. Submitting CPU-bound jobs
3. Collecting results as jobs complete
4. Propagating job exceptions through Future.result()
5. Measuring execution time

Run this file directly:
    python 03_multiprocessing_pool.py
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
from time import perf_counter


# This function runs inside a worker process.
# Keep it at module level so it can be pickled.
def cpu_job(n: int) -> int:
    total = 0

    for i in range(n):
        total += i

    return total


# Example of a job that fails.
def cpu_job_with_error(n: int) -> int:
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    return cpu_job(n)


def run_jobs(
    jobs: list[int],
    max_workers: int = 3,
) -> None:
    """
    Execute CPU-bound jobs using a fixed-size process pool.

    Args:
        jobs: Input values passed to cpu_job_with_error.
        max_workers: Maximum number of worker processes.
    """
    start = perf_counter()

    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        # Submit jobs without waiting for each one to finish.
        future_to_job = {
            pool.submit(cpu_job_with_error, n): n
            for n in jobs
        }

        # Process results in completion order, not submission order.
        for future in as_completed(future_to_job):
            job = future_to_job[future]

            try:
                result = future.result()
                print(f"SUCCESS: job={job}, result={result}")

            except Exception as exc:
                # The exception raised inside the worker is re-raised
                # here when future.result() is called.
                print(f"FAILED: job={job}, error={exc}")

    elapsed = perf_counter() - start
    print(f"Total execution time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    run_jobs(
        jobs=[
            5_000_000,
            5_000_000,
            -1,           # Deliberately fails to demonstrate error handling
        ],
        max_workers=3,
    )
