from binascii import unhexlify
from Crypto.Util.number import inverse
from math import isqrt
import socket


def send_bytes(s, b):
	s.send(b.encode() + b'\n')
	rep = s.recv(2048)
	return rep


HOST = 'challenge.404ctf.fr'
PORT = 30594

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    rep = s.recv(2048)

    cipher_flag = int( rep.split(b'\n')[2].decode() )

    e = 65537

    print(f'{cipher_flag=}')
    print(f'{e=}')

    # chosen plain text

    rep = send_bytes(s, str(cipher_flag**2) )
    rep = int(rep.split(b'\n')[1].decode())

    flag = isqrt(rep)

    print(unhexlify(hex(flag)[2:]))
