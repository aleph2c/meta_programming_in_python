# Preserving function metadata
import time
from functools import wraps
from inspect import signature

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
def countdown(n:int):
  '''counts down'''
  while n > 0:
    n -= 1


if __name__ == '__main__':
  countdown(100000)
  print(countdown.__name__)
  print(countdown.__doc__)
  print(countdown.__annotations__)
  print(signature(countdown)) 
