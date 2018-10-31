# CTF ECSC 2016

![](img/logo.png)

## Description
The Decepticons are planning their next attack wave. But we have intercepted their encrypted message and part of Megatrons private key. Optimus says, he could decrypt the message easily. Can you as well!

## Requirements
Please get the provided ZIP file containing the following files:
* Public-key: [my.pub](files/my.pub)
```
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC6zfbJ9sS8/aFfQe9TxDbZWLy5
nsq9ECmTO9XGEPLrPNitjF6dpJLS5FpU+nXpinbsqmPont5I156gDGPUxeBzd5o8
T6kUnMGErnqX2Yu64L4Pw59Fap8coGpHHg2VIP7H1keUA8quNboiG58OnPtSW1zh
hKv3pIiwFPsLQkNBKQIDAQAB
-----END PUBLIC KEY-----
```
* Keyparts of the private key: [key.parts](files/key.parts)
```
-----BEGIN RSA PRIVATE KEY-----
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
HlNb/M95n4zO2tk0V53/hxwWZrAgoBsDNQJBALHlrJ5D1TxPy8JQHyaVP48SRWuK
xQBk3F5nqikVEZiGFZ/SeAgCSxKovU5pH0reRlHhZJX+Abrugr6TYKFzwpkCQEx+
6vU1nu4MCIxmC99fOx+ZOaGMKHhzwgkl1VQ8U2GqxuFCXcqmJ8fIolmsLRWaoZ/y
qNL4cCu+KoNbB9KGym0CQAt2Qs77w3Iny+JPRpsbbQSQoyP2YhbXXFBwVmdYbNrA
fT4RcpUCfOennMmpG77xkWB6UFOu0WBH8eX+OtaSfFY=
-----END RSA PRIVATE KEY-----
```
* Secret file: [secret](files/secret)

## Goal
Decrypt the secret message!

## Gold Nugget
“A...!”



## Introducción

En esta prueba nos piden descifrar el contenido del archivo secret. A primera vista vemos que se ha utilizado el algoritmo RSA y nos dan la clave publica completa, y parte de la clave privada.

Nuestro primer objetivo será obtener la clave privada.


## RSA


