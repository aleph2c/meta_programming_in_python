class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  @property
  def name(self):
    return self._name

  @name.setter
  def prop(self, value):
    if not isinstance(value, str):
      raise TypeError('name must be a string')
    self._name = value

  @property
  def age(self):
    return self._age

  @age.setter
  def age(self, value):
    if not isinstance(value, int):
      raise TypeError('age must be an int')
    self._age = value

# we you see code like this, you should explore different ways of simplifying
# it.  One possbiel approach is to make a function that simply defines the
# property for you and returns it.  For example:

def typed_property(name, expected_type):
  storage_name = "_" + name

  @property
  def prop(self):
    return getattr(self, storage_name)

  @prop.setter
  def prop(self, value):
    if not isinstance(value, expected_type):
      raise TypeError('{} must be a {}'.format(name, expected_type))
    setattr(self, storage_name, value)
  return prop

# Example use
class Person:
  name = typed_property('name', str)
  age = typed_property('age', int)
  def __init__(self, name, age):
    self.name = name
    self.age = age

scott = Person(name="Scott", age=45)
print(scott.age)
print(scott.name)
scott.age += 1
print(scott.age)
scott.name += " " + "Volk"
print(scott.name)

# you can compact the typed_property macro like this
from functools import partial

String = partial(typed_property, expected_type=str)
Integer = partial(typed_property, expected_type=int)

# Example
class Person:
  name = String('name')
  age = Integer('age')
  def __init__(self, name, age):
    self.name = name
    self.age = age

scott = Person(name="Scott", age=21)
print(scott.age)
print(scott.name)
scott.age += 1
print(scott.age)
scott.name += " " + "Volk"
print(scott.name)
