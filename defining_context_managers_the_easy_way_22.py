# you want to implement new kinds of context manager for use with the "with"
# statement

import time
from contextlib import contextmanager

@contextmanager
def timethis(label):
  start = time.time()
  try:
    yield
  finally:
    end = time.time()
    print('{}: {}'.format(label, end-start))

# Example use:
with timethis('counting'):
  n = 10000000
  while n > 0:
    n -= 1


