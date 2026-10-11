import sys

list_version = [x**2 for x in range(1000000)]
gen_version = (x**2 for x in range(1000000))

print(sys.getsizeof(list_version))
print(sys.getsizeof(gen_version))