nums = [1, 2, 3]  # iterable, has __iter__() only no __next__()
it = iter(nums)  # iterator, has __iter__() and __next__() both
next(it) # 1
next(it) # 2
next(it) # 3
next(it) # StopIteration


# both are equivalent

for x in nums:
    print(x)

itr = iter(nums) # calls nums.__iter__()
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    print(x)
