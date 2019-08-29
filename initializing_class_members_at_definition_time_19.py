# You want ot initialize parts of the class definition once at the time a class
# is defined, not when instances are created.

import operator

class StructTupleMeta(type):
  def __init__(cls, *args, **kwargs):
    print('init in StructTupleMeta')
    super().__init__(*args, **kwargs)
    for n, name in enumerate(cls._fields):
      # it's a tuple, we are creating the ability to reach in
      # and get the correct item from the tuple
      # 
      # enumerate return an index, item for each thing in the list
      # 
      # itemgetter:
      # def itemgetter(*items):
      #   if len(items) == 1:
      #     item = items[0] 
      #     def g(obj):  # where is the obj coming from?
      #        return obj[item]
      #   else:
      #     def g(obj):
      #       return tuple(obj[item] for item in times)
      #   return g
      # itemgetter(1)('ABCDEFG')  # => 'B'
      # itemgetter(1, 3, 5)('ABCDEFG')  # => ('B', 'D', 'F')

      # class property(fget=None, fset=None, fdel=None, doc=None)
      #  in our case only fget is populated
      #  wraps a function... (don't complete undertand this)

      # setattr will set cls.name to what is returned by the property.
      # what I don't understand is how the operator.itemgetter(n) can access the
      # inner part of the tuple. (the obj)
      setattr(cls, name, property(operator.itemgetter(n)))

# Make an immutable object which is set once at creation than can never be set
# again.  (like a namedtuple)
class StructTuple(tuple, metaclass=StructTupleMeta):
  _fields = []
  # __new__ is called before an instance is created
  # "setting the tuple contents at definition time"
  def __new__(cls, *args):
    print('new in StructTuple')
    if len(args) != len(cls._fields):
      raise ValueError('{} arguments required'.format(len(cls._fields)))
    return super().__new__(cls, args)

class Stock(StructTuple):
  _fields = ['name', 'shares', 'price']

class Point(StructTuple):
  _fields = ['x', 'y']

# the magic must happen at this point
import pdb; pdb.set_trace()
s = Stock('ACME', 50, 91.1)
print(s.price)
