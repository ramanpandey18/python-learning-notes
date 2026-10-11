"""Small, separate examples of common threading synchronization primitives."""
import threading
import time


def lock_example() -> None:
    lock = threading.Lock()
    counter = 0

    def increment() -> None:
        nonlocal counter
        for _ in range(10_000):
            with lock:
                counter += 1

    threads = [threading.Thread(target=increment) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Lock counter (expected 40000):", counter)


def rlock_example() -> None:
    lock = threading.RLock()

    def outer() -> None:
        with lock:
            inner()

    def inner() -> None:
        with lock:  # Same thread can acquire RLock recursively.
            print("RLock: nested acquisition succeeded")

    outer()


def semaphore_example() -> None:
    # At most two tasks in this section at once.
    slots = threading.Semaphore(2)

    def task(i: int) -> None:
        with slots:
            print(f"Semaphore task {i} entered")
            time.sleep(0.1)

    threads = [threading.Thread(target=task, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def event_example() -> None:
    stop = threading.Event()

    def worker() -> None:
        while not stop.is_set():
            print("Event worker working")
            if stop.wait(0.1):
                break
        print("Event worker stopping")

    t = threading.Thread(target=worker)
    t.start()
    time.sleep(0.25)
    stop.set()
    t.join()


def condition_example() -> None:
    condition = threading.Condition()
    ready = False

    def consumer() -> None:
        nonlocal ready
        with condition:
            condition.wait_for(lambda: ready)
            print("Condition: predicate became true")

    t = threading.Thread(target=consumer)
    t.start()
    time.sleep(0.1)
    with condition:
        ready = True
        condition.notify_all()
    t.join()


def barrier_example() -> None:
    barrier = threading.Barrier(3)

    def phase(i: int) -> None:
        print(f"Barrier participant {i} reached phase")
        barrier.wait()
        print(f"Barrier participant {i} passed phase")

    threads = [threading.Thread(target=phase, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    lock_example()
    rlock_example()
    semaphore_example()
    event_example()
    condition_example()
    barrier_example()
