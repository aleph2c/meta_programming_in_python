# Re-metaclasses:
# class Foo:
#  pass
# x = Foo()
# x is an instance of class Foo
# Foo is an instance of type metaclass
# type is also an instance of type metaclass, so it is an instance of itself

# we want to define a metaclass that allows class definitions to supply optional
# arguments, possibly to control or configure aspects of processing during type
# creation.

# when defining classes, Python allows a metaclass to be specified using the
# metaclass keyword argument in the class assignment.  For example, with
# abstract base classes:
from abc import ABCMeta, abstractmethod

class IStream(metaclass=ABCMeta):
  @abstractmethod
  def read(self, maxsize=None):
    pass

  @abstractmethod
  def write(self, data):
    pass

# However, in custom metaclasses, additional keyword arguments can be supplied,
# you must include them on __prepare__(), __new__(), and __init__()

# __prepare__ called first and is used to create the class name space.  Normally
#         this method returns a dictionary or a simple mapping object
# __new__ is called next, it is use to instantiate the resulting type object.
#         It is called after the full class body has been executed.
# __init__ is called last, and used to perform any additional initialization
#         steps

# We use the keyword-only arguments in the recipe for debug and synchonize.
class MyMeta(type):
  # Optional
  @classmethod
  def __prepare__(cls, name, bases, *, debug=False, synchronize=False):
    # Custom processing
    # ...
    print('step 1')
    return super().__prepare__(name, bases)

  # Required
  def __new__(cls, name, bases, ns, *, debug=False, synchronize=False):
    # Custom processing
    # ...
    print('step 2')
    return super().__new__(cls, name, bases, ns)

  # Required
  def __init__(cls, name, bases, ns, *, debug=False, synchronize=False):
    # Custom processing
    # ...
    print('step 3')
    super().__init__(name, bases, ns)

# this could have been written as?
# Spam1 = type('Spam1', (), {'debug':True, 'synchronize'=True})
class Spam1(metaclass=MyMeta):
  debug = True
  synchronize = True
  # ... the above code is run even if this object is not instantiated
  def __init__(self):
    print('step 4')
    print(self.__class__.debug)
    print(self.__class__.synchronize)

Spam1 = type('Spam1', (), {'debug':True, 'synchronize'=True})
spam = Spam1()

# this will break, but it is kind of what we are trying to do in the first
# example
# class Spam2(metaclass=MyMeta(debug=True, synchronize=False)):
#   # ... the above code is run even if this object is not instantiated
#   def __init__(self):
#     print('step 4')
#     print(self.__class__.debug)
#     print(self.__class__.synchronize)

class Spam3(metaclass=MyMeta):
  # we are using keyword arguments, so we can change the order of our class
  # variables
  synchronize = True
  debug = False
  # ... the above code is run even if this object is not instantiated
  def __init__(self):
    print('step 4')
    print(self.__class__.debug)
    print(self.__class__.synchronize)

spam3 = Spam3()
