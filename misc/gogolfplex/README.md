## MISC / GoGOLFPlex

<p align="center">
  <img src="img/consignes.png" />
</p>


### Look around

Le code du challenge nous est fournit : [chall.py](chall.py)



Un autre challenge pour regarder d'un peu plus près les internals de python .... mais qui peut faire vite perdre pas mal de temps si l'on ne va pas voir la documentation officielle (RTFM !)

Tout d'abord, le titre : `gogolplex` nous amène sur un nombre particulier : [gogolplex](https://fr.wiktionary.org/wiki/gogolplex) qui a part plein de zéros n'a pas de rapport avec le challenge


### Python internals


Tout d'abord le code utilise une `f-string` donc on peut supposer que l'interpréteur est d'une version >= 3.6

Aussi, notre `input()` ne pourra pas être exploité :  [input()](https://docs.python.org/3/library/functions.html#input)

En tout cas il est bien converti en `string`.

Après quelques recherches sur internet, on peut se convaincre que la f-string ne sera pas exploitable en soit.

Il reste le `int()`.

En allant voir de plus près : [int()](https://docs.python.org/3/library/functions.html#int), on note :
`If x is not a number or if base is given, then x must be a string, bytes, or bytearray instance representing an integer literal in radix base.`

Du coup, il faut alors aller voir la définition exacte d'un [integer literal](https://docs.python.org/3/reference/lexical_analysis.html#integers), où l'on remarque : `Underscores are ignored for determining the numeric value of the literal.`

Il suffit de faire quelques tests :

```python
>>> int("1_0_0_0")
1000
>>> a="1" + "_0" * 25
>>> a
'1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0'
>>> int(a)
10000000000000000000000000
```

Finalement, les chiffres imposés par le challenge prennent tous leur sens ....

Notre input va être étendu sur 51 caractères, paddé à droite par des `0`, mais il doit être `<=` à `10**25`.

On peut saisir directement `1` suivi de 50 `0`, mais en remplaçant un zéro sur deux par un underscore qui sera ignoré par `int()`, pour obtenir `10**25<=10**25`

```bash
$ nc challenge.404ctf.fr 32697
Bienvenue sur le goGOLFplex, le plus grand parcours de golf de l'univers!
Il comporte 10^16 trous mais le meilleur score que quelqu'un ait fait dans l'histoire est 10^25
Si tu arrives à battre ou égaliser ce score tu rentreras dans l'histoire !
En revanche on a décidé de te mettre un petit handicap, ne t'inquiète pas, ce n'est pas gênant ;)
En combien de coups essayez-vous de faire le parcours?
1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0
vous réussissez à finir le parcours en 10000000000000000000000000 coups
404CTF{Und3r5c0r35_1n_1nt3g3r5??}
```
