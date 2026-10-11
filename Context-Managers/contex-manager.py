from contextlib import contextmanager

@contextmanager
def transaction():
    print("BEGIN TRANSACTION")
    try:
        yield
        print("COMMIT")           # runs if no exception in the with block
    except Exception as e:
        print(f"ROLLBACK: {type(e).__name__}: {e}")
        raise                      # re-raise so exception still propagates

# Test case 1: success
with transaction():
    print("Doing work...")

# Output:
# BEGIN TRANSACTION
# Doing work...
# COMMIT

# Test case 2: failure
with transaction():
    print("Doing work...")
    raise ValueError("Something broke")

# Output:
# BEGIN TRANSACTION
# Doing work...
# ROLLBACK: ValueError: Something broke
# ValueError: Something broke  ← exception still propagates because raise



from contextlib import contextmanager

@contextmanager
def transaction1():
    print("BEGIN TRANSACTION")
    try:
        yield
        print("COMMIT")
    except Exception as e:
        print(f"ROLLBACK: {type(e).__name__}: {e}")
        # NOTE: no `raise` here -- this is what suppresses the exception

with transaction1():
    print("Doing work...")
    raise ValueError("Something broke")

print("Program continues normally here!")  # this line WILL run — exception was swallowed
