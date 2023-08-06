import numpy as np
from . import tools

def pjeuler1():
  val = 0
  for i in range(1000):
    if i%3 == 0 or i%5 == 0:
      val += i
  return val

def pjeuler2():
  arr = np.array(fib(40))
  arr = arr[arr%2==0]
  return sum(arr[arr<4e6])
