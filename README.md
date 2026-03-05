# Airbnb2026

This repository contains experiments developed with Master AISO students in an applied teaching context. Airbnb corpora are explored, with Paris used as the reference dataset and extensions to other cities.

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
- **Output files** (8 languages × 4 file types):
  - `p02_lda_theta_[LANG].csv` - Document-topic distributions (with comment_id)
  - `p02_lda_phi_[LANG].csv` - Topic-word distributions
  - `p02_lda_top_words_[LANG].csv` - Top 10 terms per topic
  - `p02_lda_dominant_topics_[LANG].csv` - Dominant topic per document
  - `p02_lda_model_summary.csv` - Model metrics (vocabulary, topics, coherence, perplexity)
  - `p02_lda_topic_optimization.csv` - Coherence scores for topic number search (3-10)
  - `p02_lda_pipeline_metrics.csv` - Runtime & energy/carbon metrics

### p02 (Alternative): Aspect Extraction (Ollama Gemma 3)
- **Script**: [p02_aspects_gemma3_7b.py](p02_aspects_gemma3_7b.py)
- **Notebook**: [p02_aspects_gemma3_7b.ipynb](p02_aspects_gemma3_7b.ipynb)
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

## Current Pipeline Outputs

### p02_lda_topic_modeling.ipynb
The LDA topic modeling pipeline exports multilingual topic models:

- **Per-language theta matrices**: `data/p02_lda_theta_[LANG].csv` (8 languages)
  - Document-topic distribution with comment_id for traceability
- **Per-language phi matrices**: `data/p02_lda_phi_[LANG].csv`
  - Topic-word probability distributions
- **Top terms**: `data/p02_lda_top_words_[LANG].csv`
  - Most characteristic terms for each topic (top 10)
- **Dominant topics**: `data/p02_lda_dominant_topics_[LANG].csv`
  - Single best topic assignment per document
- **Summary metrics**: 
  - `data/p02_lda_model_summary.csv` - Vocabulary size, perplexity, coherence
  - `data/p02_lda_topic_optimization.csv` - Coherence grid search results
  - `data/p02_lda_pipeline_metrics.csv` - Runtime, energy consumption (Wh), carbon footprint (gCO2e)

**Configuration parameters:**
```python
SAMPLE_SIZE_PER_LANGUAGE = 1000      # Sample size per language
MIN_TOPICS = 3                        # Minimum topics to test
MAX_TOPICS = 10                       # Maximum topics to test
LDA_PASSES = 10                       # Number of LDA passes
LDA_ITERATIONS = 100                  # Iterations per pass
POWER_WATTS = 100                     # CPU power estimate for energy tracking
FR_GRID_KGCO2_PER_KWH = 0.06         # French grid carbon intensity
```

**Vocabulary filtering:**
- Terms appearing in < 5 documents are eliminated (reduces noise)
- Terms appearing in > 80% of documents are eliminated (reduces common words)
- Automatic language-specific stopword removal and stemming

### p02_aspects_gemma3_7b.py
The aspect extraction pipeline currently exports:

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
