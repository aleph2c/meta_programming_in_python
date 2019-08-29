# To avoid the mess described by decorators_as_classes_9.py you
# can do this instead:

import types
from functools import wraps

def profile(func):
  ncalls = 0
  @wraps(func)
  def wrapper(*args, **kwargs):
    nonlocal ncalls
    ncalls += 1
    return func(*args, **kwargs)
  wrapper.ncalls = lambda: ncalls
  return wrapper

# Example
@profile
def add(x, y):
  return x + y

add(3,2)
add(3,3)
add(3,3)
print(add.ncalls())

class Spam:
  @profile
  def bar(self, x):
    print(self, x)


s = Spam()
s.bar(1)
s.bar(1)
s.bar(1)
s.bar(1)
print(s.bar.ncalls())
