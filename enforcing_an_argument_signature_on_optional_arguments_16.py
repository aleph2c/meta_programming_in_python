# You've written a function or method that uses the *args and **kwargs, so that
# it can be general purpose, but you would also like to check the passed
# arguments to see if they match a specified calling signature.

from inspect import Signature, Parameter
import inspect

# Make a signature for a func(x, y=42, *, z=None)
params = [ Parameter('x', Parameter.POSITIONAL_OR_KEYWORD),
           Parameter('y', Parameter.POSITIONAL_OR_KEYWORD, default=42),
           Parameter('z', Parameter.KEYWORD_ONLY, default=None) ]
sig = Signature(params)
print(sig)

# Once you have a signature object, you can easily bind it to the *args and
# **kwargs using the signatures's bind() method, as shown in this simple
# example:

def func(*args, **kwargs):
  bound_values = sig.bind(*args, **kwargs)
  for name, value in bound_values.arguments.items():
    print(name, value)

def line():
  print('-'*10)

line(); func(1, 2, z=3)
line(); func(1)
line(); func(y=2, x=1)
# this should crash
# line(); func(1, 2, 3, 4)

def make_sig(*names):
  params = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) 
    for name in names]
  return Signature(params)

class Structure:
  _signature_ = make_sig()
  def __init__(self, *args, **kwargs):
    bound_values = self.__signature__.bind(*args, **kwargs)
    for name, value in bound_values.arguments.items():
      setattr(self, name, value)

# Example use
class Stock(Structure):
  __signature__ = make_sig('name', 'shares', 'price')

class Point(Structure):
  __signature__ = make_sig('x', 'y')

print(inspect.signature(Stock))
print(inspect.signature(Point))

s1 = Stock('ACME', 100, 490.1)
# this should crash!
# s2 = Stock('ACME', 100)

# this should crash! (common mistake)
# s3 = Stock('ACME', 100, 490.1, shares=50)

from inspect import Signature, Parameter

def make_sig(*names):
  parms = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names]
  return Signature(parms)

# start experiment
# trying to understand "make_sig(*clsdict.get('_fields', []))"
# 1) 'get' turns the dictionary into a list, defaulting the list to []
# 2) the * in front, causes the dictionary to splat into a set of distinct
# arguements given to the function _dict_function
# 3) the * in front of the make_sig, de-splats the set of distinct arguments
# back into a list
def _dict_function(*_dict_as_list):
  print(*_dict_as_list)

_dict = {'_fields':['bob', 'mary'], 'something_else':['whatever']}
print('here')
print(_dict.get('_fields', []))
_dict_function(*_dict.get('_fields', []))
print('here')
# finished experiment

class StructureMeta(type):
  def __new__(cls, clsname, bases, clsdict):
    clsdict['__signature__'] = make_sig(*clsdict.get('_fields', []))
    return super().__new__(cls, clsname, bases, clsdict)

class Structure(metaclass=StructureMeta):
  _fields = []
  def __init__(self, *args, **kwargs):
    bound_values = self.__signature__.bind(*args, **kwargs)
    for name, value in bound_values.arguments.items():
      # name is _fields key
      # value is the value provided in the instantiation
      setattr(self, name, value)

# Example
class Stock(Structure):
  _fields = ['name', 'shares', 'price']

class Point(Structure):
  _fields = ['x', 'y']

print(inspect.signature(Stock))

google_stock = Stock('GOOG', 120, 123.00)
