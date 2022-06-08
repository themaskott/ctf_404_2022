from binascii import unhexlify
from Crypto.Util.number import inverse
import socket


def send_bytes(s, b):
	s.send(b.encode() + b'\n')
	rep = s.recv(2048)
	return rep


HOST = 'challenge.404ctf.fr'
PORT = 32128

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    rep = s.recv(2048)

    cipher_flag = int( rep.split(b'\n')[1].decode() )
    N = int( rep.split(b'\n')[3][4:].decode() )

    e = 65537

    print(f'{cipher_flag=}')
    print(f'{N=}')
    print(f'{e=}')

    # chosen plain text
    k = 5
    known = pow(k,e,N)

    rep = send_bytes(s, str(cipher_flag*known) )
    rep = int(rep.split(b'\n')[1].decode())

    inv = inverse(rep,N)

    flag = inverse(inv * k,N)
    flag = hex(flag)[2:]
    print(unhexlify(flag))
