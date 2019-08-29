# you are using exec() to executre a fragment of code in the scope of the
# caller, but after execution, noe of its results seem to be visible.
import sys
a = 13
exec('b = a + 1')
print(b)   # =>  14 

# but look
def test():
  a = 13
  exec('c = a + 1')
  print(c)

print('continuing ... ')

# this will crash:
try:
  test()
except:
  print(sys.exc_info())

print('continuing ... ')

# to fix this problem we need to use the locals() function to obtain a
# dictionary of local variable prior to the call to exec().  Immediately
# afterward, you can extract modified values from the locals dictionary.

def test():
  a = 13
  loc = locals()
  exec("d = a + 1")
  d = loc['d']
  print(d)

test()

print('continuing ... ')

# The correct use of exec is very tricky.  So try and avoid it.  The code in
# exec never actually makes any changes to the local variable within a function,
# because the local variables passed to exec are a copy of the locals in the
# function.  If you change this copy, it doesn't change the original.

def test1():
  x = 0
  exec('x += 1')
  print(x)

test1()

print('continuing ... ')

# When you call locals() to obtain a copy of the local variables, you get the
# copy of the locals that will be passed to exec.

def test2():
  x = 0
  loc = locals()
  print('before:', loc)
  exec('x += 1')
  print('after:', loc)
  print('x =', x)

test2()

print('continuing ... ')

# With any use of locals(), you need to be careful about the order of
# operations.  Each time it is invoked, locals() will take the current value of
# the local variables and overwrite the corresponding entries in the dictionary:

def test3():
  x = 0
  loc = locals()
  print(loc)
  exec('x += 1')
  print(loc)
  locals()
  print(loc)

test3()
print('continuing ... ')

# An alternative to using locals is to pass your global and local dictionary to
# the exec function:

def test4():
  a = 13
  loc = {'a': a}
  glb = {}
  exec('b = a + 1', glb, loc)
  b = loc['b']
  print(b)

test4()
