class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        x = self.a
        if x <= 20:
            self.a += 1
        else:
            raise StopIteration
        return x

myclass = MyNumbers()
myiter = iter(myclass)

for x in myiter:
    print(x)