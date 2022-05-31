## PROGRAMMATION / Découpé

<p align="center">
  <img src="img/consignes.png" />
</p>


### Look around

Nous avons à notre disposition un gros fichier `tar` qui a priori selon son nommage a été archivé/compressé 2500 fois.

On peut l'ouvrir à la main quelques fois pour voir l'imbrication.

### Solve

Un petit code `bash` fera l'affaire, le trick étant d'utiliser les bonnes options de décompression quand nécessaire :

```bash
#!/bin/bash

for i in {2500..1}
do
    name=flag$i
    if [ -f $name.tar.gz ]
    then
        tar zxvf $name.tar.gz
        rm $name.*
    fi

    if [ -f $name.tar ]
    then
        tar xvf $name.tar
        rm $name.*
    fi

    if [ -f $name.tar.xz ]
    then
        tar -Jxvf $name.tar.xz
        rm $name.*
    fi

    if [ -f $name.tar.bz2 ]
    then
        tar -jxvf $name.tar.bz2
        rm $name.*
    fi

done
```

Il faut le laisser tourner pour récupérer `flag.txt`

`404CTF{C0mPr3Ssi0n_m4X1m4L3_m41S_p4S_3ff1C4c3}`
