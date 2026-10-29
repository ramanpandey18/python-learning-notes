s = "Never odd or even"
s1 = "Hello"
s2 = "aba"
def palindrome(s):
    s = s.replace(" ", "").lower()
    return s == s[::-1]

def palindrome_v1(s):
    s = s.lower()
    left = 0
    right = len(s) - 1
    while left < right:
        while left < right and s[left] == " ":
            left += 1
        while left < right and s[right] == " ":
            right -= 1
        if s[left] != s[right]:
            return False
        left  += 1
        right -= 1
    return True

def palindrome_v2(s):
    s = s.lower()
    left = 0
    right = len(s) - 1
    while left < right:
        if s[left] == " ":
            left += 1
            continue
        if s[right] == " ":
            right -= 1
            continue
        if s[left] != s[right]:
            return False
        left  += 1
        right -= 1
    return True

res = palindrome(s)
print(res)
res1 = palindrome(s1)
print(res1)
res2 = palindrome(s2)
print(res2)

res = palindrome_v1(s)
print(res)
res1 = palindrome_v1(s1)
print(res1)
res2 = palindrome_v1(s2)
print(res2)

res = palindrome_v2(s)
print(res)
res1 = palindrome_v2(s1)
print(res1)
res2 = palindrome_v2(s2)
print(res2)