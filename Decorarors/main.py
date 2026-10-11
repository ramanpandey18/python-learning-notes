import time
from functools import wraps

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"{func.__name__} took {end_time - start_time:.4f}s")
        return result
    return wrapper


def retry(func):
    wraps(func)
    def wrapper(*args, **kwargs):
        attempts = 3
        for i in range(attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if i == attempts - 1:
                    raise
                print (f"attempt {i + 1} failed: {e}, retrying... ")
    return wrapper

def retry(times = 3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == times - 1:
                        raise
                    print(f"attemtp {i + 1} failed: {e}, retrying...")
        return wrapper
    return decorator

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        mp = {}
        l = 0
        res = 0

        for r in range(len(s)):
            if s[r] in mp:
                l = max(mp[s[r]] + 1, l)
            mp[s[r]] = r
            res = max(res, r - l + 1)
        return res

