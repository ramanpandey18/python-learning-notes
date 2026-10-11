
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import BoundedSemaphore
import time


def process_job(job: int) -> int:
    time.sleep(0.2)  # Simulate blocking I/O

    if job == 4:
        raise ValueError("Invalid job")

    return job * 2


def run_jobs(jobs, workers=3, max_in_flight=6):
    # Bound running + submitted-but-not-finished work.
    slots = BoundedSemaphore(max_in_flight)
    futures = {}

    def release_slot(future):
        slots.release()

    with ThreadPoolExecutor(max_workers=workers) as pool:
        try:
            for job in jobs:
                slots.acquire()  # Backpressure
                try:
                    future = pool.submit(process_job, job)
                except BaseException:
                    slots.release()
                    raise

                futures[future] = job
                future.add_done_callback(release_slot)

            # Process outcomes as jobs complete.
            for future in as_completed(futures):
                job = futures[future]
                try:
                    result = future.result()
                    print("SUCCESS:", job, result)
                except Exception as exc:
                    print("FAILED:", job, exc)

        finally:
            # The executor context waits for submitted jobs to finish.
            # The futures dictionary retains results until this function exits.
            pass


if __name__ == "__main__":
    run_jobs(range(10), workers=3, max_in_flight=6)
