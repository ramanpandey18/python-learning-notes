from functools import reduce
numbers = [1, 2, 3, 4,]

#map
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

#filter
evens  = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)

#reduce
product = reduce(lambda x, y: x * y, numbers)
print(product)


numbers = [1, 2, 3, 4, 5, 6]

# 1. Filter out odd numbers -> [2, 4, 6]
# 2. Square the remaining numbers -> [4, 16, 36]
# 3. Sum them up -> 4 + 16 + 36 = 56
pipeline = reduce(lambda x, y : x + y, map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))
print(pipeline)


def get_list(n):
    return [i * i for i in range(n)]

def get_gen(n):
    for i in range(n):
        yield i * i


result = get_list(5)
print(f"result for get list is {result}")
result1 = get_gen(5)
print(f"result for get generator is {result1}")
print(next(result1))
print(next(result1))
print(next(result1))
print(next(result1))
print(next(result1))
# print(next(result1))