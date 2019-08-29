# Unwrapping a decorator
import time
from functools import wraps

def timethis(fn):
  '''decorator that reports the execution time'''
  @wraps(fn)
  def wrapper(*args, **kwargs):
    start = time.time()
    result = fn(*args, **kwargs)
    end = time.time()
    print(fn.__name__, end-start)
    return result
  return wrapper

@timethis
def countdown(n):
  '''counts down'''
  while n > 0:
    n -= 1


if __name__ == '__main__':
  countdown(100000)
  # the __wrapped__ attribute will strip off all decorators
  # from the function and return the original function

  # This __wrapped__ feacture only works if the @wrapped wrapper
  # was used within the decorator
  orginal_countdown = countdown.__wrapped__
  orginal_countdown(100000)

