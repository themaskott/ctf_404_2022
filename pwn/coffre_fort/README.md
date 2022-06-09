## PWN / Coffre Fort

<p align="center">
  <img src="img/consignes.png" />
</p>


### Look around

Le challenge fournit une interface de connexion, ainsi que deux binaire :
- le programme avec lequel nous interagissons via l'interface
- la `libc` utilisée sur le serveur

Si on se connecte, nous pouvons entrer un login et un mot de passe ... et c'est tout.

```bash
$ nc challenge.404ctf.fr 30863
Bienvenue sur l'interface de connexion au Coffre-fort !

- Veuillez saisir votre identifiant.
toto
- Veuillez désormais saisir votre mot de passe.
pass
```

On peut faire quelques essais classique (taille, format string, ...) mais cela ne change rien au comportement.

### Analyse statique

```bash
$ checksec coffre-fort
[*] '/home/debian/challenge/404/coffre-fort'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

Pour ce qui est des sécurités, bonne nouvelle, pas de canary. En revanche la stack est non exécutable, et l'ASLR activée sur le serveur.

```bash
seccomp-tools dump ./coffre-fort
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000000  A = sys_number
 0001: 0x15 0x05 0x00 0x00000001  if (A == write) goto 0007
 0002: 0x15 0x04 0x00 0x00000000  if (A == read) goto 0007
 0003: 0x15 0x03 0x00 0x0000003c  if (A == exit) goto 0007
 0004: 0x15 0x02 0x00 0x000000e7  if (A == exit_group) goto 0007
 0005: 0x25 0x01 0x00 0x0000014c  if (A > 0x14c) goto 0007
 0006: 0x06 0x00 0x00 0x00000000  return KILL
 0007: 0x06 0x00 0x00 0x7fff0000  return ALLOW
```

Par ailleurs des filtres sont en place sur les `SYSCALL` autorisés pour le binaire.

Ici nous pourrons : lire, écrire, quitter ou utiliser des `SYSCALL` supérieurs à 0x14c (332)

https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/

Toutefois, il n'y a pas de check sur l'architecture.

### Analyse du code

```c
undefined8 FUN_main(void)

{
  char msg_2 [50];
  char user_pass [32];
  char user_name [128];
  char msg_1 [94];

  FUN_seccomp();
  msg_1._0_8_ = 0x756e65766e656942;
  msg_1._8_8_ = 0x276c207275732065;
  msg_1._16_8_ = 0x6361667265746e69;
  msg_1._24_8_ = 0x6e6f632065642065;
  msg_1._32_8_ = 0x61206e6f6978656e;
  msg_1._40_8_ = 0x657266666f432075;
  msg_1._48_8_ = 0xa212074726f662d;
  msg_1._56_8_ = 0x6c69756556202d0a;
  msg_1._64_8_ = 0x73696173207a656c;
  msg_1._72_8_ = 0x6572746f76207269;
  msg_1._80_8_ = 0x6669746e65646920;
  msg_1._88_4_ = 0x746e6169;
  msg_1._92_2_ = 0xa2e;
  user_name._0_8_ = 0;
  user_name._8_8_ = 0;
  user_name._16_8_ = 0;
  user_name._24_8_ = 0;
  user_name._32_8_ = 0;
  user_name._40_8_ = 0;
  user_name._48_8_ = 0;
  user_name._56_8_ = 0;
  user_name._64_8_ = 0;
  user_name._72_8_ = 0;
  user_name._80_8_ = 0;
  user_name._88_8_ = 0;
  user_name._96_8_ = 0;
  user_name._104_8_ = 0;
  user_name._112_8_ = 0;
  user_name._120_8_ = 0;
  write(1,msg_1,0x5e);
  read(0,user_name,0x80);
  user_pass._0_8_ = 0;
  user_pass._8_8_ = 0;
  user_pass._16_8_ = 0;
  user_pass._24_8_ = 0;
  msg_2._0_8_ = 0x6c6c69756556202d;
  msg_2._8_8_ = 0x6f73a9c364207a65;
  msg_2._16_8_ = 0x6173207369616d72;
  msg_2._24_8_ = 0x746f762072697369;
  msg_2._32_8_ = 0x6420746f6d206572;
  msg_2._40_8_ = 0x2e65737361702065;
  msg_2._48_2_ = 10;
  write(1,msg_2,0x31);
  read(0,user_pass,0x20);
  FUN_check_pass((byte *)user_pass);
  return 0;
}
```


```c
void FUN_seccomp(void)

