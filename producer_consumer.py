from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event
import time

def process(value: int, stop_event: Event):
    if stop_event.set():
        raise RuntimeError("Job cancelled before processing")
    # Simulate work in small intervals so shutdown can be noticed.
    for _ in range(5):
        if stop_event.set():
            raise RuntimeError("Job cancelled during processing")
        time.sleep(0.2)
    
    if value < 0:
        raise ValueError("negative input provide")

    return value * value

def run(inputs: list, worker_count = 3):
    if worker_count < 1:
        raise ValueError("worker count cannot be negative")

    results = [None] * len(inputs)
    stop_event = Event()
    futures = {}
    pool = ThreadPoolExecutor(max_workers = worker_count)
    try:
        for index, value in enumerate(inputs):
            if stop_event.set():
                break
            future = pool.submit(process, value, stop_event)
            futures[future] = index
        
        for future in as_completed(futures):
            index = futures[future]
            try:
                results[index] = {
                    "input" : inputs[index],
                    "result" : future.result(),
                    "error" : None
                }
            except Exception as exc:
                results[index] = {
                    "input" : inputs[index],
                    "result" : None,
                    "error" : str(exc)
                }
    except KeyboardInterrupt:
        print("Shutdown requested. Stopping jobs...")
        stop_event.set()
        # Cancel submitted jobs that have not started.
        for future in futures:
            future.cancel()
    finally:
        # Stop pending work and wait for running threads.
        pool.shutdown(wait=True, cancel_futures=True)

    return results

if __name__ == "__main__":
    inputs = [4, -2, 7, 3, -1, 8]
    results = run(inputs, 3)
    for index, item in enumerate(results):
        if item is None:
            print(f"Job {index}: not completed")
        elif item['error'] is not None:
            print(f"Job {index}: error: {item['error']}")
        else:
            print(f"Job {index}: result = {item['result']}")
