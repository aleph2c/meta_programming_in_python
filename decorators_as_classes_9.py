# if you want decorators to work both inside and outside of class definitions

import types
from functools import wraps

class Profiled:
  def __init__(self, func):
    wraps(func)(self)
    self.ncalls = 0

  def __call__(self, *args, **kwargs):
    '''making a callable class'''
    self.ncalls += 1
    # __wrapped__ contains the original func
    return self.__wrapped__(*args, **kwargs)

  def __get__(self, instance, cls):
    '''still don't understand how this works'''
    if instance is None:
      # this is never run
      return self
    else:
      print("__get__ ", self, instance)
      return types.MethodType(self, instance)

@Profiled
def add(x, y):
  return x + y

class Spam:
  @Profiled
  def bar(self, x):
    print(self, x)

  @classmethod
  @Profiled
  def foo(cls, x):
    print(cls, x)

print(add(2, 3))
print(add(4, 5))
print(add.ncalls)

s = Spam()
s.bar(1)
s.bar(2)
print(s.bar.ncalls)

Spam.foo(2)
Spam.foo(3)
Spam.foo(4)
print(Spam.foo.ncalls)
