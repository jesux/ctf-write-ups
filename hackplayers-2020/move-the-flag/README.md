# Hackplayers H-c0n Quals 2020 - Mov(e) the flag - Reversing - 374 Points

El binario esta ofuscado utilizando [movfuscator](https://github.com/xoreaxeaxeax/movfuscator)

Adaptamos el script de este writeup <https://github.com/guyinatuxedo/ctf/tree/master/other/rev/movfuscated1>

Utilizamos `perf` para contar el número de instrucciones en cada ejecución del proceso.
La principal diferencia con el otro reto, es que antes de comprobar cada caracter de la flag, se comprueba que la longitud sea de 39.

[solve.py](solve.py)

### Get flag length
```
[+] 29 - 150164
[+] 30 - 150165
[+] 31 - 150165
[+] 32 - 150165
[+] 33 - 150166
[+] 34 - 150164
[+] 35 - 150165
[+] 36 - 150164
[+] 37 - 150167
[+] 38 - 150162
[+] 39 - 163962
FLAG LENGTH: 39
```

### Get flag
```
[+] 0 - 686015
[+] 1 - 686015
[+] 2 - 708714
[+] 3 - 686017
[+] 4 - 686015
[+] 5 - 686016
[+] 6 - 686016
[+] 7 - 686016
[+] 8 - 686018
[+] 9 - 686016
[+] a - 686015
[+] b - 686016
[+] c - 686016
[+] d - 686017
[+] e - 686015
[+] f - 686017
[+] } - 686015
RESULT: H-c0n{bdd0fbdbefa8e89f42
```

`H-c0n{bdd0fbdbefa8e89f421140836280a568}`