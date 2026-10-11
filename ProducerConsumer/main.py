import threading
import queue
import time

def producer(q):
    jobs = ["job1", "job2", "job3", "job4", "job5", "job6"]
    for job in jobs:
        print(f"[Producer] Queuing: {job}")
        q.put(job)
        time.sleep(0.2)        # produce one job every 0.2s

    q.put(None)                # poison pill — signals stop
    print("[Producer] Done — sent poison pill")

def consumer(q, worker_id):
    while True:
        item = q.get()         # blocks until item available
        if item is None:
            q.put(None)        # pass pill to next worker
            print(f"[Worker {worker_id}] Stopping")
            break
        print(f"[Worker {worker_id}] Processing: {item}")
        time.sleep(0.5)        # each job takes 0.5s to process
        print(f"[Worker {worker_id}] Done: {item}")

q = queue.Queue()

producer_thread = threading.Thread(target=producer, args=(q,))
workers = [
    threading.Thread(target=consumer, args=(q, i))
    for i in range(3)
]

producer_thread.start()
for w in workers:
    w.start()

producer_thread.join()
for w in workers:
    w.join()

print("\nAll jobs processed!")
