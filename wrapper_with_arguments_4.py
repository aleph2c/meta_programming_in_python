# Defining a Decorator that takes arguments
from functools import wraps
import logging

# Without the following line, nothing will show up.
# the basicConfig must be called before using the logger
logging.basicConfig(level=logging.DEBUG)

def logged(level, name=None, message=None):
  '''
  Add logging to a function.  level is the logging
  level, name is the logger name, and message is the
  log message.  If name and message aren't specified,
  they default to the funtion's module and name.
  '''
  def decorate(func):
    logname = name if name else func.__module__
    # the getLogger creates a name which will appear in the log stream
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
      log.log(level, logmsg)
      return func(*args, **kwargs)
    return wrapper
  return decorate

# example use
@logged(logging.DEBUG)
def add(x, y):
  return x + y

@logged(logging.CRITICAL, 'example')
def spam():
  print('Spam!')

if __name__ == '__main__':
  add(1, 2)
  spam()
