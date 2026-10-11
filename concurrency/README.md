# Python Concurrency Interview Lab (Python 3.9+)

A compact, runnable study pack for backend interviews. No database, broker, or external dependency.

## Files

1. `01_job_processor_threads.py` — bounded producer/consumer with fixed worker threads, Futures, backpressure, failure isolation, graceful shutdown.
2. `02_thread_pool.py` — `ThreadPoolExecutor`, `submit`, `as_completed`, result/exception handling.
3. `03_multiprocessing_pool.py` — CPU-bound work with `ProcessPoolExecutor`, pickling and `__main__` guard.
4. `04_asyncio_workers.py` — bounded `asyncio.Queue`, async workers, sentinels, per-job error isolation.
5. `05_sync_primitives.py` — Lock, RLock, Semaphore, Event, Condition, Barrier examples.
6. `06_compare_models.py` — simple benchmark for sequential/thread/process CPU-bound work.
7. `COMPARISON.md` — decision table and interview-ready rules.
8. `TEST_PLAN.md` — a safe, ordered plan to test and understand the code.

## Run

Use your existing virtual environment:

```bash
python --version
python 01_job_processor_threads.py
python 02_thread_pool.py
python 03_multiprocessing_pool.py
python 04_asyncio_workers.py
python 05_sync_primitives.py
python 06_compare_models.py
```

Run each script separately. Multiprocessing requires importable top-level functions and the `if __name__ == "__main__":` guard. Online interpreters and notebook-like runners may not support process pools reliably; use a normal `.py` file.

## Suggested order (about 2–3 hours)

1. Read `COMPARISON.md` first (5–10 min).
2. Read `01_job_processor_threads.py` top-to-bottom without testing yet (25–35 min).
3. Read `02_thread_pool.py` (10 min).
4. Read `03_multiprocessing_pool.py` and compare with the CPU benchmark (20 min).
5. Read `04_asyncio_workers.py` (25–35 min).
6. Skim and explain `05_sync_primitives.py` (15–20 min).
7. Review the decision table and interview questions (20 min).

Do not try to memorize every line. For each file, answer: what executes work, where is state stored, what bounds memory/concurrency, how are failures reported, and how does shutdown work?

## Important limitations

These are teaching examples, not a production-ready task queue:
- In-memory jobs are lost if the process exits or crashes.
- Retry, durable delivery, idempotency, rate limiting and observability need deliberate designs.
- A bounded queue limits queued items, not memory retained by callers or job payload sizes.
- The thread job processor's shutdown path is intentionally straightforward; before production use, test lifecycle races, start failures, cancellation, and concurrent shutdown callers thoroughly.
