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
Chaque section doit inclure une **cellule markdown explicative** décrivant son objectif avant l'implémentation:
1. **Imports + constantes** - Charger les packages et initialiser `POWER_WATTS`, `FR_GRID_KGCO2_PER_KWH`, modèles LLM/API, compteurs temps
2. **Détection GPU & parallélisation** - Détecter nb GPUs disponibles (voir p01 pour pattern), configurer multiprocessing mode, assigner workers par GPU (jusqu'à 4 GPU H100), fallback sur CPU si indisponible
3. **Helpers techniques** - Progress bars, appels API, gestion erreurs réseau
4. **Helpers métier** - Parsing, normalisation, extraction d'entités
5. **Préparation échantillon** - Filtrer langues, textes non vides, déduplications
6. **Boucle principale d'extraction** - Parallélisée par GPU/CPU selon disponibilité
7. **Agrégation/statistiques** - Consolider résultats par langue/modèle/GPU
8. **Exports CSV** - Per-review et synthèse
9. **Résumé final (runtime/eCO2)** - Afficher durée, Wh, gCO2e, date/heure fin

### Documentation obligatoire des sections
**RÈGLE EXPLICITE** : Chaque section de notebook/script DOIT avoir une cellule markdown descriptive **immédiatement sous le titre**, expliquant en 2-3 phrases simples:
- **L'objectif** : qu'est-ce que cette étape accomplit (langage simple, verbes actifs)
- **Les transformations clés** : données/variables entrantes vs sortantes
- Exemple bon format : "Charge le CSV, nettoie les données (supprime tokens vides, normalise), puis crée l'échantillon à traiter."
- Exemple mauvais format : "Section pour traiter données" ❌

## Standards Ollama
- Endpoint: `http://localhost:11434/api/generate`
- Paramètres minimaux: `model`, `prompt`, `stream=False`, `temperature`
- Gérer les erreurs réseau/JSON proprement et retourner une sortie vide plutôt qu’interrompre tout le run.
## Standards GPU et Parallélisation
**Pattern inspiré de p01_syntactic_dependency_analysis.ipynb**

Tous les scripts de traitement **doivent**:
1. **Détecter les GPUs disponibles** via `torch.cuda.device_count()` ou `nvidia-smi` (fallback):
   ```python
   import torch
   gpu_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
   ```
2. **Valider les GPU H100** (ou autre) avec un test CUDA simple sur chaque device
3. **Assigner les tâches par GPU** (une langue/entité par GPU jusqu'à 4 workers H100)
4. **Configurer multiprocessing spawn** pour éviter les deadlocks CUDA sous Linux/Jupyter:
   ```python
   import multiprocessing as mp
   mp.set_start_method('spawn', force=True)
   ```
5. **Fallback CPU** automatique si nb(GPUs) < 1 ou si GPU detectionéchoue
6. **Logs de runtime** pour chaque GPU/worker afficher: lang, GPU#, durée, Wh/gCO2e
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
- **Chaque section (notebook/script) possède une cellule markdown explicative** décrivant son objectif (2-3 phrases simples) immédiatement sous le titre.
- **GPU/CPU branching configuré** avec détection et fallback CPU implanté (si applicable au script).

## Skill Mermaid (Pipeline)
Pour les diagrammes Mermaid de pipeline, utiliser le skill local:
- Fichier: `.github/skills/mermaid-pipeline/SKILL.md`

Règles obligatoires pour les prochains diagrammes:
- Fond blanc + couleurs pastel claires.
- 3 blocs principaux: `DATA INPUTS` (bleu), `INTERNAL PROCESSING` (jaune), `OUTPUTS` (vert).
- Blocs principaux alignés horizontalement (gauche vers droite).
- Boites internes empilees verticalement dans chaque bloc.
- Fleches claires (gris clair), labels courts orientés action.

## Skill English Notebook Style
Pour la traduction et réécriture en anglais des cellules texte de notebook, utiliser le skill local:
- Fichier: `.github/skills/english-notebook-style/SKILL.md`

Règles obligatoires pour les prochaines mises en anglais:
- Traduire toutes les cellules markdown (titre, sections, paragraphes explicatifs).
- Utiliser des titres élégants et informatifs.
- Rédiger des paragraphes complets, clairs, et cohérents (pas de style télégraphique).
- Conserver le sens technique exact (pipeline, runtime, CO2, jointure, etc.).
- Ne pas modifier la logique du code sauf demande explicite.