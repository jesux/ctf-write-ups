# Hackplayers H-c0n Quals 2020 - Kojo No Mai - Crypto - 200 Points

Como ennciado del reto tenemos una clave pública de RSA y textos cifrados y codificados en base64.

```
-----BEGIN PUBLIC KEY-----
MCwwDQYJKoZIhvcNAQEBBQADGwAwGAIRAOSpZLB7VXE7iZA72YTS85UCAwEAAQ==
-----END PUBLIC KEY-----

XnZvSmNqZqz+N5LL+ec6XA==
k4TD9AHouSlxdn97PXfmOg==
FhHp7W1orCt78mlz5PNGBQ==
a5FPpzeDX29qOriH2kS64A==
XCWOYhWFC6v3wa3qM58v5g==
qlLYhsaMWbOvCXddqsQ/pA==
i1jClSfyTf8XLiT57Su6IQ==
DZbTy4vMKW0WqjrD7CspMg==
```

Con *openssl* obtenemos los parámetros de la clave privada RSA.

```bash
openssl rsa -in pub -pubin -text -noout

RSA Public-Key: (128 bit)
Modulus:
    00:e4:a9:64:b0:7b:55:71:3b:89:90:3b:d9:84:d2:
    f3:95
Exponent: 65537 (0x10001)
```

`n = 0x00e4a964b07b55713b89903bd984d2f395 = 303943523431340122197231114949456229269`

Factorizamos este número, en este caso utilizamos <factordb.com>.

`303943523431340122197231114949456229269<39> = 16894353763414259897<20> · 17990834552639007677<20>`


Desciframos con RSA cada uno de los trozos, observamos que solo los últimos 5 caracteres de cada trozo forman parte de la flag.

```python
import gmpy
from base64 import b64decode

n = 0x00e4a964b07b55713b89903bd984d2f395
p = 16894353763414259897
q = 17990834552639007677
e = 65537

assert p*q==n

phi = (p - 1) * (q - 1)
d = int(gmpy.invert(e, phi))
#d = 294756161789557849827579195158651733121

cc = ''
for c64 in ['XnZvSmNqZqz+N5LL+ec6XA==', 'k4TD9AHouSlxdn97PXfmOg==', 'FhHp7W1orCt78mlz5PNGBQ==', 'a5FPpzeDX29qOriH2kS64A==', 'XCWOYhWFC6v3wa3qM58v5g==', 'qlLYhsaMWbOvCXddqsQ/pA==', 'i1jClSfyTf8XLiT57Su6IQ==', 'DZbTy4vMKW0WqjrD7CspMg==']:
	c = int(b64decode(c64).encode('hex'), 16)
	m = pow(c,d,n)
	mh = hex(m)[2:-1]
	if len(mh)%2==1:
		mh = '0' + mh
	cc += mh.decode('hex')[-5:]

print(cc)
```

`H-c0n{1aa36c2eb49a2f427e57c715bda839e6}`
