# you want to apply a decorator to a class or state method
# MAKE SURE your decorators are applied BEFORE the @classmethod or @staticmethod

import time
from functools import wraps

# A simple decorator
def timethis(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    start = time.time()
    r = func(*args, **kwargs)
    end = time.time()
    print(end - start)
    return r
  return wrapper

class Spam:
  @timethis
  def instance_method(self, n):
    print(self, n)
    while n > 0:
      n -= 1

  @classmethod
  @timethis
  def class_method(cls, n):
    print(cls, n)
    while n > 0:
      n -= 1

  @staticmethod
  @timethis
  def static_method(n):
    print(n)
    while n > 0:
      n -= 1

s = Spam()
s.instance_method(100000)
Spam.class_method(100001)
s.static_method(100002)
