# re-write portions of your class definition to alter its behavior, but without
# using inheritance or metaclasses

def log_getattribute(cls):
  # get the original implimentation
  orig_getattribute = cls.__getattribute__

  # make a new definition
  def new_getattribute(self, name):
    print('getting:', name)
    return orig_getattribute(self, name)

  # attach to the class and return
  cls.__getattribute__ = new_getattribute
  return cls

# example use
@log_getattribute
class A:
  def __init__(self, x):
    self.x = x
  def spam(self):
    pass

a = A(42)
a.x
a.spam()
