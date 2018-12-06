# Navajanegra 2016 - Web 1 MongoJojo
## MongoDB Blind Injection

![](img/mongojojo.png)

Las imagenes de las supernenas se generan con la siguiente URL con un parametro en base64 del nombre de cada una (Cactus, Petalo y Burbuja).

```html
<img src="/avatar/Q2FjdHVz">
<img src="/avatar/UGV0YWxv">
<img src="/avatar/QnVyYnVqYQ==">
```

Este parametro de la URL es vulnerable a NoSQL injection, ya que la aplicación utiliza una base de datos MongoDB.

### Scripts

Con estos 3 scripts se automatiza el proceso de obtener cada caracter del objeto `this`. El primero lo hace probando entre una lista de caracteres, el segundo implementa threads para agilizar el proceso y finalmente el tercero hace una busqueda binaria y soporta threads.

[MongoJojo.py](MongoJojo.py)

[![asciicast](https://asciinema.org/a/88573.svg)](https://asciinema.org/a/88573)

[MongoJojo-threads.py](MongoJojo-threads.py)

[![asciicast](https://asciinema.org/a/88578.svg)](https://asciinema.org/a/88578)

[MongoJojo-threads-bit.py](MongoJojo-threads-bit.py)

[![asciicast](https://asciinema.org/a/88871.svg)](https://asciinema.org/a/88871)

```
{  "_id" : ObjectId("57d6bc3c27913d21a0bbad41"),  "user" : "MojoJojo",  "password" : "bubbles{Ih4t3Sup3RG1rrrlz}",  "avatar" : "mojo.png",  "admin" : "YES" }
```

```
{
	"_id" : ObjectId("57d6bc4727913d21a0bbad42"),
	"user" : "Burbuja",
	"password" : "1234",
	"avatar" : "burbuja.png",
	"admin" : "NO"
}

{
	"_id" : ObjectId("57d6bc5227913d21a0bbad43"),
	"user" : "Petalo",
	"password" : "gl00m",
	"avatar" : "petalo.png",
	"admin" : "NO"
}

{
	"_id" : ObjectId("57d6bc5c27913d21a0bbad44"),
	"user" : "Cactus",
	"password" : "CuidadoQueQuemo",
	"avatar" : "cactus.png",
	"admin" : "NO"
}

{
	"_id" : ObjectId("57d6bc3c27913d21a0bbad41"),
	"user" : "MojoJojo",
	"password" : "bubbles{Ih4t3Sup3RG1rrrlz}",
	"avatar" : "mojo.png",
	"admin" : "YES"
}
```
