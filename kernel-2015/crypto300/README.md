# Kernel 2015 - Crypto 300

Para esta prueba tenemos 54 archivos de cartas con los siguientes números ordenados

```
48  52  B  09  10  11  51  16  20  21  14  06  26  27  28  05  08  33  34  35  36  37  38  39  40  41  42  43  44  45  13  30  25  29  15  A  50  12  07  31  32  04  17  46  47  03  22  23  24  49  01  18  19  02
```

La clave a descifrar es `HBCNC DKARI OFVIC DISQ`

Después de investigar llegamos a la conclusión de que nos encontramos ante el [cifrado Solitario](https://en.wikipedia.org/wiki/Solitaire_(cipher)) de la novela [Cryptonomicon](https://en.wikipedia.org/wiki/Cryptonomicon)

Utilizamos este script de *Python* [https://www.schneier.com/code/sol.py] y lo modificamos para introducir el orden de nuestra baraja. Los comodines A y B los sustituimos por ’53’ y ’54’

```python
deck = [48, 52, 54, 9, 10, .... 18, 19, 2]
```

El resultado obtenido es `XBDQDVHLVQCJDNWQJLV`

En este caso no hemos obtenido el mensaje correcto.

Después de probar distintas combinaciones y verificar que el algoritmo fuera correcto se encontró la solución utilizando el script con la baraja inicial ordenada

```python
deck = [1, 2, 3,  .... 52, 53, 54]
```

El mensaje es **DESPUESUNBUSCAMINAS**

Una vez encontrada la solución, podemos observar como lo que nos ofrecía la prueba es el orden de la baraja después de cifrar el texto y simplemente hemos tenido suerte al encontrar la solucion con una baraja ordenada.

Para resolver correctamente la prueba, necesitamos invertir el proceso de cifrado y reordenado de la baraja.
Para ello he modificado el script inicial con esta nueva opción.

[solitaire-inverse.py](https://gist.github.com/jesux/0a2d243b3fdcc8827adf)
