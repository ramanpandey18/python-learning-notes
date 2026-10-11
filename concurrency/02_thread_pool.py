"""ThreadPoolExecutor: suitable for independent blocking I/O tasks."""
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch_simulated(job_id: int) -> dict:
    # Represents a blocking network or SDK call.
    time.sleep(0.1 * (job_id % 3 + 1))
    if job_id == 4:
        raise ValueError("simulated failure")
    return {"job_id": job_id, "value": job_id * 10}


def main() -> None:
    jobs = range(10)
    with ThreadPoolExecutor(max_workers=3, thread_name_prefix="io-worker") as pool:
        futures = {pool.submit(fetch_simulated, job_id): job_id for job_id in jobs}

        for future in as_completed(futures):
            job_id = futures[future]
            try:
                print("DONE:", future.result())
            except Exception as exc:
                print(f"FAILED job={job_id}: {exc}")


if __name__ == "__main__":
    main()
