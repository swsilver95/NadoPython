foo = [1,2,3,"Hello", "World", [1,2,3]]
foo.append("Python")
foo.remove("Hello")
del foo[0]
foo[2] = "HI"

foo = {"짜장면":5000, "짬뽕":6000, "탕수육":12000}
print(foo["짜장면"])
print(foo.items())
print(foo.keys())
print(foo.values())

foo = (1,2,3)
print(foo[0])
# foo[0] = "Hello"
# foo.append("World")
# foo.remove(1)

foo = set([1,1,2,2,3,3,3,3,4])
foo2 = set([3,4,5])
print(foo)
print(foo & foo2)
print(foo | foo2)
print(foo - foo2)

print(True)
print(False)