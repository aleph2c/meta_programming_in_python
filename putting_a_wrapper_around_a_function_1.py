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
  countdown(1000000)
  countdown(10000000)
  countdown(100000000)
  
