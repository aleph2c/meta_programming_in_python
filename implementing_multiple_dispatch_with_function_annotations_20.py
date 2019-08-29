# method overloading based on types in python

# could we write code like this?
# class Spam:
#  def bar(self, x:int, y:int):
#    print('Bar 1', x, y)
#  def bar(self, s:str, n:int=0):
#    print('Bar 2', s, n)
# 
# s = Spam()
# s.bar(2, 3)    # => Bar 1: 2 3
# s.bar('hello') # => Bar 2: hello 0

import inspect
import types

class MultiMethod:
  '''represents a signal multimethod'''
  def __init__(self, name):
    self._methods = {}
    self.__name__ = name
  def register(self, method):
    '''register a new method as a multimethod'''
    sig = inspect.signature(method)
    # Build a type signature from the method's annotation
    types = []
    for name, param in sig.parameters.items():
      if name == 'self':
        continue
      if param.annotation is inspect.Parameter.empty:
        raise TypeError(
          'Argument {} must be anotated with a type'.format(name)
        )
      if not isinstance(param.annotation, type):
        raise TypeError(
          'Argument {} annotation must be a type'.format(name)
        )
      if param.default is not inspect.Parameter.empty:
        self._methods[tuple(types)] = method
      types.append(param.annotation)

    self._methods[tuple(types)] = method

  def __call__(self, *args):
    '''
    call a method based on type signature of the arguments
    '''
    types = tuple(type(arg) for arg in args[1:])
    method = self._methods.get(types, None)
    if method:
      return method(*args)
    else:
      raise TypeError('No matching method for types {}'.format(types))

  def __get__(self, instance, cls):
    '''
    descriptor method needed to make calls work in a class
    '''
    if instance is not None:
      return types.MethodType(self, instance)
    else:
      return self

class MultiDict(dict):
  '''
  special dictionary to build multimethods in a metaclass
  '''
  def __setitem__(self, key, value):
    if key in self:
      # If key alread exists, it must be a multimethod or callable
      current_value = self[key]
      if isinstance(current_value, MultiMethod):
        current_value.register(value)
      else:
        mvalue = MultiMethod(key)
        mvalue.register(current_value)
        mvalue.register(value)
        super().__setitem__(key, mvalue)
    else:
      super().__setitem__(key, value)

class MultipleMeta(type):
  '''
  Metaclass that allows multiple dispatch of methods
  '''
  def __new__(cls, clsname, bases, clsdict):
    return type.__new__(cls, clsname, bases, dict(clsdict))

  @classmethod
  def __prepare__(cls, clsname, bases):
    return MultiDict()

# to use this code:
class Spam(metaclass=MultipleMeta):
  def bar(self, x:int, y:int):
    print('Bar 1:', x, y)

  def bar(self, s:str, n:int = 0):
    print('Bar 2:', s, n)

# Example: overloading __init__
import time 
class Date(metaclass=MultipleMeta):
  def __init__(self, year:int, month:int, day:int):
    self.year = year
    self.month = month
    self.day = day

  def __init__(self):
    t = time.localtime()
    self.__init__(t.tm_year, t.tm_mon, t.tm_mday)

s = Spam()
s.bar(2, 3)
s.bar('hello')

d = Date(2012, 12, 21)
e = Date()
print(e.year)
