import time
import functools

def retry(times=3, delay=2, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < times:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@retry(times=3, delay=1)
def flaky_function():
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure")
    return "success"

flaky_function()
