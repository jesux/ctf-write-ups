from itertools import product
import string

def hash(password):
  x = 1337
  for c in password:
    x = 33*x + ord(c)
  return x%pow(2,32)


search = 0x45c84173

for key1 in product(string.lowercase, repeat=3):
  out = hash(key1 + ('a','a','a','a','a','a'))
  diff = (search - out + 4294967296)%4294967296
  if diff >= 0 and diff <= 1008959350:
    for key2 in product(string.lowercase):
      out = hash(key1 + key2 + ('a','a','a','a','a'))
      diff = (search - out + 4294967296)%4294967296
      if diff >= 0 and diff <= 30574525:
        for key3 in product(string.lowercase):
          out = hash(key1 + key2 + key3 + ('a','a','a','a'))
          diff = (search - out + 4294967296)%4294967296
          if diff >= 0 and diff <= 926500:
            for key4 in product(string.lowercase):
              out = hash(key1 + key2 + key3 + key4 + ('a','a','a'))
              diff = (search - out + 4294967296)%4294967296
              if diff >= 0 and diff <= 28075:
                for key5 in product(string.lowercase):
                  out = hash(key1 + key2 + key3 + key4 + key5 + ('a','a'))
                  diff = (search - out + 4294967296)%4294967296
                  if diff >= 0 and diff <= 850:
                    for key6 in product(string.lowercase):
                      out = hash(key1 + key2 + key3 + key4 + key5 + key6 + ('a',))
                      diff = (search - out + 4294967296)%4294967296
                      if diff >= 0 and diff <= 25:
                        lastchar = (chr( ord('a') + diff),)
                        print("%s" % (''.join(key1 + key2 + key3 + key4 + key5 + key6 + lastchar)))