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
	printf("crypto keygen	- generate a new key, displayed as hexstring\n");
	printf("crypto enc <key> - encrypt stdin with hexstring key\n");
	printf("crypto dec <key> - decrypt stdin with hexstring key\n");
	printf("\n");
}

void brutedecode() {

	FILE *f;

	// READ STDIN
	unsigned char msg[16384];
	int n_msg;
	int msg_len;
	EVP_CIPHER_CTX *ctx;
	unsigned char iv[16];
	int n_iv;
	unsigned char cipher[16384];
	int n_cipher;

	char filename[50];

	n_iv = read(STDIN_FILENO, iv, 16);
	if (n_iv != 16) {
		printf("cannot read IV from stdin\n");
		exit(1);
	}
	printf("IV: %016x\n", n_iv);


	n_cipher = read(STDIN_FILENO, cipher, 16384);
	if (n_cipher < 16) {
		printf("cannot read from stdin\n");
		exit(1);
	}

	unsigned char key[16];
	unsigned char hexkey[33];
	unsigned int seed = 0;
	int i;
	unsigned int val;

	for(seed=0 ; seed<=16777216; seed++) {

		srand(seed);

		for (i=0; i<16; i++) {
			val = rand();
			key[i] = (unsigned char)(val & 0xff);
			srand(val);
		}

		if (!(ctx = EVP_CIPHER_CTX_new())) continue;

		if (EVP_DecryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, key, iv) != 1) {
			continue;
		}

		if (EVP_DecryptUpdate(ctx, msg, &n_msg, cipher, n_cipher) != 1) {
			continue;
		}
		msg_len = n_msg;

		if (EVP_DecryptFinal_ex(ctx, msg + n_msg, &n_msg) != 1) {
			continue;
		}

		msg_len += n_msg;

		EVP_CIPHER_CTX_free(ctx);

		for (i=0; i<16; i++) {
			sprintf(hexkey + 2*i, "%02x", key[i]);
		}

		sprintf(filename, "out/%d_%s", seed, hexkey);
		printf("%d ", seed);
		f = fopen(filename, "wb");
		fwrite(msg, msg_len, 1, f);
		fclose(f);
	}
}

int main(int argc, char *argv[]) {
	brutedecode();
	exit(0);
	return 1;
}
