# CTF ASIS QUALS 2015 - Simple Algorithm

## simple_algorithm.py

```python
#!/usr/bin/python

flag = '[censored]'
hflag = flag.encode('hex')
iflag = int(hflag[2:], 16)

def FAN(n, m):
    i = 0
    z = []
    s = 0
    while n > 0:
    	if n % 2 != 0:
    		z.append(2 - (n % 4))
    	else:
    		z.append(0)
    	n = (n - z[i])/2
    	i = i + 1
    z = z[::-1]
    l = len(z)
    for i in range(0, l):
        s += z[i] * m ** (l - 1 - i)
    return s

i = 0
r = ''
while i < len(str(iflag)):
    d = str(iflag)[i:i+2]
    nf = FAN(int(d), 3)
    r += str(nf)
    i += 2

print r
```

## enc.txt
```
2712733801194381163880124319146586498182192151917719248224681364019142438188097307292437016388011943193619457377217328473027324319178428
```

## Script simple_algorithm

La primera parte del script convierte el string de la flag en su equivalente en número entero. En esta conversión se pierde el primer carácter de la flag, pero no nos supone un problema al conocer el formato de flag `ASIS{...}`.

Una vez convertido en entero, se llama a la función FAN con trozos de 2 números y se concatena el resultado.

## Función FAN

En otros writeups de este mismo reto se programa la función inversa a FAN. Una solución mas sencilla y rápida es generar una lista con los 100 valores que toma la función FAN.

```python
values = {}
for x in range(0,100):
    nf = FAN(int(x), 3)
    values[str(nf)] = x
```

La función FAN recibe un número del 0 al 99 y genera un número de 1 a 4 dígitos.

```
0 0
1 1
2 3
3 8
4 9
5 10
6 24
...
97 1945
98 1947
99 1952
```

## Colisiones

Debido a como funciona la función FAN, la salida de esta no tiene una longitud fija, lo que nos dificulta recuperar la flag original.

Es posible solucionar este problema de 2 formas distintas.

La mas sencilla es procesar los números desde el final al principio, de esta forma se evitan la mayoría de colisiones.

La forma compleja, pero mas adecuada, es guardar el historial de acciones realizadas y volver hacia atrás cuando se llega a un punto muerto.

```python
i = 0
estados = []
out = []
fail = None
while i < len(enc):
    for l in [4,3,2,1]:
        if fail!=None and l>=fail: continue
        nf = enc[i:i+l]
        if nf in values:
            fail = None
            estados.append((i,l))
            i += l
            out.append("%02d" % int(values[nf]))
            break
    else:
        (i,fail) = estados.pop()
        out.pop()
```

El ultimo problema que se nos presenta ocurre cuando el ultimo número que se le pasa la función FAN en el momento de codificar es de un solo dígito. Ocurre que al reversear el algoritmo, el ultimo elemento que obtenemos es `09`, que en realidad es únicamente `9`.

```python
if out[-1][0]=='0':
    out[-1] = out[-1][1]
```

[solve.py](https://github.com/jesux/ctf-write-ups/blob/master/asis-quals-2015/simple-algorithm/solve.py)

Por último, obtenemos parte de la flag, y al añadir el primer caracter queda `ASIS{a9ab115c488a311896dac4e8bc20a6d7}`