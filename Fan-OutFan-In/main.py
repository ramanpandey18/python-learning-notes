from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def worker(job):
    print(f"[Worker] Starting job: {job}")
    time.sleep(0.3)              # simulate work
    result = job * job
    print(f"[Worker] Done job: {job} → result: {result}")
    return result

jobs = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print("=== Fan-Out + Fan-In ===\n")
start = time.time()

# Fan-Out: distribute all jobs across 3 workers
# Fan-In:  as_completed collects results as they finish
with ThreadPoolExecutor(max_workers=3) as executor:

    # FAN-OUT — submit all jobs
    futures = [executor.submit(worker, job) for job in jobs]
    print(f"[Fan-Out] {len(jobs)} jobs distributed across 3 workers\n")

    # FAN-IN — collect results as they complete
    results = []
    for future in as_completed(futures):
        result = future.result()
        results.append(result)
        print(f"[Fan-In] Collected result: {result}")

print(f"\nAll results: {sorted(results)}")
print(f"Total time:  {time.time() - start:.2f}s")
print(f"Expected:    {[j*j for j in jobs]}")
