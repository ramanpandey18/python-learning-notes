"""Bounded asyncio producer-consumer example; no blocking I/O calls."""
import asyncio
import random
from dataclasses import dataclass
from typing import Any


@dataclass
class Job:
    job_id: int


STOP = None


async def process(job: Job) -> dict[str, Any]:
    # Async sleep yields control to the event loop.
    await asyncio.sleep(random.uniform(0.05, 0.2))
    if job.job_id == 4:
        raise ValueError("simulated async job failure")
    return {"job_id": job.job_id, "processed": True}


async def worker(worker_id: int, jobs: asyncio.Queue) -> None:
    while True:
        job = await jobs.get()
        try:
            if job is STOP:
                return
            try:
                result = await process(job)
            except Exception as exc:
                print(f"WORKER {worker_id}: job {job.job_id} failed: {exc}")
            else:
                print(f"WORKER {worker_id}: {result}")
        finally:
            jobs.task_done()


async def producer(jobs: asyncio.Queue, count: int, worker_count: int) -> None:
    for job_id in range(count):
        await jobs.put(Job(job_id))  # Applies backpressure when full.
        print(f"SUBMITTED: {job_id}")

    await jobs.join()  # Wait for actual jobs to finish before stop markers.
    for _ in range(worker_count):
        await jobs.put(STOP)


async def main() -> None:
    worker_count = 3
    jobs: asyncio.Queue = asyncio.Queue(maxsize=5)

    tasks = [
        asyncio.create_task(worker(i + 1, jobs))
        for i in range(worker_count)
    ]
    await producer(jobs, count=10, worker_count=worker_count)
    await asyncio.gather(*tasks)
    print("All async workers stopped.")


if __name__ == "__main__":
    asyncio.run(main())
