def square_generator(n):
    for i in range(1, n + 1):
        yield i * i

for sq in square_generator(5):
    print(sq)

def square_generator_1(n):
    yield n * n

for sq in square_generator_1(5):
    print(sq)