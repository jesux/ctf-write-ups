# CTF FWHIBBIT 2017 - Wash your money

En esta prueba tenemos una pagina con diferentes funcionalidades, una de ellas nos permite subir archivos *.doc* o *.docx*.

![](img/01-web.png)

![](img/02-contact.png)

![](img/03-upload.png)

Si intentamos evadir los filtros y subir otro tipo de archivo nos aparece un mensaje con el texto *Not a valid file*.

![](img/04-upload-no-valido.png)

![](img/05-upload-docx.png)

![](img/06-upload-ok.png)

![](img/07-rewrite.png)

Utilizando *wfuzz* encontramos los diferentes archivos que forman la página, y como se utiliza `index.php?page=[file]` para mostrar las paginas.

![](img/08-fuzzing-parameter.png)

Un archivo *docx* es en realidad es un archivo *zip* con los archivos que forman el documento, aprovechamos esto para insertar una webshell php dentro del empaquetado.

![](img/09-montar-zip.png)

Utilizando el wrapper `zip://` podemos ejecutar la webshell.

![](img/10-shell.png)

Aunque no es obligatorio, copiamos la webshell al directorio uploads para trabajar de forma mucho mas comoda.

Con esta nueva webshell podemos ver facilmente el archivo con la flag en el directorio ** __FLAG_HERE__ **

![](img/14-flag.png)