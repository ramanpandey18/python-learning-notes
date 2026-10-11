class SquareIterator:
    def __init__(self, n):
        self.n = n
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.n:
            raise StopIteration
        result = self.current * self.current
        self.current += 1
        return result

for sq in SquareIterator(5):
    print(sq)