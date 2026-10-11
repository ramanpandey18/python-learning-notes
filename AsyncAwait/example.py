import asyncio
import time

async def fetch_service_a():
    await asyncio.sleep(1)
    return "Result A"

async def fetch_service_b():
    await asyncio.sleep(1)
    return "Result B"

async def main():
    start = time.perf_counter()
    results = await asyncio.gather(fetch_service_a(), fetch_service_b())
    end = time.perf_counter()
    print(f"Rsults: {results}")
    print(f"Time taken: {end - start:.2f}s")

asyncio.run(main())

