import time

from Crypto.Util.number import getStrongPrime, inverse, getRandomRange
from secret import flag


def encrypt( public_key, pt ):
    N, e = public_key
    return pow(pt, e, N)


def decrypt( public_key, private_key, ct ):
    N, e = public_key
    return pow(ct, private_key, N)


def gen_key( nb_bits ):
    p = getStrongPrime(nb_bits)
    q = getStrongPrime(nb_bits)
    N = p * q
    e = 65537
    d = inverse(e, (p - 1) * (q - 1))
    return ((N, e), d)


def gen_benchmarks( public_key, private_key, f):
    for i in range(200):
        r = getRandomRange(2, N)
        t = time.time()
        ct = encrypt(public_key, r)
        t_int = time.time() - t
        pt = decrypt(public_key, private_key, ct)
        t2 = time.time() - t
        check = (pt == r)
        f.write(
            f'input: {hex(r)}\nencrypted: {hex(ct)}\ntime to encrypt: {t_int}\ntime to decrypt: {t2 - t_int}\nmandatory_check: {check}\n\n')

f = open("data.txt", 'w')
public_key, private_key = gen_key(1024)
gen_benchmarks(public_key, private_key, f)
encrypted_flag = encrypt(public_key, flag)
N,e = public_key

f.write(f'N: {hex(N)}, e: {hex(e)}\n')
f.write(f'cipher: hex(encrypted_flag)')
f.close()
