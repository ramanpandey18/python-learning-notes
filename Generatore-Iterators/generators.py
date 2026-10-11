def square_generator(n):
    for i in range(1, n + 1):
        yield i * i

for sq in square_generator(5):
    print(sq)