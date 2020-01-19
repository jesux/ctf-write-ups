#!/usr/bin/env python2

from subprocess import *
import string
import sys

command = "perf stat -x : -e instructions:u " + sys.argv[1] + " 1>/dev/null"

letters = string.printable
letters = '0123456789abcdef}'

LEN = None
#LEN = 39
flag = 'H-c0n{'
#flag = 'H-c0n{bdd0fbdbefa8e89f421140836280a568}'


if LEN is None:
    ins_count = 0
    LEN = ''
    for i in range(40):
        target = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
        target_output, _ = target.communicate(input='%s\n'%('A'*i))
        instructions = int(target_output.split(':')[0])
        print('\r[+] %s - %d' % (i, instructions))
        if instructions > ins_count:
            LEN = i
            ins_count = instructions
    print('FLAG LENGTH: %02d\n' % LEN)

while len(flag)<LEN:
    ins_count = 0
    count_chr = ''
    for i in letters:
        target = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
        target_output, _ = target.communicate(input='%s\n' % (flag + i + ((LEN-len(flag)-1)*'A')))
        instructions = int(target_output.split(':')[0])
        print('[+] %s - %d' % (i, instructions))
        if instructions > ins_count:
            count_chr = i
            ins_count = instructions

    flag += count_chr
    print('RESULT: %s\n' % flag)
