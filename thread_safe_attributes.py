import time
import random
import logging
from threading import Event
from threading import Thread
from collections import deque

log_file = 'thread_safe_attribute.log'
with open(log_file, 'w') as fp:
  fp.write("")

logging.basicConfig(
  format='%(asctime)s:%(message)s',
  filename=log_file,
  level=logging.INFO)

class A1():
  def __init__(self):
    self._name = deque(maxlen=1)
    self._name.append(None)

  @property
  def name(self):
    return self._name[-1]

  @name.setter 
  def name(self, value):
    self._name.append(value)

class MetaThreadSafeAttribute(type):

  def __init__(self, clsname, bases, clsdict):
    '''Build the thread safe properties of the class using this as a metaclass

    **Args**:
       | ``self`` (cls): The cls using this metaclass
       | ``clsname`` (str): The name of the class
       | ``bases`` (bases): The base clases used by cls
       | ``clsdict`` (dict): The namespace of the cls

    '''
    # Note, self is the cls of the class using this metaclass
    for name in self._attributes:
      self.thread_safe_property(name)
    super().__init__(clsname, bases, clsdict)

  def __call__(self, *args, **kwargs):
    '''pre-process a class's __init__ call.

    The __call__ magic method grabs '()', so if a class is being constructed, we
    will catch this, and define the required deque objects in the intance of the
    class.

    **Note**:
       This class does the following, given a <name> from the
       '_attributes' list, class variable:

       self._<name> = deque(maxlen=1)
       self._<name>.append(0)

    **Args**:
       | ``*args`` (list): positional arguments
       | ``**kwargs``(dict): keyword arguments


    **Returns**:
       (self): return an initialized instance
    '''
    for name in self._attributes:
      self.__class__.create_deque(self, name)
    self.__init__(self, *args, **kwargs)
    return self

  @staticmethod
  def thread_safe_property(name):
    '''Create a thread safe property

    **Args**:
       | ``name`` (str): the name of the property
    '''
    storage_name = '_' + name

    @property
    def _prop(self):
      return exec('self.{}[-1]'.format(storage_name))

    @_prop.setter
    def _prop(self, value):
      exec('self.{}.append(value)'.format(storage_name))

  @staticmethod
  def create_deque(obj, name):
    '''Create and populate a small deque

    **Args**:
       | ``obj`` (self): self object of the instance using this metaclass
       | ``name`` (str): name of the attribute used by the property

    '''
    setattr(obj, name, deque(maxlen=1))
    exec('obj.{}.append(0)'.format(name))



def make_test_thread(name, object_to_hammer, thread_event):
  def thread_runner(name, obj, e):
    while e.is_set():
      if random.choice(list(['get', 'set'])) == 'get':
        logging.info(name + str(obj.hammed_attribute))
      else:
        obj.hammed_attribute += 1 
      time.sleep(random.uniform(0, 0.5))
  return Thread(target=thread_runner, name=name, daemon=True, args=(name, object_to_hammer, thread_event))

def test_thread_safe_attribute(time_in_seconds, number_of_threads, log_file):
  '''test the thread safe attribute feature provided by miros

    This test will create and run a given number of threads for a given number
    of seconds.  Each thread will either set an attribute or increment an
    attribute.  The results will be written to a log file (logging is thread
    safe) at INFO level.  This same log file will be openned at the end of the test, and it will be checked
    to confirm that the numbers increased monotonically.  This is confirming
    that all threads accessed and changed the same variable.

    **Args**:
       | ``time_in_seconds`` (int): time to run the parallel threads in the test
       | ``number_of_threads`` (int): the number of threads to test with
       | ``log_file`` (str): the file name used

    **Example(s)**:
      
    .. code-block:: python

       test_thread_safe_attribute(
         time_in_seconds=10,
         number_of_threads=100,
         log_file=log_file)

  '''
  # a class to test against
  class A3(metaclass=MetaThreadSafeAttribute):
    _attributes = ['hammed_attribute']

    def __init__(self, a, b, c):
      self.hammed_attribute = 0
      self.a = a
      self.b = b
      self.c = c

  # confirm that normal attributes are working
  a3 = A3(a=1, b=2, c=3)
  assert(a3.a == 1)
  assert(a3.b == 2)
  assert(a3.c == 3)
  # confirm that the thread safe attribute is working as expected from main
  a3.hammed_attribute = 0
  assert(a3.hammed_attribute == 0)
  a3.hammed_attribute += 1
  assert(a3.hammed_attribute == 1)
  a3.hammed_attribute -= 1
  assert(a3.hammed_attribute == 0)

  # begin the multithreaded tests
  # make an event that can turn off all threads
  event = Event()
  event.set()
  # create and start the thread
  for i in range(number_of_threads):
    thread = make_test_thread("thrd_" + "{0:02}:".format(i), a3, event)
    thread.start()

  # let the test run for the desired time
  time.sleep(time_in_seconds)

  # the test is over, open the log file and check the last number in it.
  # this number should always be equal to the last number or greater than the
  # last number. If this is true over the entire file, the test passes
  last_number = 0
  with open(log_file, 'r') as fp:
    for line in fp.readlines():
      print(line, end='')
      current_last = int(line.split(':')[-1])
      assert(current_last >= last_number)
      last_number = current_last

class A2(metaclass=MetaThreadSafeAttribute):
  _attributes = [
    'hammed_attribute1',
    'hammed_attribute2']

  def __init__(self, a, b, c):
    self.hammed_attribute1 = 0
    self.hammed_attribute2 = 0
    self.a = a
    self.b = b
    self.c = c

if __name__ == '__main__':
  a = A1()
  a.name = "bob"
  print(a.name)

  a2 = A2(a=2, b=3, c=4)
  a2.hammed_attribute2 = 1

  test_thread_safe_attribute(
    time_in_seconds=10,
    number_of_threads=100,
    log_file=log_file)


