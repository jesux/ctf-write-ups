# Hackplayers H-c0n Quals 2020 - Dream Agenda - Exploiting - 332 Points

Aprovechamos una vulnerabilidad en la aplicación que nos permite introducir números negativos.

Obtenemos de la GOT la dirección de *puts* en la libc. Utilizando una base de datos de versiones de libc encontramos que versión se utiliza en el sistema objetivo.

```
./find puts 0x7f8763787690
ubuntu-xenial-amd64-libc6 (id libc6_2.23-0ubuntu10_amd64)
archive-glibc (id libc6_2.23-0ubuntu11_amd64)
```

Obtenemos las direcciones de memoria en la libc de las funciones *atoi* y *system*, y calculamos el offset entre ambas.

```
./dump libc6_2.23-0ubuntu11_amd64 atoi
offset_atoi = 0x0000000000036e80

./dump libc6_2.23-0ubuntu11_amd64 system
offset_system = 0x0000000000045390
```

`offset_atoi_system = 0xe510`

Modificamos en la tabla GOT la dirección a la que apunta la función *atoi* para que apunte a *system*.

[solve.py](solve.py)
