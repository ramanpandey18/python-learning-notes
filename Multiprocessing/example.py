import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def work():
    total = 0

    for i in range(50_000_000):
        total += i

    return total


def main():
    # Sequential
    start = time.perf_counter()

    for _ in range(3):
        work()

    print("Sequential:", time.perf_counter() - start)

    # Threads
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(work)
            for _ in range(3)
        ]

        for future in futures:
            future.result()

    print("Threads:", time.perf_counter() - start)

    # Processes
    start = time.perf_counter()

    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(work)
            for _ in range(3)
        ]

        for future in futures:
            future.result()

    print("Processes:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
