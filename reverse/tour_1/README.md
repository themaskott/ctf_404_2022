## REVERSE / Renverse la tour ! [1/2]

<p align="center">
  <img src="img/consignes.png" />
</p>


### Look around

Le fichier du challenge contient trois fonctions, appellées successivement pour encoder notre mot de passe.

Il s'agit alors de trouver un password validant la condition :

```python
if tour3(tour2(tour1(mdp))) == "¡P6¨sÉU1T0d¸VÊvçu©6RÈx¨4xFw5":
```


### Dive into python

Il nous reste simplement à coder les fonctions inverse de ces trois fonctions pour calculer (dans le bon ordre ...):


```python
r_tour1(r_tour2(r_tour3(tour3(tour2(tour1(mdp))) ))) == r_tour1(r_tour2(r_tour3("¡P6¨sÉU1T0d¸VÊvçu©6RÈx¨4xFw5")))

mdp == r_tour1(r_tour2(r_tour3("¡P6¨sÉU1T0d¸VÊvçu©6RÈx¨4xFw5")))

```