{
  int iVar1;
  undefined2 local_18 [4];
  undefined *local_10;

  local_18[0] = 8;
  local_10 = &DAT_00404020;
  iVar1 = prctl(0x26,1,0,0,0);
  if (iVar1 < 0) {
    perror("prctl(PR_SET_NO_NEW_PRIVS)");
                    /* WARNING: Subroutine does not return */
    exit(2);
  }
  iVar1 = prctl(0x16,2,local_18);
  if (iVar1 < 0) {
    perror("prctl(PR_SET_SECCOMP)");
                    /* WARNING: Subroutine does not return */
    exit(2);
  }
  return;
}
```




```c
undefined  [16] FUN_check_pass(byte *user_pass)

{
  int rand_int;
  long uVar1;
  byte uVar2;
  byte rand_tab_1 [128];
  byte rand_tab_2 [128];
  byte buff [32];
  int j;
  int i;
  long uVar3;

  buff._0_8_ = 0;
  buff._8_8_ = 0;
  buff._16_8_ = 0;
  buff._24_8_ = 0;
  for (i = 0; (uint)i < 0x80; i = i + 1) {
    rand_int = rand();
    rand_tab_1[i] = (byte)rand_int;
    rand_int = rand();
    rand_tab_2[i] = (byte)rand_int | 1;
  }
  j = 0;
  do {
    if (user_pass[j] == 0) {
      uVar3 = 0;
      uVar1 = 1;
LAB_0040135c:
      return CONCAT88(uVar3,uVar1);
    }
    buff[j] = user_pass[j] ^ rand_tab_2[j];
    if ((j < 0x20) && (uVar3 = (long)buff[j], buff[j] != rand_tab_1[j])) {
      uVar1 = 0;
      goto LAB_0040135c;
    }
    j = j + 1;
  } while( true );
}

