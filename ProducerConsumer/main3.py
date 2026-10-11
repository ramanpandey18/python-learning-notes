
import asyncio


async def process_job(job: int) -> int:
    await asyncio.sleep(0.2)  # Simulate asynchronous I/O

    if job == 4:
        raise ValueError("Invalid job")

    return job * 2


async def worker(queue: asyncio.Queue):
    while True:
        job = await queue.get()

        try:
            if job is None:
                return

            try:
                result = await process_job(job)
                print("SUCCESS:", job, result)
            except Exception as exc:
                print("FAILED:", job, exc)
        finally:
            queue.task_done()


async def main():
    worker_count = 3
    queue = asyncio.Queue(maxsize=6)

    workers = [
        asyncio.create_task(worker(queue))
        for _ in range(worker_count)
    ]

    # The producer naturally slows down when the queue is full.
    for job in range(10):
        await queue.put(job)

    # Drain all real jobs before requesting worker shutdown.
    await queue.join()

    for _ in range(worker_count):
        await queue.put(None)

    await asyncio.gather(*workers)


if __name__ == "__main__":
    asyncio.run(main())
