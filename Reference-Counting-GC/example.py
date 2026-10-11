import sys
import gc

class Node:
    def __init__(self, name):
        self.name = name
        self.ref = None

# Step 1: observe basic refcounting
a = Node("A")
print(sys.getrefcount(a))  # notice it's 2, not 1 (extra ref from getrefcount's own argument)

# Step 2: create a circular reference
a = Node("A")
b = Node("B")
a.ref = b
b.ref = a

print(sys.getrefcount(a))  # still shows refs even though nothing external points to it now

# Step 3: delete external references
del a
del b
# At this point, A and B still exist in memory — they reference each other
# refcount never hit 0, so normal refcounting can't clean them up

# Step 4: force garbage collection
collected = gc.collect()
print(f"Objects collected: {collected}")