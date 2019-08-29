# You want to define decorator inside of a class definition and apply it to
# other functions or methods
from functools import wraps

class A:
  # Decorator as an instance method
  def decorator1(self, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      print('Decorator 1')
      return func(*args, **kwargs)
    return wrapper

  # Decorator as a class method
  @classmethod
  def decorator2(cls, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      print('Decorator 2')
      return func(*args, **kwargs)
    return wrapper

a = A()

@a.decorator1
def spam1():
  print('spam 1')

@A.decorator2
def spam2():
  print('spam 2')

spam1()
spam2()