```


### Exploit







Stack dans la fonction check_pass après génération des rand() :


gdb-peda$ x/50gx $rsp
0x7fffffffdd50:	0x00007ffff7fb1540	0x00007fffffffdee0
0x7fffffffdd60:	0xe3f2ba294a516967	0xc9332e76e71b547c
0x7fffffffdd70:	0x5e580525a3310d66	0xdc21740e549bcdab
0x7fffffffdd80:	0x6bea7e3efc413e70	0xdbec3c323bec5c8f
0x7fffffffdd90:	0x7c05d1fbaafbfe02	0xf1b10fa85c89be75
0x7fffffffdda0:	0x6448cbca3ae9f705	0x795e5a14641c1e1f
0x7fffffffddb0:	0xaf1bacaa0911643b	0x7dba22bb1548e333
0x7fffffffddc0:	0x4eb51bf8f87f1a0b	0x6cfa4ebc3d793898
0x7fffffffddd0:	0x5c3bb5be55aa21ac	0x4efd154fe4e2b336
0x7fffffffdde0:	0x47fbabcdedff73c7	0x9b9f635b8de9f9c3
0x7fffffffddf0:	0xd5e9175d5b59b733	0x873d418311b5c7b3
0x7fffffffde00:	0x97dd970167e1a1e9	0x5d1955affbb12b39
0x7fffffffde10:	0x953de7293bfb431b	0xb3eb9599bbf961d9
0x7fffffffde20:	0xbd47d10be5a101ef	0x634bc573c57ba923
0x7fffffffde30:	0x3b11f3d5dd9f2571	0xf59b196f5d4751cd
0x7fffffffde40:	0xe9cb13a529231de1	0x05cb775f354de133
0x7fffffffde50:	0xd3057371a31b2b87	0xa98349339ff1af95
0x7fffffffde60:	0x0000000000000085	0x0000000000000000
0x7fffffffde70:	0x0000000000000000	0x0000000000000000
0x7fffffffde80:	0x0000000000000008	0x0000008000000000
0x7fffffffde90:	0x00007fffffffdfe0	0x00000000004015d1
0x7fffffffdea0:	0x6c6c69756556202d	0x6f73a9c364207a65
0x7fffffffdeb0:	0x6173207369616d72	0x746f762072697369
0x7fffffffdec0:	0x6420746f6d206572	0x2e65737361702065
0x7fffffffded0:	0x000003400000000a	0x0000034000000340



On retrouve le même aléa que généré par notre code :

tab_a :6769514a29baf2e37c541be7762e33c9660d31a32505585eabcd9b540e7421dc703e41fc3e7eea6b8f5cec3b323cecdb02fefbaafbd1057c75be895ca80fb1f105f7e93acacb48641f1e1c64145a5e793b641109aaac1baf33e34815bb22ba7d0b1a7ff8f81bb54e9838793dbc4efa6cac21aa55beb53b5c36b3e2e44f15fd4e
tab_b : c773ffedcdabfb47c3f9e98d5b639f9b33b7595b5d17e9d5b3c7b51183413d87e9a1e1670197dd97392bb1fbaf55195d1b43fb3b29e73d95d961f9bb9995ebb3ef01a1e50bd147bd23a97bc573c54b6371259fddd5f3113bcd51475d6f199bf5e11d2329a513cbe933e14d355f77cb05872b1ba3717305d395aff19f334983a9

tab_a :
6769514a29baf2e3 7c541be7762e33c9
660d31a32505585e abcd9b540e7421dc
703e41fc3e7eea6b 8f5cec3b323cecdb
02fefbaafbd1057c 75be895ca80fb1f1
05f7e93acacb4864 1f1e1c64145a5e79
3b641109aaac1baf 33e34815bb22ba7d
0b1a7ff8f81bb54e 9838793dbc4efa6c
ac21aa55beb53b5c 36b3e2e44f15fd4e

tab_b :
c773ffedcdabfb47 c3f9e98d5b639f9b
33b7595b5d17e9d5 b3c7b51183413d87
e9a1e1670197dd97 392bb1fbaf55195d
1b43fb3b29e73d95 d961f9bb9995ebb3
ef01a1e50bd147bd 23a97bc573c54b63
71259fddd5f3113b cd51475d6f199bf5
e11d2329a513cbe9 33e14d355f77cb05
872b1ba3717305d3 95aff19f334983a9



```c
#include <stdlib.h>
#include <stdio.h>


int main(){

    unsigned char tab_a[128] = {0} ;
    unsigned char tab_b[128] = {0} ;

    int a = 0 ;
    int b = 0 ;


    for (int i = 0 ; i < 128 ; i++){

        a = rand() ;
        tab_a[i] = (unsigned char)a;

        b = rand() ;
        tab_b[i] = (unsigned char)b | 1;

    }

    printf("tab_a :\n") ;
    for (int i = 0 ; i < 128 ; i++ ){
        printf("%02x",tab_a[i]) ;
        if((i+1)%8==0)
            printf(" ");
        if((i+1)%16==0)
            printf("\n");
    }


    printf("\n");
    printf("tab_b :\n");

    for (int i = 0 ; i < 128 ; i++){
        printf("%02x",tab_b[i]) ;
        if ((i+1)%8==0)
            printf(" ");
        if((i+1)%16==0)
            printf("\n");
    }

    printf("\n");

    return 0 ;
}


