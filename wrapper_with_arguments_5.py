# Definining a Decorator with User Adjustable Attributes
from functools import wraps, partial 
import logging
logging.basicConfig(level=logging.DEBUG)

# func = decorator(x, y, z)(func)
# so this given wrapper, returns a function, then it calls this function again
# with func..
# 
# On the first call obj is baked into the function that it is accessible
# on the next call.
# 
# The obj (which is the wrapper below) is
# provided as the first argument... and the function is assigned as
# an attribute of this function, then the function is returned
def attach_wrapper(obj, func=None):
  if func is None:
    return partial(attach_wrapper, obj)
  setattr(obj, func.__name__, func)
  return func

def logged(level, name=None, message=None):
  '''
  Add logging to a function.  level is the logging
  level, name is the logger name, and message is the
  log message.  If name and message aren't specified,
  they default to the funtion's module and name.
  '''
  def decorate(func):
    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
      log.log(level, logmsg)
      return func(*args, **kwargs)

    # attach setter functions
    @attach_wrapper(wrapper)
    def set_level(new_level):
      nonlocal level  # reaches out
      level = new_level

    @attach_wrapper(wrapper)
    def set_message(newmsg):
      nonlocal logmsg  # reaches out
      logmsg = newmsg

    return wrapper
  return decorate

# example use
@logged(logging.DEBUG)
def add(x, y):
  return x + y

@logged(logging.CRITICAL, 'example')
def spam():
  print('spam')

if __name__ == '__main__':
  add(2, 3)

  add.set_message('Add called')
  add(2, 3)

  add.set_level(logging.WARNING)
  add(2, 3)