Empecemos por un poco de teoría, [RSA](https://es.wikipedia.org/wiki/RSA) es un algoritmo de [cifrado asimetrico](https://es.wikipedia.org/wiki/Criptograf%C3%ADa_asim%C3%A9trica) por tanto se utiliza una clave publica y una clave privada.

El funcionamiento de RSA se basa en números primos, y la seguridad radica en la dificultad de factorización de un número entero lo suficientemente grande.

Resumiendo, en RSA la clave privada la forman 2 números primos, y la clave publica esta formada por el producto de estos 2 números primos.

## Clave pública

```bash
# openssl rsa -in my.pub -pubin -text -noout
Public-Key: (1024 bit)
Modulus:
    00:ba:cd:f6:c9:f6:c4:bc:fd:a1:5f:41:ef:53:c4:
    36:d9:58:bc:b9:9e:ca:bd:10:29:93:3b:d5:c6:10:
    f2:eb:3c:d8:ad:8c:5e:9d:a4:92:d2:e4:5a:54:fa:
    75:e9:8a:76:ec:aa:63:e8:9e:de:48:d7:9e:a0:0c:
    63:d4:c5:e0:73:77:9a:3c:4f:a9:14:9c:c1:84:ae:
    7a:97:d9:8b:ba:e0:be:0f:c3:9f:45:6a:9f:1c:a0:
    6a:47:1e:0d:95:20:fe:c7:d6:47:94:03:ca:ae:35:
    ba:22:1b:9f:0e:9c:fb:52:5b:5c:e1:84:ab:f7:a4:
    88:b0:14:fb:0b:42:43:41:29
Exponent: 65537 (0x10001)
```

Convertimos el numero a decimal
```
n = 131178613911428433274564590768469109412256238466895565623112738296405357018269420980173329763468887678203068746581497153939540144978113996740173055353905750486822971628851441565420624628795519630030170400764800669166654557089792442549757770719898745350512819900979210083766185632402450686583976608686892335401
e = 65537
```

Una vez obtenido `n` podriamos probar a factorizarlo, ya sea con herramientas como [YAFU](https://sourceforge.net/projects/yafu/), o en la base de datos de [factordb](http://factordb.com/). La solución aparece en factordb debido a que fue subida al terminar el CTF. <http://factordb.com/index.php?id=1100000000874962407>


## Clave privada

### PEM vs DER
Las formas mas comunes de codificar un certificado o clave RSA son los formatos PEM y DER.
* DER: Los datos se guardan directamente en binario.
* PEM: Los datos están en base64, con el prefijo `-----BEGIN`

Ademas, estos datos se representan utilizando [ASN1](https://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One#Example_encoded_in_DER)

```
RSAPrivateKey ::= SEQUENCE {
  version           Version,
  modulus           INTEGER,  -- n
  publicExponent    INTEGER,  -- e
  privateExponent   INTEGER,  -- d
  prime1            INTEGER,  -- p
  prime2            INTEGER,  -- q
  exponent1         INTEGER,  -- d mod (p-1)
  exponent2         INTEGER,  -- d mod (q-1)
  coefficient       INTEGER,  -- (inverse of q) mod p
  otherPrimeInfos   OtherPrimeInfos OPTIONAL
}
```

### Decodificar clave privada

Lo primero es comprobar si la parte en base64 es correcta y convertirla. El comando 'base64' de linux informa de cuando la conversión no es válida con el mensaje `base64: invalid input`. En el caso de que obtuviéramos un error en la conversión, deberíamos añadir de 1 a 3 caracteres 'A' al principio de la cadena en base64 (o eliminar de 1 a 3 caracteres al principio), luego en la salida tendriamos que tener en cuenta que los 3 primeros bytes no serían correctos.

```bash
# echo 'HlNb/M95n4zO2tk0V53/hxwWZrAgoBsDNQJBALHlrJ5D1TxPy8JQHyaVP48SRWuKxQBk3F5nqikVEZiGFZ/SeAgCSxKovU5pH0reRlHhZJX+Abrugr6TYKFzwpkCQEx+6vU1nu4MCIxmC99fOx+ZOaGMKHhzwgkl1VQ8U2GqxuFCXcqmJ8fIolmsLRWaoZ/yqNL4cCu+KoNbB9KGym0CQAt2Qs77w3Iny+JPRpsbbQSQoyP2YhbXXFBwVmdYbNrAfT4RcpUCfOennMmpG77xkWB6UFOu0WBH8eX+OtaSfFY=' \
|base64 -d \
|xxd
00000000: 1e53 5bfc cf79 9f8c ceda d934 579d ff87
00000010: 1c16 66b0 20a0 1b03 3502 4100 b1e5 ac9e
00000020: 43d5 3c4f cbc2 501f 2695 3f8f 1245 6b8a
00000030: c500 64dc 5e67 aa29 1511 9886 159f d278
00000040: 0802 4b12 a8bd 4e69 1f4a de46 51e1 6495
00000050: fe01 baee 82be 9360 a173 c299 0240 4c7e
00000060: eaf5 359e ee0c 088c 660b df5f 3b1f 9939
00000070: a18c 2878 73c2 0925 d554 3c53 61aa c6e1
00000080: 425d caa6 27c7 c8a2 59ac 2d15 9aa1 9ff2
00000090: a8d2 f870 2bbe 2a83 5b07 d286 ca6d 0240
000000a0: 0b76 42ce fbc3 7227 cbe2 4f46 9b1b 6d04
000000b0: 90a3 23f6 6216 d75c 5070 5667 586c dac0
000000c0: 7d3e 1172 9502 7ce7 a79c c9a9 1bbe f191
000000d0: 607a 5053 aed1 6047 f1e5 fe3a d692 7c56
```

Ahora viene la parte algo mas tediosa, debido a que tenemos solo parte de la clave, los decodificadores automaticos de ASN1 no identifican los elementos, por lo que deberemos hacerlo a mano.

Lo primero es identificar los bytes con '02' que determinan el inicio de un elemento. El primero se encuentra en el byte 26.

El siguiente byte es 0x41, lo que indica que los siguientes 65 bytes forman parte de ese elemento. Seguidamente tenemos otro byte '02' seguido de 0x40, repetimos el mismo proceso y nos quedamos con los 64 bytes siguientes. Por ultimo otra vez tenemos otro elemento también de 64 bytes.


```
prime2
... 1e535bfccf799f8ccedad934579dff871c1666b020a01b0335

exponent1
0241 00b1e5ac9e43d53c4fcbc2501f26953f8f12456b8ac50064dc5e67aa2915119886159fd27808024b12a8bd4e691f4ade4651e16495fe01baee82be9360a173c299
dp = 9317230555533003184594563259109694707596614327146138666703649935877055729203242875279069935567209487505831328441244886222704237470751403936551032289739417

exponent2
0240 4c7eeaf5359eee0c088c660bdf5f3b1f9939a18c287873c20925d5543c5361aac6e1425dcaa627c7c8a259ac2d159aa19ff2a8d2f8702bbe2a835b07d286ca6d
dq = 4006408700946313574129254108070537891459032408758698413850128951471164074309142647658423982431577412561002034667831521677333834921593924180515292197603949

coefficient
0240 0b7642cefbc37227cbe24f469b1b6d0490a323f66216d75c50705667586cdac07d3e117295027ce7a79cc9a91bbef191607a5053aed16047f1e5fe3ad6927c56
qinv = 600311393936749309456263364056664123433762703229653947738301787668727059286270010747766114963444360392903962802634972566162421580254127364574025918610518

``` 

El mismo proceso manual se puede realizar con este [script](https://github.com/p4-team/ctf/tree/master/2016-03-12-0ctf/equation)

```python
#!/usr/bin/env python3
from base64 import b64decode

def get_dp_dq_qinv(key64):
    result = []
    key_tab = list(b64decode(key64))
    print(key_tab)
    i = 0
    while i < len(key_tab):
        x = key_tab[i]
        if x == 0x2:  # integer start
            length = key_tab[i + 1]
            octets = key_tab[i + 2: i + 2 + length]
            value = int.from_bytes(octets, byteorder="big")
            result.append(value)
            print(value)
            i += 2 + length
        else:
            i += 1
    return tuple(result)

dp, dq, qinv = get_dp_dq_qinv(key64)
``` 

### Obtener p y q

Aunque este reto es posible resolverlo sin conocer la clave publica `n`, tenerla simplifica los calculos al no tener que comprobar si los posibles candidatos son un numeros primos, simplemente hay que comprobar si el candidato es un factor de `n`.


```python
def is_factor(num, n):
  if num < 2 or num%2 == 0: return False
  if num%3 == 0: return False
  return (((n/num)*num)==n)

def recover_parameters(dp, dq, qinv, e, n):
    d1p = dp * e - 1
    for k in range(3, e):
        if d1p % k == 0:
            hp = d1p // k
            p = hp + 1
            if is_factor(p, n):
                q = n / p
                if (qinv * q) % p == 1 or (qinv * p) % q == 1:
                    return (p, q)
    return results

p, q = recover_parameters(dp, dq, qinv, e, n)
print("p: %lu" % p)
print("q: %lu" % q)
```

```
p = 12409530116611113069722673907902939927077171750562461687594137012713380508978436132121375571419505917625282847052267327325475909667939575657231740096180389
q = 10570796208942330718133134445050881347580442327501864726780301183323228790933543286750277085897914122428857455856744411456476812241092677201917577388557109
```

### Generar clave privada completa

Con la herramienta [rsatool.py](https://github.com/ius/rsatool) podemos generar un nuevo archivo de clave privada conociendo p, q, e.

```bash
# rsatool.py -p 12409...80389 -q 10570...57109 -o key && cat key
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQC6zfbJ9sS8/aFfQe9TxDbZWLy5nsq9ECmTO9XGEPLrPNitjF6dpJLS5FpU+nXp
inbsqmPont5I156gDGPUxeBzd5o8T6kUnMGErnqX2Yu64L4Pw59Fap8coGpHHg2VIP7H1keUA8qu
NboiG58OnPtSW1zhhKv3pIiwFPsLQkNBKQIDAQABAoGAahRL8KSRVEEzQkTPA2KJQyOBCGeD+ZkU
AugXnUJCsBL9eJAdqqeqONgz883G57gZkIux8IdG81Z+XaSrjEhSDEbUiEujCc81POFXTmfpB0mu
dsAlchH7aWs/910Enj9l9l1j+jNfuC2xZeH3B36f7xrjviZu6OvGKHNCyDKWTgECQQDs8IUKgFCU
MlyYxN/p9rrL48NDf+9o4lFdeGw35JXyngEXkX7iSMpNtI/WaZnnXlm2+X0eqCr/0wmMGMKlB3Cl
AkEAydT5vs7PIlHhRVZMTWmINQ+QoyXQc+MgZvrcrkb3Oq0CJ4cI3Rd+HlNb/M95n4zO2tk0V53/
hxwWZrAgoBsDNQJBALHlrJ5D1TxPy8JQHyaVP48SRWuKxQBk3F5nqikVEZiGFZ/SeAgCSxKovU5p
H0reRlHhZJX+Abrugr6TYKFzwpkCQEx+6vU1nu4MCIxmC99fOx+ZOaGMKHhzwgkl1VQ8U2GqxuFC
XcqmJ8fIolmsLRWaoZ/yqNL4cCu+KoNbB9KGym0CQAt2Qs77w3Iny+JPRpsbbQSQoyP2YhbXXFBw
VmdYbNrAfT4RcpUCfOennMmpG77xkWB6UFOu0WBH8eX+OtaSfFY=
-----END RSA PRIVATE KEY-----
```

## Descifrar secret

```bash
# openssl rsautl -decrypt -in secret -out secret.txt -inkey key && cat secret.txt
{All H4il M3gatr0n! Def3at Otpimu$ -> W0rld Dom1nation!}
```

## Enlaces
* <https://github.com/p4-team/ctf/tree/master/2016-03-12-0ctf/equation>
* <http://cseweb.ucsd.edu/~hovav/dist/reconstruction.pdf>
* <https://github.com/ctfs/write-ups-2014/tree/master/plaid-ctf-2014/rsa>
* <https://0day.work/0ctf-2016-quals-writeups/>