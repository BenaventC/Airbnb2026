# Airbnb2026
Ce repo regroupe des experimentations faites avec les étdudiants du Master AISO au cours d'un enseignement d'application. Des corpus Airbnb font l'objet de l'exploration. Celui de Paris est le modèle, les étudiants étudient d'autres villes. 

On trouvera des scripts en python pour différentes tâches NLP. Les scripts en r/quarto sont consacrés à l'analyse statistiques et à la production de présentation en beamer.  

## python

-   Annotation syntaxique
-   Detection des genres à partir des prénoms
-   Detection des aspects et sentiments
-   ...

## quarto

-   Analyse quanti de Paris

## workflow git (après chaque modif)

1) Vérifier les changements

```bash
git status
```

2) Ajouter et commiter

```bash
git add .
git commit -m "feat|fix|docs|chore: message court"
```

3) Envoyer sur GitHub

```bash
git push
```

### notes importantes

- Le hook local bloque les fichiers > 500 Ko (sauf exceptions configurées).
- Les fichiers `data/reviews_select.csv` et `results_*.csv` sont autorisés selon les règles du projet.
- Les gros CSV de résultats sont gérés via Git LFS (`.gitattributes`).
