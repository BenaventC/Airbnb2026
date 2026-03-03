# Airbnb2026

This repository contains experiments developed with Master AISO students in an applied teaching context. Airbnb corpora are explored, with Paris used as the reference dataset and extensions to other cities.

The project includes Python scripts for multiple NLP tasks, as well as R/Quarto scripts for statistical analysis and Beamer presentation generation.

## Python

- Syntactic annotation: [p01_syntactic_dependency_analysis.ipynb](p01_syntactic_dependency_analysis.ipynb)
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
