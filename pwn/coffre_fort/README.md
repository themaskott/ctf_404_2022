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


### Exploit
