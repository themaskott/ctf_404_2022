from binascii import unhexlify
from Crypto.Util.number import GCD, inverse


N = 0x99e3992a04e6b2bb911f0d49b4ef539be1c6480388efb34932a3379862985e6954c3425a322ca3fb215fab720893ca6db1ecbcb4fd90a6f8fd2a700f1496a585fadafb1037c1eba99d47d4bfaa8dea7cc49f357257b00521aacb63277bdf1578948764d7db0eb9912781e11f34d33e60ccd07cb20aaf10e444638e92f37aebd6d4d742c0d9c93e9f9dd0d75bfd4352cf602592573b9799530116cbd2232a2b44b3f26ca9780036818b96f81a97e8756a6dbd8b99263267d4835776adb3f0e342b8cd1afc00458f4b5e0b589930d5c352b407779a0733969806b80390c3c548116077d954a176675637e0a38cd2fbc64039560aa2fb4b44c821602ffb9051291d

e = 0x10001

flag = 0x6addc82dedf3ad551f40d14821e891b942f291806a51561f2983cc7905af8ab313251938d6b12f26b3e25e1136a27f309bc2e8d7ad51988e14d946f8da65ae52f11247e0b5478c7eac8a97bb9141356981e3d4f9a48657f8730d708826220584c3fb13f8841c9297937bec9898d51270955c6efac70fb2ebbabe38b92d01def114edad977e5eff1c05e4ca40335d132a208b173dfdb21f29e730695be2e59b63373b7c33dc217009d103c3c475eb7366ba95c4bcdb8fdfe65ab965a42c9b3369f984ee1838c498a77984ff0fe9fea7b089973a9e539e5d5196946a54737e10f830bb4e58631f130fa1e17eeec443575dfb88b23c4bb4229ae410fb5facbd31a1

plain = []
encrypted = []

with open("data.txt","r") as f:
    for l in f:
        if l.startswith("input"):
            plain.append( int(l.split(':')[1].replace('\n','').strip(), 16 ))
        if l.startswith("encrypted"):
            encrypted.append( int(l.split(':')[1].replace('\n','').strip(), 16 ))

# check that all plain / ciphered are extracted
print(len(plain) == len(encrypted) == 200)

# check that each plain correspond to the right ciphered
for (p, c) in zip(plain, encrypted):
    if pow(p,e,N) != c:
        print(p)

hole = 0

# search for hole in known plain texts
for p in plain:
    if p in encrypted:
        print(p)
        print(encrypted[plain.index(p)])
        hole = p

p = GCD(hole, N)
q = N//p

d = inverse(e, (p-1)*(q-1))

f = pow(flag,d,N)

print(unhexlify(hex(f)[2:]))
