# Cybercamp Quals 2018 - 12. Seguridad Nacional (500 puntos)
### Categoría > Forense


Se te proporciona un fichero de tráfico de red el cual contiene comunicaciones entre dos sospechosos de terrorismo. Tu objetivo, ver qué información están intercambiando y obtener la FLAG.

#### [Pista 1 Objetivo 12] [50 pts]
Los sospechosos se han transmitido un fichero relevante.

#### [Pista 2 Objetivo 12] [90 pts]
Han eliminado los datos relevantes.

#### [Pista 3 Objetivo 12] [150 pts]
La Madre de Fernando Torres puede ser de ayuda para recuperarlos.


## Solución

El primer paso es crackear el archivo ZIP y obtener su contenido. Omitimos este paso al haberse realizado ya varias veces durante este mismo CTF.

Pass: `cyberhacker`

Obtenemos una imagen de disco `diskimage` con una particion *NTFS*.

```bash
file diskimage
diskimage: DOS/MBR boot sector MS-MBR Windows 7 english at offset 0x163 "Invalid partition table" at offset 0x17b "Error loading operating system" at offset 0x19a "Missing operating system", disk signature 0xa54645b7; partition 1 : ID=0x7, start-CHS (0x0,2,3), end-CHS (0x3b,0,48), startsector 128, 59392 sectors
```

```bash
fdisk -l diskimage
Disk diskimage: 32 MiB, 33554432 bytes, 65536 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xa54645b7

Device     Boot Start   End Sectors Size Id Type
diskimage1        128 59519   59392  29M  7 HPFS/NTFS/exFAT
```

```bash
mount -t ntfs-3g -o offset=65536,ro diskimage /mnt/a/
```

Dentro de la partición no encontramos ningún archivo interesante.

Usamos la herramienta `ntfsundelete`, pero para ello antes extraemos la partición NTFS con `dd`.

```bash
dd if=diskimage of=diskimage1 skip=128 count=59392
```

```bash
ntfsundelete diskimage1
Inode    Flags  %age     Date    Time       Size  Filename
-----------------------------------------------------------------------
16       F..!     0%  1970-01-01 01:00         0  <none>
21       F..!     0%  1970-01-01 01:00         0  <none>
22       F..!     0%  1970-01-01 01:00         0  <none>
23       F..!     0%  1970-01-01 01:00         0  <none>
77       FN..   100%  2018-06-19 10:36     61440  flag.png
78       FR..   100%  2018-06-19 11:17       170  top_secret.7z
79       FN..   100%  2018-06-19 10:37   2097152  top_secret.db
80       D...     0%  2018-06-19 10:34         0  docs
81       FN..   100%  2017-12-06 17:24      8084  Makefile
...
```

Extraemos el archivo `top_secret.7z`

```bash
ntfsundelete -u -i 78 diskimage1
Undeleted 'top_secret.7z' successfully.
```

Este archivo esta protegido por contraseña, en primer luegar probamos con nuestro diccionario, pero al no encontrar resultado debemos buscar en el contenido del disco.

En el disco se encuentra un archivo parcialmente sobrescrito con la contraseña del archivo.

```
7z file
nR3qrtp2(Yu8Y5ph


bank login
t0wt0w
```

Flag: `secretmilitarybasecoords`
