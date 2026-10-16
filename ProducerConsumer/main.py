
import threading
import queue
import time

job_queue = queue.Queue()
STOP = None


# The work each job performs
def process_job(job_id):
    time.sleep(1)

    if job_id == 4:
        raise ValueError("Job 4 failed!")

    return f"Job {job_id} completed"


# Each worker continuously consumes jobs
def worker():
    while True:
        job_id = job_queue.get()

        try:
            if job_id is STOP:
                return

            try:
                result = process_job(job_id)
                print("SUCCESS:", result)

            except Exception as error:
                print(f"FAILED: Job {job_id}: {error}")

        finally:
            job_queue.task_done()


# Create exactly 3 workers
workers = []

for _ in range(3):
    thread = threading.Thread(target=worker)
    thread.start()
    workers.append(thread)


# Submit 10 jobs
for job_id in range(1, 11):
    job_queue.put(job_id)


# Wait until all jobs are processed
job_queue.join()


# Tell workers to stop
for _ in workers:
    job_queue.put(STOP)

# Wait for every worker to exit
for thread in workers:
    thread.join()

print("All jobs finished. Processor stopped.")
