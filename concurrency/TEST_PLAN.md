# Testing and study plan

Don't run every experiment at once. Read the corresponding file first, predict behavior, then run it.

## 1. Thread job processor

Run:
```bash
python 01_job_processor_threads.py
```

Expected: most jobs succeed; one deliberate job fails; later jobs still run; the processor closes.

Then study:
- `queue.Queue(maxsize=...)`
- `put()` and `get()`
- `task_done()` versus `join()`
- `Future.result()`
- `Condition` and lifecycle state
- stop sentinels

Exercise: change the worker count to 1, then to 5. Change queue size to 1. Observe how bounded capacity affects submission.

Important: a timeout passed to `submit()` is a queue-admission timeout; it is not a timeout for the actual job. `Future.result(timeout=...)` controls how long the caller waits for a result, not how long the function is allowed to run.

## 2. Thread pool

Run:
```bash
python 02_thread_pool.py
```

Notice that `as_completed()` yields futures in completion order, not submission order. Exceptions are raised when you call `future.result()`.

Exercise: make one task raise; verify other tasks continue.

## 3. Process pool

Run:
```bash
python 03_multiprocessing_pool.py
```

The worker function is at module scope, and process creation is guarded by `if __name__ == "__main__":`. This matters because child processes must be able to import/reconstruct the callable.

Exercise: compare `workers=1` and `workers=3`. Timings vary by machine, CPU load and process startup cost. Do not expect exact linear speedup.

## 4. Async workers

Run:
```bash
python 04_asyncio_workers.py
```

Notice:
- `await queue.get()` suspends a task rather than blocking the whole event-loop thread.
- `asyncio.Queue` is for tasks in one event loop, not for OS-thread communication.
- `asyncio.sleep()` yields; `time.sleep()` would block the event loop.
- `asyncio.gather(..., return_exceptions=True)` allows the demonstration to collect worker task outcomes.

Exercise: change the queue size and worker count. Make a job raise.

## 5. Synchronization primitives

Run:
```bash
python 05_sync_primitives.py
```

For each primitive, explain which condition it solves and whether it protects data or coordinates timing.

## 6. Benchmarks

Run:
```bash
python 06_compare_models.py
```

It is a demonstration, not a formal benchmark. Close heavy applications, repeat multiple times, and compare medians. Process startup and hardware matter.

## Final oral practice

Answer these out loud:
1. Why doesn't the GIL make threads useless?
2. Why is a process pool usually better for pure Python CPU work?
3. Why can an unbounded queue cause memory exhaustion?
4. What's the difference between `Queue.join()` and `Thread.join()`?
5. Why can `future.result()` raise?
6. Why is `time.sleep()` harmful inside an async function?
7. Why is a semaphore not the same as a requests-per-second limiter?
8. What must happen before graceful shutdown inserts worker stop markers?
9. Can a running Python thread be safely force-killed?
10. What changes if jobs must survive process crashes?
