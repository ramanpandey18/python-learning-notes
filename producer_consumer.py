from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def process(value: int):
    time.sleep((abs(value) % 3) * 0.05)
    if value < 0:
        raise ValueError("negative input provide")

    return value * value

def run(inputs: list, worker_count = 3):
    if worker_count < 1:
        raise ValueError("worker count cannot be negative")

    results = [None] * len(inputs)
    with ThreadPoolExecutor(max_workers = worker_count) as pool:
        futures = {pool.submit(process, value): index for index, value in enumerate(inputs)}

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
    return results

if __name__ == "__main__":
    inputs = [4, -2, 7, 3, -1, 8]
    results = run(inputs, 3)
    for index, item in enumerate(results):
        if item['error'] is not None:
            print(f"Job {index}: error: {item['error']}")
        else:
            print(f"Job {index}: result = {item['result']}")
