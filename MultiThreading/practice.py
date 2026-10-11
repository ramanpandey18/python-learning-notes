# import time

# def fetch_url(n):
#     print(f"Fetching URL {n}...")
#     time.sleep(1)  # simulates network wait
#     return f"Result {n}"

# def sequential_fetch(count):
#     start = time.perf_counter()
#     results = []
#     for i in range(count):
#         results.append(fetch_url(i))
#     end = time.perf_counter()
#     print(f"Sequential took {end - start:.2f} seconds")
#     return results

# sequential_fetch(5)

# import time
# import threading

# def fetch_url(n, results, index):
#     print(f"Fetching URL {n}...")
#     time.sleep(1)
#     results[index] = f"Result {n}"

# def threaded_fetch(count):
#     start = time.perf_counter()
#     results = [None] * count
#     threads = []
    
#     for i in range(count):
#         t = threading.Thread(target=fetch_url, args=(i, results, i))
#         threads.append(t)
#         t.start()
    
#     for t in threads:
#         t.join()
    
#     end = time.perf_counter()
#     print(f"Threaded took {end - start:.2f} seconds")
#     return results

# threaded_fetch(5)


# import asyncio
# import time

# async def fetch_url_async(n):
#     print(f"Fetching URL {n}...")
#     await asyncio.sleep(1)
#     return f"Result {n}"

# async def async_fetch(count):
#     start = time.perf_counter()
    
#     results = await asyncio.gather(*[fetch_url_async(i) for i in range(count)])
    
#     end = time.perf_counter()
#     print(f"Asyncio took {end - start:.2f} seconds")
#     return results

# asyncio.run(async_fetch(5))

# import time
# from multiprocessing import Process, Manager

# def fetch_url_mp(n, results, index):
#     print(f"Fetching URL {n}...")
#     time.sleep(1)
#     results[index] = f"Result {n}"

# def multiprocess_fetch(count):
#     start = time.perf_counter()
#     manager = Manager()
#     results = manager.list([None] * count)
#     processes = []
    
#     for i in range(count):
#         p = Process(target=fetch_url_mp, args=(i, results, i))
#         processes.append(p)
#         p.start()
    
#     for p in processes:
#         p.join()
    
#     end = time.perf_counter()
#     print(f"Multiprocessing took {end - start:.2f} seconds")
#     return list(results)

# if __name__ == "__main__":
#     multiprocess_fetch(5)


import time
import threading
from multiprocessing import Process, Manager

def count_primes(start, end, results=None, index=None):
    count = 0
    for num in range(start, end):
        if num < 2:
            continue
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    if results is not None and index is not None:
        results[index] = count
    return count

def sequential_primes():
    start = time.perf_counter()
    ranges = [(0, 100000), (100000, 200000), (200000, 300000), (300000, 400000)]
    total = 0
    for r in ranges:
        total += count_primes(*r)
    end = time.perf_counter()
    print(f"Sequential: {end - start:.2f}s, total primes: {total}")

def threaded_primes():
    start = time.perf_counter()
    ranges = [(0, 100000), (100000, 200000), (200000, 300000), (300000, 400000)]
    results = [None] * len(ranges)
    threads = []
    
    for i, r in enumerate(ranges):
        t = threading.Thread(target=count_primes, args=(r[0], r[1], results, i))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    total = sum(results)
    end = time.perf_counter()
    print(f"Threaded:   {end - start:.2f}s, total primes: {total}")

def multiprocess_primes():
    start = time.perf_counter()
    ranges = [(0, 100000), (100000, 200000), (200000, 300000), (300000, 400000)]
    manager = Manager()
    results = manager.list([None] * len(ranges))
    processes = []
    
    for i, r in enumerate(ranges):
        p = Process(target=count_primes, args=(r[0], r[1], results, i))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    total = sum(results)
    end = time.perf_counter()
    print(f"Multiproc:  {end - start:.2f}s, total primes: {total}")

if __name__ == "__main__":
    sequential_primes()
    threaded_primes()
    multiprocess_primes()


import time
import asyncio

async def count_primes_async(start, end):
    # No 'await' inside this loop -- pure blocking CPU work.
    # This is the key thing to notice: async def alone doesn't make code concurrent.
    count = 0
    for num in range(start, end):
        if num < 2:
            continue
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count

async def async_primes_main():
    ranges = [(0, 100000), (100000, 200000), (200000, 300000), (300000, 400000)]
    start = time.perf_counter()

    results = await asyncio.gather(*[count_primes_async(r[0], r[1]) for r in ranges])

    total = sum(results)
    end = time.perf_counter()
    print(f"Asyncio (CPU-bound):  {end - start:.2f}s, total primes: {total}")

if __name__ == "__main__":
    asyncio.run(async_primes_main())