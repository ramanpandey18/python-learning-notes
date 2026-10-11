from concurrent.futures import ThreadPoolExecutor
import time


def task(n):
    print(f"Task {n} started")
    time.sleep(2)
    print(f"Task {n} finished")


tasks = range(1, 7)

start = time.time()

with ThreadPoolExecutor(max_workers=6) as executor:
    executor.map(task, tasks)

print(f"Total time: {time.time() - start:.2f}s")
