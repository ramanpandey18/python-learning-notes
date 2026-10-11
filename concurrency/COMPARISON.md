# Python concurrency: choosing the right tool

## Decision table

| Model | Best fit | Parallel Python CPU execution? | Shared state | Main costs / risks |
|---|---|---:|---|---|
| Sequential | Small/simple workloads; baseline | One execution flow | Straightforward | No overlap |
| `threading.Thread` | A few long-lived blocking workers | Generally no for pure Python CPU work under standard CPython GIL | Shared process memory | Races, locks, lifecycle |
| `ThreadPoolExecutor` | Many independent blocking I/O tasks | Generally no for pure Python CPU work under standard CPython GIL | Shared process memory | Too many submitted tasks, shared-state bugs |
| `ProcessPoolExecutor` | CPU-heavy pure Python tasks | Yes, across processes/cores | Separate process memory | Startup, pickling, IPC, memory duplication |
| `asyncio` | Many concurrent I/O operations using async-compatible libraries | No, normally one event-loop thread | Same process; tasks interleave at `await` points | Blocking the event loop, cancellation and task-lifecycle complexity |
| Hybrid | Mixed workloads | Depends on the CPU stage | Depends on boundaries | More operational complexity |

“Generally” matters: native extensions may release the GIL, and free-threaded CPython builds change the CPU-threading tradeoff. Always measure the actual workload and interpreter.

## Fast decision path

1. Is the work mostly pure Python CPU computation?
   - Consider `ProcessPoolExecutor`.
2. Is the work mostly blocking I/O using synchronous libraries?
   - Consider `ThreadPoolExecutor` or a bounded thread worker queue.
3. Is the work mostly I/O and supported by async libraries?
   - Consider `asyncio`.
4. Is work arriving continuously?
   - Consider a producer/consumer design with bounded buffering and explicit shutdown.
5. Does a resource have a concurrency limit?
   - Use a semaphore or a bounded pool.
6. Does a remote API impose requests per second?
   - A semaphore alone is not a rate limiter; use time-based rate limiting too.

## Core distinctions

- **Concurrency:** multiple operations make progress over an overlapping period.
- **Parallelism:** operations execute at the same instant on different execution resources.
- **Backpressure:** a slow consumer makes the producer slow down, wait, or reject work.
- **Race condition:** result depends on the timing/interleaving of operations.
- **Deadlock:** participants wait indefinitely on each other/resources.
- **Future:** a handle for a result or exception that may become available later.
- **Cancellation:** often prevents pending work; it generally cannot safely force-stop arbitrary running Python code.
- **Graceful shutdown:** stop admission, finish accepted work according to policy, then stop workers.

## Senior interview checklist for a job processor

Discuss:
- bounded queue and producer backpressure
- fixed worker count
- per-job result and exception handling
- retries only when safe; idempotency for side effects
- job timeout versus submission timeout
- cancellation behavior
- graceful versus immediate shutdown
- metrics: queued, running, succeeded, failed, retries, queue wait and execution duration
- whether jobs must survive process crashes
- ordering and duplicate delivery requirements
- memory limits for payloads and retained results
