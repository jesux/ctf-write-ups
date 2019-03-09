#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

// cc -Wall -o crypto crypto.c -lssl -lcrypto

void usage()
{
    printf("crypto - tool to generate keys, encrypt and decrypt\n\n");
    printf("crypto keygen    - generate a new key, displayed as hexstring\n");
    printf("crypto enc <key> - encrypt stdin with hexstring key\n");
    printf("crypto dec <key> - decrypt stdin with hexstring key\n");
    printf("\n");
}

void handleErrors(void)
{
    //ERR_print_errors_fp(stderr);
    exit(1);
}


/* hex2dec */
int hex2dec(char c)
{
    int val;

    if ((c >= '0') && (c <= '9')) {
        val = c - '0';
    } else if ((c >= 'A') && (c <= 'F')) {
        val = c - 'A' + 10;
    } else if ((c >= 'a') && (c <= 'f')) {
        val = c - 'a' + 10;
    } else {
        return -1;
    }

    return val;
}

/* hex2dec2 - 2char version of hex2dec */
int hex2dec2(char *ptr)
{
    int val, val2;

    val = hex2dec(ptr[0]);
    if ((val < 0)  || (val > 0xf)) {
        return -1;
    }

    val2 = hex2dec(ptr[1]);
    if ((val2 < 0)  || (val2 > 0xf)) {
        return -1;
    }

    return (val * 0x10) + val2;
}

/* decode hex and return length */
int decodekey(unsigned char *decoded, char *arg)
{
    int i;
    int len = strlen(arg);
    int val;

    if (len != 32) {
        printf("key should be 128 bits\n");
        return 0;
    }

    for (i=0; i<(len / 2); i++) {
        val = hex2dec2(arg + (i*2));
        if ((val < 0) || (val > 255)) {
            printf("error in hexstring\n");
            return 0;
        }
        decoded[i] = (unsigned char) val;
    }

    return 1;
}


void keygen()
{
    int fd;
    unsigned char key[16];
    unsigned int seed = 0;
    int i;
    unsigned int val;

    fd = open("/dev/urandom", O_RDONLY);
    if (fd <= 0) {
        printf("cannot open /dev/unrandom\n");
        exit(1);
    }

    if (read(fd, &seed, 3) < 3) {
        printf("cannot read from /dev/urandom\n");
        exit(1);
    }

    close(fd);

    printf("The seed is %d \n", seed);

    srand(seed);

    for (i=0; i<16; i++) {
        val = rand();
        key[i] = (unsigned char)(val & 0xff);
        srand(val);
    }

    for (i=0; i<16; i++) {
        printf("%02x", key[i]);
    }
    printf("\n");

}

void encrypt(unsigned char *key)
{
    unsigned char iv[16];
    int fd;
    unsigned char msg[16384];
    int n_msg;
    unsigned char cipher[16384];
    int n_cipher;
    int cipher_len;
    EVP_CIPHER_CTX *ctx;

    fd = open("/dev/urandom", O_RDONLY);
    if (fd <= 0) {
        printf("cannot open /dev/unrandom\n");
        exit(1);
    }

    if (read(fd, iv, 16) < 16) {
        printf("cannot read from /dev/urandom\n");
        exit(1);
    }

    close(fd);

    n_msg = read(STDIN_FILENO, msg, 16384);
    if (n_msg <= 0) {
        printf("cannot read from stdin\n");
        exit(1);
    }

    if (!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

    if (EVP_EncryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, key, iv) != 1)
        handleErrors();

    if (EVP_EncryptUpdate(ctx, cipher, &n_cipher, msg, n_msg) != 1)
        handleErrors();
    cipher_len = n_cipher;

    if (EVP_EncryptFinal_ex(ctx, cipher + n_cipher, &n_cipher) != 1)
        handleErrors();
    cipher_len += n_cipher;

    EVP_CIPHER_CTX_free(ctx);

    write(STDOUT_FILENO, iv, 16);
    write(STDOUT_FILENO, cipher, cipher_len);


}

void decrypt(unsigned char *key)
{
    unsigned char iv[16];
    int n_iv;
    unsigned char msg[16384];
    int n_msg;
    unsigned char cipher[16384];
    int n_cipher;
    int msg_len;
    EVP_CIPHER_CTX *ctx;

    n_iv = read(STDIN_FILENO, iv, 16);
    if (n_iv != 16) {
        printf("cannot read IV from stdin\n");
        exit(1);
    }

    n_cipher = read(STDIN_FILENO, cipher, 16384);
    if (n_cipher < 16) {
        printf("cannot read from stdin\n");
        exit(1);
    }

    if (!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

    if (EVP_DecryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, key, iv) != 1)
        handleErrors();

    if (EVP_DecryptUpdate(ctx, msg, &n_msg, cipher, n_cipher) != 1)
        handleErrors();
    msg_len = n_msg;

    if (EVP_DecryptFinal_ex(ctx, msg + n_msg, &n_msg) != 1)
        handleErrors();
    msg_len += n_msg;

    EVP_CIPHER_CTX_free(ctx);

    write(STDOUT_FILENO, msg, msg_len);

}



int main(int argc, char *argv[])
{
    unsigned char key[16];

    if (argc == 1) {
        usage();
        exit(0);
    }

    if (!strcmp(argv[1], "keygen")) {
        keygen();
        exit(0);
    }

    if (argc < 3) {
        usage();
        exit(0);
    }

    if (!decodekey(key, argv[2])) {
        usage();
        printf("key should be 128 bit hexstring, no leading 0x\n");
        exit(1);
    }

    if (!strcmp(argv[1], "enc")) {
        encrypt(key);
        exit(0);
    }

    if (!strcmp(argv[1], "dec")) {
        decrypt(key);
        exit(0);
    }

    usage();

    return 1;
}
