# Skill: règles générales de structure de code (AirBnB_NLP4socialscience)

## Objectif
Ce dépôt suit un pipeline NLP reproductible pour les reviews Airbnb:
1. filtrage des données,
2. extraction (aspects/sentiment/syntaxe),
3. normalisation éventuelle,
4. export CSV + métriques runtime/énergie/eCO2.

## Règles globales
- Préférer des scripts Python nommés avec préfixe `pXX_` (ex: `p02_aspects_gemma3_7b.py`).
- Conserver les entrées/sorties dans `data/`.
- Ne pas hardcoder de chemins absolus.
- Toujours garder une option `--sample-size` (int ou `total`).
- Ajouter une barre de progression pour les boucles longues (`tqdm` si disponible, fallback sinon).
- Afficher en fin de run: durée, Wh, gCO2e.

## Structure recommandée d’un script pipeline
1. **Imports + constantes** (`POWER_WATTS`, `FR_GRID_KGCO2_PER_KWH`, modèle LLM, URL API)
2. **Helpers techniques** (progress bar, appels API)
3. **Helpers métier** (parsing, normalisation)
4. **Préparation échantillon** (filtre langues + textes non vides)
5. **Boucle principale d’extraction**
6. **Agrégation/statistiques**
7. **Exports CSV**
8. **Résumé final (runtime/eCO2)**

## Standards Ollama
- Endpoint: `http://localhost:11434/api/generate`
- Paramètres minimaux: `model`, `prompt`, `stream=False`, `temperature`
- Gérer les erreurs réseau/JSON proprement et retourner une sortie vide plutôt qu’interrompre tout le run.

## Standards de sortie
- Fichier par review: `data/results_*_per_review.csv`
- Fichier synthèse: `data/results_*_summary.csv`
- Fichier synthèse normalisée (si activée): `data/results_*_summary_normalized.csv`
- Encodage: `utf-8`

## Checklist avant validation
- Le script passe sur `--sample-size 5`.
- Les colonnes de sortie sont stables et documentées.
- Aucun notebook/script ne dépend d’un état caché du kernel.
- Les résultats sont reproductibles avec les mêmes paramètres.
