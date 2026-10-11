"""ProcessPoolExecutor: suitable for CPU-heavy pure Python tasks."""
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed


def cpu_work(n: int) -> int:
    # Top-level function: process workers must be able to import it.
    total = 0
    for i in range(n):
        total += i
    return total


def main() -> None:
    inputs = [8_000_000, 8_000_000, 8_000_000]

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(cpu_work, n) for n in inputs]
        for future in as_completed(futures):
            print("Result:", future.result())

    print(f"Processes: {time.perf_counter() - start:.2f}s")
    print("Logical CPUs:", os.cpu_count())
    print("Remember: process startup and machine load affect timings.")


if __name__ == "__main__":
    main()
