from multiprocessing import Pool
import time

def heavy_computation(n):
    print(f"[Process] Starting task {n}")
    total = sum(i * i for i in range(5_000_000))  # heavy CPU work
    print(f"[Process] Done task {n} → result: {total}")
    return total

if __name__ == "__main__":
    numbers = [1, 2, 3, 4]

    # WITHOUT multiprocessing — sequential
    print("=== Sequential ===")
    start = time.time()
    results = [heavy_computation(n) for n in numbers]
    print(f"Sequential time: {time.time() - start:.2f}s\n")

    # WITH multiprocessing — parallel
    print("=== Parallel ===")
    start = time.time()
    with Pool(processes=4) as pool:
        results = pool.map(heavy_computation, numbers)
    print(f"Parallel time:   {time.time() - start:.2f}s")