from itertools import product
import string

def hash(password):
  x = 1337
  for c in password:
    x = 33*x + ord(c)
  return x%pow(2,32)


search = 0x45c84173

for key6 in product(string.lowercase, repeat=6):
  diff = search - hash(key6 + ('a','a','a'))
  if diff >= 0 and diff <= 28076:
    for key3 in product(string.lowercase, repeat=3):
      if hash(key6 + key3) == search:
        print("%s" % (''.join(key6+key3)))
        break
