from itertools import product
import string

_2e32 = pow(2,32)

def hash(password):
  x = 1337
  for c in password:
    x = 33*x + ord(c)
  return x%_2e32

def calcdiff(n):
  x = 25
  for c in range(0, n-1):
    x = 33*x + 25
  return x


def brute(search, cur, n, nmax):
  ndiff = calcdiff(nmax-n+1)
  for key in product(string.lowercase):
    if cur is None:
      key2 = key
    else:
      key2 = cur + key

    if ndiff > _2e32:
      brute(search, key2, n+1, nmax)

    else:
      out = hash(key2 + tuple(('a',) * (nmax-n)))
      diff = (search - out + _2e32)%_2e32
      if diff >= 0 and diff <= ndiff:
        if n < nmax-1:
          brute(search, key2, n+1, nmax)
        else:
          out = hash(key2 + ('a',))
          diff = search - out
          if diff >= 0 and diff <= calcdiff(0):
            lastchr = (chr( ord('a') + diff),)
            print("%s" % (''.join(key2 + lastchr)))


search = 0x45c84173

for i in range(1, 9+1):
  brute(search, None, 1, i)
