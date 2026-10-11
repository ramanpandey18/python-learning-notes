"""Illustrative benchmark: sequential vs threads vs processes for CPU work."""
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def cpu_work(n: int) -> int:
    total = 0
    for i in range(n):
        total += i
    return total


def timed(label, fn) -> None:
    start = time.perf_counter()
    fn()
    print(f"{label}: {time.perf_counter() - start:.2f}s")


def main() -> None:
    # Tune n down if your computer takes too long; repeat several times for
    # meaningful comparisons. This is not a scientific benchmark.
    n = 5_000_000
    jobs = [n, n, n]

    timed("Sequential", lambda: [cpu_work(x) for x in jobs])

    def run_threads():
        with ThreadPoolExecutor(max_workers=3) as pool:
            list(pool.map(cpu_work, jobs))
    timed("Threads", run_threads)

    def run_processes():
        with ProcessPoolExecutor(max_workers=3) as pool:
            list(pool.map(cpu_work, jobs))
    timed("Processes", run_processes)


if __name__ == "__main__":
    main()
