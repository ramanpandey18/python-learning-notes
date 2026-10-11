import asyncio
import time

# --- Snippet 1 ---
async def fetch_data_multi(url):
    print(f"Fetching {url}")
    await asyncio.sleep(1)
    print(f"Done {url}")
    return f"data from {url}"

async def main_gather():
    start = time.time()
    results = await asyncio.gather(
        fetch_data_multi("url1"),
        fetch_data_multi("url2"),
        fetch_data_multi("url3")
    )
    print(f"\nResults: {results}")
    print(f"Total time: {time.time() - start:.2f}s")

asyncio.run(main_gather())

# --- Snippet 2 ---
async def fetch_data_single():
    await asyncio.sleep(1)
    return "data"

def main_sync():
    result = asyncio.run(fetch_data_single())
    print(result)

print("=" * 40)
print("SNIPPET 2 — fetch_data_single")
print("=" * 40)
main_sync()
print()


# Source - https://stackoverflow.com/a/53420574
# Posted by Levon, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-10, License - CC BY-SA 4.0

import asyncio
import time

# ─────────────────────────────────────────
# Snippet 1 — pure sync, sequential
# ─────────────────────────────────────────
def run_sync():
    def sleep(start):
        print(f'Time: {time.time() - start:.2f}')
        time.sleep(1)

    def sum_(name, numbers, start):
        total = 0
        for number in numbers:
            print(f'Task {name}: Computing {total}+{number}')
            sleep(start)
            total += number
        print(f'Task {name}: Sum = {total}\n')

    start = time.time()
    sum_("A", [1, 2], start)
    sum_("B", [1, 2, 3], start)
    end = time.time()
    print(f'Time: {end-start:.2f} sec\n')


# ─────────────────────────────────────────
# Snippet 2 — async but WRONG (time.sleep blocks)
# ─────────────────────────────────────────
def run_async_wrong():
    start = time.time()

    async def sleep():
        print(f'Time: {time.time() - start:.2f}')
        time.sleep(1)                    # ← blocks the event loop

    async def sum_(name, numbers):
        total = 0
        for number in numbers:
            print(f'Task {name}: Computing {total}+{number}')
            await sleep()
            total += number
        print(f'Task {name}: Sum = {total}\n')

    loop = asyncio.new_event_loop()
    tasks = [
        loop.create_task(sum_("A", [1, 2])),
        loop.create_task(sum_("B", [1, 2, 3])),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    end = time.time()
    print(f'Time: {end-start:.2f} sec\n')


# ─────────────────────────────────────────
# Snippet 3 — async CORRECT (asyncio.sleep yields)
# ─────────────────────────────────────────
def run_async_correct():
    start = time.time()

    async def sleep():
        print(f'Time: {time.time() - start:.2f}')
        await asyncio.sleep(1)           # ← yields, other tasks run

    async def sum_(name, numbers):
        total = 0
        for number in numbers:
            print(f'Task {name}: Computing {total}+{number}')
            await sleep()
            total += number
        print(f'Task {name}: Sum = {total}\n')

    loop = asyncio.new_event_loop()
    tasks = [
        loop.create_task(sum_("A", [1, 2])),
        loop.create_task(sum_("B", [1, 2, 3])),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    end = time.time()
    print(f'Time: {end-start:.2f} sec\n')


# ─────────────────────────────────────────
# Call all three
# ─────────────────────────────────────────
print("=" * 40)
print("SYNC (sequential)")
print("=" * 40)
run_sync()

print("=" * 40)
print("ASYNC WRONG (time.sleep blocks)")
print("=" * 40)
run_async_wrong()

print("=" * 40)
print("ASYNC CORRECT (asyncio.sleep)")
print("=" * 40)
run_async_correct()
