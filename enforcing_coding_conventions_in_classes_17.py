# your program consists of a large hierarchy and you would like to enforce
# certain types of coding conventions (or perhaps diagnostics) to help maintain
# programmer sanity.

class MyMeta(type):
  def __new__(cls, clsname, bases, clsdict):
    return super().__new__(cls, clsname, bases, clsdict)

  def __init__(self, clsname, bases, clsdict):
    super().__init__(clsname, bases, clsdict)

class NoMixedCaseMeta(type):
  def __new__(cls, clsname, bases, clsdict):
    for name in clsdict:
      if name.lower() != name:
        raise TypeError('Bad attribute name: ' + name)
    return super().__new__(cls, clsname, bases, clsdict)

class Root(metaclass=NoMixedCaseMeta):
  pass

class A(Root):
  def foo_bar(self):  # Ok
    pass

# this will break! no CamelCase method names permitted
#class B(Root):
#  def fooBar(self):   # TypeError
#    pass

a = A()

# As a more advanced and useful example, here is a metaclass that checks the
# definition of redefined methods to make sure they are the same calling
# signature as the original method in the superclass

from inspect import signature
import logging

# Without the following line, nothing will show up.
# the basicConfig must be called before using the logger
logging.basicConfig(level=logging.DEBUG)

class MatchSignatureMeta(type):
  def __init__(self, clsname, bases, clsdict):
    super().__init__(clsname, bases, clsdict)
    # self is a class obj
    sup = super(self, self)
    for name, value in clsdict.items():
      if name.startswith('_') or not callable(value):
        continue
      # Get the previous definition (if any) and compare the signatures
      prev_dfn = getattr(sup, name, None)
      if prev_dfn:
        prev_sig = signature(prev_dfn)
        val_sig = signature(value)
        if prev_sig != val_sig:
          logging.warning('Signature mismatch in %s. %s != %s',
            value.__qualname__, prev_sig, val_sig)

# Example
class Root(metaclass=MatchSignatureMeta):
  pass

class A(Root):
  def foo(self, x, y):
    pass

  def spam(self, x, *, z):
    pass

# Class with redefined methods, but slightly different signatures
class B(A):
  def foo(self, a, b):
    pass

  def spam(self, x, z):
    pass
