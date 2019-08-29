# we want to define a metaclass that allows class definitions to supply optional
# arguments, possiblly to control or configure aspects of processing during type
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

class MyMeta(type):
  # Optional
  @classmethod
  def __prepare__(cls, name, bases, *, debug=False, synchronize=False):
    # Custom processing
    # ...
    return super().__prepare__(name, bases)

  # Required
  def __new__(cls, name, bases, ns, *, debug=False, synchronize=False):
    # Custom processing
    # ...
    return super().__new__(cls, name, bases, ns)

  # Required
  def __init__(cls, name, bases, ns, *, debug=False, synchronize=False):
    # Custom processing
    # ...
    super().__init__(name, bases, ns)
