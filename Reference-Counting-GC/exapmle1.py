import weakref

class Node:
    def __init__(self, name):
        self.name = name
        self.ref = None

a = Node("A")
b = Node("B")
a.ref = weakref.ref(b)  # weak reference — doesn't increase b's refcount
b.ref = a

del b
print(a.ref())  # what do you think this prints? try it before reading on