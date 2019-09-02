# You're writing code that ultimately needs to create a new class object.
# You've thought about emitting class source code to string and using functions
# such as exec() to evaluate it, but you'd prefer a more elegant solution.

# stock.py
# Example of making a class manually from parts
# Methods
def __init__(self, name, shares, price):
  self.name = name
  self.shares = shares
  self.price = price

def cost(self):
  return self.shares * self.price

cls_dict = {
  '__init__' : __init__,
  'cost' : cost, 
}

# Manually Make a class
import types

Stock = types.new_class('Stock', (), {}, lambda ns: ns.update(cls_dict))
# this is needed for pickle
Stock.__module__ = __name__
s = Stock('ACME', 50, 91.1)
print(s)
print(s.cost())

# Manually Make a class with a metaclass
import abc
Stock = types.new_class('Stock', (), {'metaclass': abc.ABCMeta}, lambda ns: ns.update(cls_dict))
Stock.__module__ == __name__
print(Stock)

# The third argument can also contain keyword arguments

# class Spam(Base, debug=True, typecheck=False):
#   pass

# Spam = types.new_class('Spam', (Base,) {'debug': True, 'typecheck': False},
#     lambda ns: ns.update(cls_dict))

# Re-implement namedtuple:

import operator
import types
import sys

def named_tuple(classname, fieldnames):
  # Populate a dictionary of field property accessors
  # Re: operator.itemgetter(n)
  # Return a callable object that fetches item from its operand using the
  # operand's __getitem__() (__getitem__(a, b)return value of a at index b)
  # method.  If multiple items are specified, returns a tuple of lookup values.
  #   f = itemgetter(2), the call f(r) returns r[2]
  cls_dict = { name: property(operator.itemgetter(n))
    for n, name in enumerate(fieldnames) }
  # Make a __new__ function and add to the class dict
  def __new__(cls, *args):
    if len(args) != len(fieldnames):
      raise TypeError('Expected {} arguments'.format(len(fieldnames)))
    return tuple.__new__(cls, args)

  cls_dict['__new__'] = __new__
  
  # Make a class
  cls = types.new_class(classname, (tuple,), {}, lambda ns: ns.update(cls_dict))

  # Set the module to that of the caller
  cls.__module__ = sys._getframe(1).f_globals['__name__']
  return cls

Point = named_tuple('Point', ['x', 'y'])
print(Point)
p = Point(4, 5)
print(len(p))

print(p.x)
print(p.y)
# this should break (it's a namedtuple)
p.x = 2
