import numpy as np	

def fib(n):
  arr = [1,1]
  for i in range(n-2):
    arr = arr+[arr[-2]+arr[-1]]
  return arr[0:n]