```




stack check_pass

0x7fffffffdd50: 0x00007ffff7fb1540  0x00007fffffffdee0
tab_1
0x7fffffffdd60: 0xe3f2ba294a516967  0xc9332e76e71b547c
0x7fffffffdd70: 0x5e580525a3310d66  0xdc21740e549bcdab
0x7fffffffdd80: 0x6bea7e3efc413e70  0xdbec3c323bec5c8f
0x7fffffffdd90: 0x7c05d1fbaafbfe02  0xf1b10fa85c89be75
0x7fffffffdda0: 0x6448cbca3ae9f705  0x795e5a14641c1e1f
0x7fffffffddb0: 0xaf1bacaa0911643b  0x7dba22bb1548e333
0x7fffffffddc0: 0x4eb51bf8f87f1a0b  0x6cfa4ebc3d793898
0x7fffffffddd0: 0x5c3bb5be55aa21ac  0x4efd154fe4e2b336
tab_2
0x7fffffffdde0: 0x47fbabcdedff73c7  0x9b9f635b8de9f9c3
0x7fffffffddf0: 0xd5e9175d5b59b733  0x873d418311b5c7b3
0x7fffffffde00: 0x97dd970167e1a1e9  0x5d1955affbb12b39
0x7fffffffde10: 0x953de7293bfb431b  0xb3eb9599bbf961d9
0x7fffffffde20: 0xbd47d10be5a101ef  0x634bc573c57ba923
0x7fffffffde30: 0x3b11f3d5dd9f2571  0xf59b196f5d4751cd
0x7fffffffde40: 0xe9cb13a529231de1  0x05cb775f354de133
0x7fffffffde50: 0xd3057371a31b2b87  0xa98349339ff1af95
buff
0x7fffffffde60: 0xe3f2ba294a516967  0xc9332e76e71b547c
0x7fffffffde70: 0x5e580525a3310d66  0xdc21740e549bcdab

0x7fffffffde80: 0xd69cd64026a0e0a8  0x00000080000000fe
0x7fffffffde90: 0x00007fffffffdfe0  0x00000000004015d1

stack main

String_2
0x7fffffffdea0: 0x6c6c69756556202d  0x6f73a9c364207a65
0x7fffffffdeb0: 0x6173207369616d72  0x746f762072697369
0x7fffffffdec0: 0x6420746f6d206572  0x2e65737361702065
0x7fffffffded0: 0x000003400000000a  0xe8c20872deb0ee40
user_pass
0x7fffffffdee0: 0xa2b3fb680b102826  0x88726f37a65a153d
0x7fffffffdef0: 0x1f194464e2704c27  0x9d60354f15da8cea

user_name
0x7fffffffdf00: 0xa3f2b33648c589ea  0x276c20f2757320cd
0x7fffffffdf10: 0x6361198d9a8bb189  0x6e6f6320652435b4
0x7fffffffdf20: 0x0d4c071a0c2e4543  0x0a01cfa50b635a10
0x7fffffffdf30: 0x6b5200071b0e0b5f  0x1806034524495e63
0x7fffffffdf40: 0x1749151c4d5a001e  0x4b17071c1750520c
0x7fffffffdf50: 0x6669772e6564692a  0x4141025caade8f29
0x7fffffffdf60: 0x4141414141414141  0x4141414141414141
0x7fffffffdf70: 0x4141414141414141  0x4141414141414141

String_1
0x7fffffffdf80: 0x756e65766e656942  0x276c207275732065
0x7fffffffdf90: 0x6361667265746e69  0x6e6f632065642065
0x7fffffffdfa0: 0x61206e6f6978656e  0x657266666f432075
0x7fffffffdfb0: 0x0a212074726f662d  0x6c69756556202d0a
0x7fffffffdfc0: 0x73696173207a656c  0x6572746f76207269
0x7fffffffdfd0: 0x6669746e65646920  0x00000a2e746e6169
0x7fffffffdfe0: 0x00000000004015e0  0x00007ffff7e11d0a
0x7fffffffdff0: 0x00007fffffffe0d8  0x00000001ffffe3e9
0x7fffffffe000: 0x000000000040135e  0x00007ffff7e118e9

-----

0x7fffffffdd50: 0x00007ffff7fb1540  0x00007fffffffdee0

0x7fffffffdd60: 0xe3f2ba294a516967  0xc9332e76e71b547c
0x7fffffffdd70: 0x5e580525a3310d66  0xdc21740e549bcdab
0x7fffffffdd80: 0x6bea7e3efc413e70  0xdbec3c323bec5c8f
0x7fffffffdd90: 0x7c05d1fbaafbfe02  0xf1b10fa85c89be75
0x7fffffffdda0: 0x6448cbca3ae9f705  0x795e5a14641c1e1f
0x7fffffffddb0: 0xaf1bacaa0911643b  0x7dba22bb1548e333
0x7fffffffddc0: 0x4eb51bf8f87f1a0b  0x6cfa4ebc3d793898
0x7fffffffddd0: 0x5c3bb5be55aa21ac  0x4efd154fe4e2b336

0x7fffffffdde0: 0x47fbabcdedff73c7  0x9b9f635b8de9f9c3
0x7fffffffddf0: 0xd5e9175d5b59b733  0x873d418311b5c7b3
0x7fffffffde00: 0x97dd970167e1a1e9  0x5d1955affbb12b39
0x7fffffffde10: 0x953de7293bfb431b  0xb3eb9599bbf961d9
0x7fffffffde20: 0xbd47d10be5a101ef  0x634bc573c57ba923
0x7fffffffde30: 0x3b11f3d5dd9f2571  0xf59b196f5d4751cd
0x7fffffffde40: 0xe9cb13a529231de1  0x05cb775f354de133
0x7fffffffde50: 0xd3057371a31b2b87  0xa98349339ff1af95

0x7fffffffde60: 0x0000000000000085  0x0000000000000000
0x7fffffffde70: 0x0000000000000000  0x0000000000000000

0x7fffffffde80: 0x0000000000000008  0x0000008000000000
0x7fffffffde90: 0x00007fffffffdfe0  0x00000000004015d1

0x7fffffffdea0: 0x6c6c69756556202d  0x6f73a9c364207a65
0x7fffffffdeb0: 0x6173207369616d72  0x746f762072697369
0x7fffffffdec0: 0x6420746f6d206572  0x2e65737361702065
0x7fffffffded0: 0x000003400000000a  0x0000034000000340

0x7fffffffdee0: 0x4242424242424242  0x4242424242424242
0x7fffffffdef0: 0x4242424242424242  0x4242424242424242

0x7fffffffdf00: 0x4141414141414141  0x4141414141414141
0x7fffffffdf10: 0x4141414141414141  0x4141414141414141
0x7fffffffdf20: 0x4141414141414141  0x4141414141414141
0x7fffffffdf30: 0x4141414141414141  0x4141414141414141
0x7fffffffdf40: 0x4141414141414141  0x4141414141414141
0x7fffffffdf50: 0x4141414141414141  0x4141414141414141
0x7fffffffdf60: 0x4141414141414141  0x4141414141414141
0x7fffffffdf70: 0x4141414141414141  0x4141414141414141

0x7fffffffdf80: 0x756e65766e656942  0x276c207275732065
0x7fffffffdf90: 0x6361667265746e69  0x6e6f632065642065
0x7fffffffdfa0: 0x61206e6f6978656e  0x657266666f432075
0x7fffffffdfb0: 0x0a212074726f662d  0x6c69756556202d0a
0x7fffffffdfc0: 0x73696173207a656c  0x6572746f76207269
0x7fffffffdfd0: 0x6669746e65646920  0x00000a2e746e6169
0x7fffffffdfe0: 0x00000000004015e0  0x00007ffff7e11d0a
0x7fffffffdff0: 0x00007fffffffe0d8  0x00000001ffffe3e9
0x7fffffffe000: 0x000000000040135e  0x00007ffff7e118e9
