# Airbnb2026

This repository contains experiments developed with Master AISO students in an applied teaching context. Airbnb corpora are explored, with Paris used as the reference dataset and extensions to other cities explorerd by student.

The project includes Python scripts for multiple NLP tasks, as well as R/Quarto scripts for statistical analysis and Beamer presentation generation.

## Python

### p01: Syntactic Analysis
- [p01_syntactic_dependency_analysis.ipynb](p01_syntactic_dependency_analysis.ipynb) - Dependency parsing and POS tagging

### p02: Topic Modeling (LDA)
- **Notebook**: [p02_lda_topic_modeling.ipynb](p02_lda_topic_modeling.ipynb)
- **Purpose**: Latent Dirichlet Allocation (LDA) for multilingual topic modeling on Airbnb reviews
- **Features**:
  - Separate LDA models for 8 major languages (en, fr, es, de, it, pt, ko, nl)
  - Automatic topic number optimization via coherence analysis (U_Mass metric)
  - Vocabulary filtering (terms appearing in ≥5 documents)
  - Extraction of phi (topic-word) and theta (document-topic) matrices with comment ID preservation
  - Runtime & energy consumption tracking

### p03-p04: Supporting Analysis
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

### p05: Aspect Extraction (Ollama Gemma 3)
- [p05_aspects_gemma3_7b.ipynb](p05_aspects_gemma3_7b.ipynb)

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

For consistency across all Python scripts and notebooks:

1) **Progress bars**: Use `tqdm` for loops expected to run > 30 seconds
2) **eCO2 tracking**: Report runtime, energy (Wh), and carbon footprint (gCO2e) at script completion
   - Default: `POWER_WATTS = 150`, `FR_GRID_KGCO2_PER_KWH = 0.056`

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
