from threading import Lock

class Singleton:
    _instance = None
    _lock = Lock()
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
        

a = Singleton()
b = Singleton()

print(a is b)

# obj1 = DB()
# obj2 = DB()