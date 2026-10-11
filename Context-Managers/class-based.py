class Transaction:
    def __enter__(self):
        print("BEGIN TRANSACTION")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            print("COMMIT")
        else:
            print(f"ROLLBACK: {exc_type.__name__}: {exc_value}")
        return False  # don't suppress — let exception propagate

# Test case 1: success
with Transaction():
    print("Doing work...")

# Output:
# BEGIN TRANSACTION
# Doing work...
# COMMIT

# Test case 2: failure
with Transaction():
    print("Doing work...")
    raise ValueError("Something broke")

# Output:
# BEGIN TRANSACTION
# Doing work...
# ROLLBACK: ValueError: Something broke
# ValueError: Something broke  ← exception still propagates because return False


class Transaction1:
    def __enter__(self):
        print("BEGIN TRANSACTION")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            print("COMMIT")
        else:
            print(f"ROLLBACK: {exc_type.__name__}: {exc_value}")
        return True  # <-- suppress the exception (dangerous in real code!)

with Transaction1():
    print("Doing work...")
    raise ValueError("Something broke")

print("Program continues normally here!")  # this line WILL run — exception was swallowed