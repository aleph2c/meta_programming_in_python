import weakref

# metaclass to turn another class into a singleton
class Singleton(type):

  def __init__(self, *args, **kwargs):
    self.__instance = None
    super().__init__(*args, **kwargs)

  def __call__(self, *args, **kwargs):
    if self.__instance is None:
      self.__instance = super().__call__(*args, **kwargs)
      return self.__instance
    else:
      return self.__instance

class Spam1(metaclass=Singleton):
  def __init__(self):
    print('Creating spam')

# metaclass to turn another class into a staticmethod only container
class NoInstances(type):
  def __call__(self, *args, **kwargs):
    raise TypeError("Can't instantiate directly")

class Spam2(metaclass=NoInstances):
  @staticmethod
  def grok(x):
    print('Spam.grok')

class Cached(type):
  def __init__(self, *args, **kwargs):
    print('Calling meta class __init__')
    super().__init__(*args, **kwargs)
    self.__cache = weakref.WeakValueDictionary()

  def __call__(self, *args):
    print('Calling meta class __call__')
    if args in self.__cache:
      return self.__cache[args]
    else:
      obj = super().__call__(*args)
      self.__cache[args] = obj
      return obj

class Spam3(metaclass=Cached):
  def __init__(self, name):
    print('Creating Spam({!r})'.format(name))
    self.name = name

a = Spam1()
b = Spam1()
assert(a == b)
Spam2.grok(42)

a3 = Spam3('Guido')
b3 = Spam3('Diana')
c3 = Spam3('Guido')  # Cached
print(a3 is b3)
print(a3 is c3)


