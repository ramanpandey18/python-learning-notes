import functools

class memoize:
    def __init__(self, func):
        self.func = func
        self.cache = {}
        functools.update_wrapper(self, func)  # preserves __name__, __doc__ for class-based decorators

    def __call__(self, *args, **kwargs):
        # kwargs aren't hashable directly as a dict, so convert to a sorted tuple
        key = (args, tuple(sorted(kwargs.items())))
        if key not in self.cache:
            self.cache[key] = self.func(*args, **kwargs)
        return self.cache[key]

@memoize
def expensive_computation(n):
    print(f"Computing for {n}...")
    return n ** 2

print(expensive_computation(4))  # Computing for 4... -> 16
print(expensive_computation(4))  # 16 (cached, no print)
print(expensive_computation(5))  # Computing for 5... -> 25
