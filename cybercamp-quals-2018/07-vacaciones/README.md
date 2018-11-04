# Cybercamp Quals 2018 - 07. Vacaciones (300 puntos)
### Categoría > Forense


Por orden de un juez, se ha intervenido un equipo en casa de un sospechoso ciberdelincuente, por suerte su portátil aún se encontraba encendido cuando se produjo la detención. Se sabe que ha intentado eliminar pruebas, pero creemos que aún es posible obtener alguna. ¿Cuál era su nick en la red? (Respuesta: flag{NICK}).


#### [Pista 1 Objetivo 7] [35 pts]
Normalmente se suele utilizar cifrado AES en las particiones LUKS.

#### [Pista 2 Objetivo 7] [55 pts]
findaes quizá pueda ayudar a encontrar la clave perdida .

#### [Pista 3 Objetivo 7] [85 pts]
Cryptsetup puede ayudarte a regenerar las cabeceras, para luego recuperar el fichero eliminado. testdisk y photorec son muy utilizadas en el mundo forense.


## Solución


Buscamos la clave AES con la herramienta `findaes`

```bash
findaes dump.elf
Searching dump.elf
Found AES-256 key schedule at offset 0xe414ce8:
0a b4 d6 ef 72 82 6b c6 03 a8 89 9f 32 5b b6 7e 9b 32 41 77 1c fd 03 30 56 9a ce ab 16 f2 51 bd
Found AES-128 key schedule at offset 0xe4158f8:
84 bc d9 8c fc f2 de db 26 06 35 bf ca a9 a4 7d
```

Guardamos la clave en formato binario en el archivo `aeskey`.

```bash
echo 84bcd98cfcf2dedb260635bfcaa9a47d | xxd -r -p > aeskey
```
El archivo `volume.bin` contiene una partición entre los sectores 63 y 16064.

```bash
fdisk -l volume.bin
Disk volume.bin: 64 MiB, 67108864 bytes, 131072 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x00000000

Device      Boot Start   End Sectors  Size Id Type
volume.bin1         63 16064   16002  7.8M 83 Linux
```

Utilizamos la herramienta `dd` para extraer esta partición.

```bash
dd if=volume.bin of=volume2.bin skip=63 count=16002 bs=512
```

```bash
cryptsetup -v luksDump volume2.bin
LUKS header information for volume2.bin

Version:       	1
Cipher name:   	aes
Cipher mode:   	cbc-essiv:sha256
Hash spec:     	sha256
Payload offset:	2048
MK bits:       	128
MK digest:     	81 ab 3d d4 e6 5f b9 38 99 5f d5 63 bf 95 25 f8 f7 5a 56 a9
MK salt:       	43 83 7c 4b 01 94 7d 2a bb 37 c2 6a 8d a4 6b 85
               	1b 45 23 bb ed 67 dd a8 c0 72 3e d9 e1 9d 8e ff
MK iterations: 	74983
UUID:          	85a77307-ea74-4495-932d-3fb25323edfd

Key Slot 0: ENABLED
	Iterations:         	1199742
	Salt:               	3d 1b 35 0f e5 46 c6 cc 51 72 0f 2c b3 9e fe 4e
	                      	05 88 ce 14 73 43 43 80 a0 29 ce 95 85 fd 34 2b
	Key material offset:	8
	AF stripes:            	4000
Key Slot 1: DISABLED
Key Slot 2: DISABLED
Key Slot 3: DISABLED
Key Slot 4: DISABLED
Key Slot 5: DISABLED
Key Slot 6: DISABLED
Key Slot 7: DISABLED
Command successful.
```

Desciframos el volumen y lo montamos.

```bash
cryptsetup -v --master-key-file aeskey luksOpen volume2.bin bHDD
mount /dev/mapper/bHDD /mnt/volume/
```

Nos encontramos con que una vez montado el volumen no contiene ningun archivo.

Realizamos una copia del volumen descifrado a un archivo. Aunque esto no es estrictamente necesario, es mas facil trabajar con un archivo.

```bash
dd if=/dev/mapper/bHDD of=luks.bin
```

La herramienta `binwalk` nos revela la existencia de un archivo ZIP, sin embargo esta herramienta no es capaz de extraer el archivo correctamente.

```bash
binwalk luks.bin
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
114176        0x1BE00         Zip archive data, encrypted at least v1.0 to extract, compressed size: 38, uncompressed size: 26, name: secret.txt
114378        0x1BECA         End of Zip archive
```

La herramienta `photorec` no detecta el archivo ZIP, por lo que usamos `foremost`.

```bash
foremost luks.bin
Processing: luks.bin
|foundat=secret.txtUT
*|
```

Una vez tenemos el archivo zip, utilizamos `john` para crackear la contraseña.

```bash
zip2john 00000223.zip
00000223.zip:$pkzip2$1*2*2*0*26*1a*abce94d7*0*44*0*26*abce*ab6c*14fab29fabf746766d7f7af67ddc8b7229c5c96fc973db3da79ecb9789f12d0a57209f6b44cf*$/pkzip2$:::::00000223.zip
```

```bash
john ziphash
iloveyou         (00000223.zip)
```

```bash
unzip 00000223.zip
Archive:  00000223.zip
[00000223.zip] secret.txt password:
 extracting: secret.txt
```

```bash
 cat secret.txt
_z3r0.c00l!_ was here! :)
```

Flag: `flag{_z3r0.c00l!_}`
