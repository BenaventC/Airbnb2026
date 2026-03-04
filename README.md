# Airbnb2026

This repository contains experiments developed with Master AISO students in an applied teaching context. Airbnb corpora are explored, with Paris used as the reference dataset and extensions to other cities.

The project includes Python scripts for multiple NLP tasks, as well as R/Quarto scripts for statistical analysis and Beamer presentation generation.

## Python

- Syntactic annotation: [p01_syntactic_dependency_analysis.ipynb](p01_syntactic_dependency_analysis.ipynb)
- Main aspect extraction pipeline (Ollama Gemma 3):
  - Script: [p02_aspects_gemma3_7b.py](p02_aspects_gemma3_7b.py)
  - Notebook: [p02_aspects_gemma3_7b.ipynb](p02_aspects_gemma3_7b.ipynb)
- Gender classification from first names:
  - [review_gender_classification.ipynb](review_gender_classification.ipynb)
  - [review_gender_classification2.ipynb](review_gender_classification2.ipynb)
- Aspect extraction and ABSA:
  - [aspect_extraction_gemma3.ipynb](aspect_extraction_gemma3.ipynb)
  - [aspect_probability_gemma3.ipynb](aspect_probability_gemma3.ipynb)
  - [absa_gemma3.ipynb](absa_gemma3.ipynb)
  - [absa_neighbourhood_gemma3.ipynb](absa_neighbourhood_gemma3.ipynb)
- Sentiment analysis: [bert_sentiment_analysis.ipynb](bert_sentiment_analysis.ipynb)
- Age estimation (experimental):
  - [extract_age_from_name_ollama.ipynb](extract_age_from_name_ollama.ipynb)
  - [extract_reviewer_age.ipynb](extract_reviewer_age.ipynb)

## Quarto

- Corpus listing/description: [script00_listing.qmd](script00_listing.qmd)
- Faceted analysis: [script01_facet.qmd](script01_facet.qmd)
- ABSA (Quarto version): [script02_absa.qmd](script02_absa.qmd)

## Skills demonstrated

- NLP preprocessing and multilingual filtering (French, English, Spanish, German, Portuguese, Italian)
- Dependency parsing and POS/dependency statistics with spaCy
- ABSA and sentiment workflows (BERT and local LLM-based pipelines)
- Local LLM usage (Ollama / Gemma-based analysis notebooks)
- Reproducible research workflow with Git, Git LFS, and structured outputs

## Project standards (progress and eCO2)

For consistency across all Python scripts and notebooks in this repository:

1) Progress bars for long tasks
- Use `tqdm` for any loop expected to run longer than ~30 seconds.
- Typical cases: document-level annotation, per-row NLP parsing, large exports.

2) eCO2 tracking for each script
- Each script should track total runtime and report estimated energy + eCO2.
- Default parameters used in this project:
  - `POWER_WATTS = 150`
  - `FR_GRID_KGCO2_PER_KWH = 0.056`

Minimal template:

```python
import time

POWER_WATTS = 150
FR_GRID_KGCO2_PER_KWH = 0.056
SCRIPT_START = time.perf_counter()

# ... script body ...

elapsed_sec = time.perf_counter() - SCRIPT_START
energy_kwh = (POWER_WATTS / 1000) * (elapsed_sec / 3600)
eco2_kg = energy_kwh * FR_GRID_KGCO2_PER_KWH
eco2_g = eco2_kg * 1000

print(f"Runtime: {elapsed_sec:.2f} s")
print(f"Energy: {energy_kwh*1000:.2f} Wh")
print(f"eCO2: {eco2_g:.2f} gCO2e")
```

## Current p02 outputs

The `p02` pipeline currently exports:

- Per-review aspects: [data/results_aspects_gemma3_7b_per_review.csv](data/results_aspects_gemma3_7b_per_review.csv)
- Raw summary: [data/results_aspects_gemma3_7b_summary.csv](data/results_aspects_gemma3_7b_summary.csv)
- Normalized summary (synonyms merged): [data/results_aspects_gemma3_7b_summary_normalized.csv](data/results_aspects_gemma3_7b_summary_normalized.csv)

Typical command:

```bash
python p02_aspects_gemma3_7b.py --sample-size 50 --normalize
```

Notes:
- Current model used in `p02`: `gemma3:4b`.
- `--sample-size` accepts an integer or `total`.
- The script keeps extraction robust to non-strict JSON model answers.

## Environment

This repository now uses a single Python virtual environment:

- Canonical environment folder: `.venv/`
- Duplicate folders `.venv-*` are considered deprecated and ignored.

Recommended interpreter path in VS Code:

```text
${workspaceFolder}\\.venv\\Scripts\\python.exe
```

## Copilot skill rules

Project-specific coding skill/instructions are stored in:

- [.github/copilot-instructions.md](.github/copilot-instructions.md)

## Git workflow (after each change)

1) Check changes

```bash
git status
```

2) Stage and commit

```bash
git add .
git commit -m "feat|fix|docs|chore: short message"
```

3) Push to GitHub

```bash
git push
```

### Important notes

- The local hook blocks files larger than 500 KB (except configured exceptions).
- Files `data/reviews_select.csv` and `results_*.csv` are allowed by project rules.
- Large result CSV files are handled through Git LFS (`.gitattributes`).
