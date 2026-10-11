from concurrent.futures import (
    ProcessPoolExecutor,
    wait,
    FIRST_COMPLETED,
)
from time import perf_counter


def cpu_job(n: int) -> int:
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    total = 0
    for i in range(n):
        total += i

    return total


def run_jobs(jobs, max_workers=3, max_in_flight=6):
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    if max_in_flight < 1:
        raise ValueError("max_in_flight must be at least 1")

    start = perf_counter()
    job_iterator = iter(jobs)
    futures = {}

    with ProcessPoolExecutor(max_workers=max_workers) as pool:

        # Fill the initial window.
        for _ in range(max_in_flight):
            try:
                job = next(job_iterator)
            except StopIteration:
                break

            future = pool.submit(cpu_job, job)
            futures[future] = job

        # Keep replacing completed jobs until everything is submitted.
        while futures:
            completed, _ = wait(
                futures,
                return_when=FIRST_COMPLETED,
            )

            for future in completed:
                job = futures.pop(future)

                try:
                    result = future.result()
                    print(f"SUCCESS: job={job}, result={result}")
                except Exception as exc:
                    print(f"FAILED: job={job}, error={exc}")

                # Submit one replacement for each completed job.
                try:
                    next_job = next(job_iterator)
                except StopIteration:
                    continue

                new_future = pool.submit(cpu_job, next_job)
                futures[new_future] = next_job

    print(f"Total execution time: {perf_counter() - start:.2f} seconds")


if __name__ == "__main__":
    run_jobs(
        jobs=(n for n in [5_000_000, 5_000_000, -1, 5_000_000,
                         5_000_000, 5_000_000, 5_000_000]),
        max_workers=3,
        max_in_flight=6,
    )
