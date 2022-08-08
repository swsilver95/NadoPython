foo = "Hello World"
foo = 'Hello World'
foo = """Hello World"""
foo = '''Hello World'''

foo = '개가 "멍멍" 짖는다.'
foo = "개가 '멍멍' 짖는다."
foo = """개가
멍멍
짖는다."""
foo = '''개가
"""멍멍"""
짖는다.'''

foo = "Hello World"
print(foo[0])
print(foo[1:3])
print(foo[-1])

foo = "    Hello World    "
foo = foo.strip()
print(foo)

foo = "Hello World"
foo = foo.replace("World", "Python")
print(foo)

foo = ["Hello", "World", "Python", "Study"]
print(','.join(foo))