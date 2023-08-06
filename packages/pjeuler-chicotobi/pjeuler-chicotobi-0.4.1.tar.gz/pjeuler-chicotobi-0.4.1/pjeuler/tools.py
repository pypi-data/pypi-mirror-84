import numpy as np	
import math
import collections
import functools

def fib(n):
  arr = [1,1]
  for i in range(n-2):
    arr = arr+[arr[-2]+arr[-1]]
  return arr[0:n]


def primes(n):   
    l = np.ones((n,1))
    l[0] = 0
    next_prime = np.where(l==1)[0]
    while next_prime.size:
      incr = next_prime[0]+1
      print(incr)
      l[incr-1] = 2
      l[np.arange(2*incr-1,n,incr)]=0
      next_prime = np.where(l==1)[0]
    return np.where(l==2)[0]+1


def factors(m):
    n = math.floor(m**.5)
    l = np.ones((n,1))
    l[0] = 0
    f = []
    tmp = np.where(l==1)[0]
    while tmp.size:
      prime = tmp[0]+1
      while m%prime==0:
          m /= prime
          f.append(prime)
      if(m==1):
        break
      l[prime-1] = 2
      l[np.arange(2*prime-1,n,prime)]=0
      tmp = np.where(l==1)[0]
    if m != 1:
        f.append(int(m))
    return f


def is_palindrome(n):
    return str(n)==str(n)[::-1]


def lcm(*args):
    if len(args)>1:
        args = list(args)
    else:
        args = args[0]
    l = [collections.Counter(factors(x)) for x in args]
    r = functools.reduce(lambda a,b:a|b,l)
    return np.prod([x**y for (x,y) in r.items()])


def gcd(*args):
    if len(args)>1:
        args = list(args)
    else:
        args = args[0]
    l = [collections.Counter(factors(x)) for x in args]
    r = functools.reduce(lambda a,b:a&b,l)
    return np.prod([x**y for (x,y) in r.items()])