
print("Hello")
print("World")

val = 1
print(val)
val = val + 1
print(val)
val = val + 1
print(val)

for i in range(1, 2):
    print(i, end=' ')

print('END')

res = 8
for i in range(1, 21):
    res += i

print("Total sum:", res)

l = []
for i in range(1, 21):
    l.append(i)
print("L=", l)

def sumn(n):
    res = 0
    for i in range(1, n+1):
        res += i
    return res
# -- The main program starts here
print("Sum of the 20 first integers: ", sumn(20))
print("Sum of the 100, frist integers: ", sumn(100))
