# Airbnb2026

This repository contains experiments developed with [Master AISO](https://psl.eu/formation/master-intelligence-artificielle-et-societe) students in an applied teaching context. Airbnb corpora are explored, with Paris used as the reference dataset and extensions to other cities explored by students.

The project embodies a symbolist spirit: when things correspond, Large Language Models become subtle knives, cutting doors between worlds. *Inspired by Philip Pullman's "His Dark Materials" trilogy and Baudelaire's "Correspondances."* 

---

<div align="center">
  <img src="Images/leonoracarrington.jpg" alt="Leonora Carrington - Surreal Inspiration" width="320" />
  
  **Leonora Carrington** (1917–2011)  
  *Artist, feminist, ecologist & surrealist pioneer*
  
  > "Born in Lancashire, Carrington traversed worlds and consciousness—from Florence to Paris, Spain to Mexico—weaving mythology, esotericism, and human-animal metamorphoses into visionary art."
  
  📍 **Now exhibiting** at [Musée du Luxembourg](https://museeduluxembourg.fr/fr/agenda/evenement/leonora-carrington) (Feb 18 – Jul 19, 2026)
</div>

---

## Python codes


### 01: Syntactic Analysis
- [p01_syntactic_dependency_analysis.ipynb](p01_syntactic_dependency_analysis.ipynb) - Dependency parsing and POS tagging

### 02: Adjective-Noun Analysis (AMOD + t-SNE)
- **Notebook**: [p02_amod_adj_noun_tsne.ipynb](p02_amod_adj_noun_tsne.ipynb)
- **Purpose**: Extract AMOD (adjective modifying noun) relationships from syntactic annotations, compute semantic similarity, and visualize via t-SNE projection + heatmap
- **Pipeline Structure** (9 sections per skill rules):
  1. Imports & constants – Load packages, set POWER_WATTS, FR_GRID_KGCO2_PER_KWH, timer
  2. GPU detection – Automatic CUDA detection with CuPy optional acceleration (CPU fallback)
  3. Helpers – Functions for normalization, token extraction, AMOD pair discovery, distance computation
  4. Data prep – Load CSV, clean tokens, apply sampling strategy
  5. Extraction loop – Extract AMOD pairs by sentence (uses tqdm for progress)
  6. Aggregation – Crosstab ADJ × NOUN, frequency filtering (≥20), cosine distance matrix, t-SNE
  7. CSV exports – 4 output files (pairs, crosstab, distances, t-SNE coords)
  8. Energy summary – Runtime, Wh, gCO2e metrics
  9. Visualizations – t-SNE scatter (385 adjectifs) + heatmap (top 20 × 20)
- **Outputs**: 
  - `results_amod_pairs_per_review.csv` – All AMOD pairs extracted
  - `results_amod_crosstab_summary.csv` – ADJ × NOUN co-occurrence matrix
  - `results_amod_distance_summary.csv` – Cosine distance matrix (ADJ × ADJ)
  - `results_amod_tsne_summary.csv` – 2D t-SNE coordinates + frequency + noun count
- **Latest Execution** (full dataset):
  - **Input**: 3.5M annotations from reviews
  - **Extraction**: 126,965 AMOD pairs detected
  - **Filtering**: 385 adjectives (freq ≥ 20) × 3,225 nouns
  - **Runtime**: 1,119 sec (~18.6 min) on CPU
  - **Energy**: 46.62 Wh | **CO2**: 2.61 gCO2e

### 04: Topic Modeling (LDA)
- **Notebook**: [p04_lda_topic_modeling.ipynb](p04_lda_topic_modeling.ipynb)
- **Purpose**: Latent Dirichlet Allocation (LDA) for multilingual topic modeling on Airbnb reviews
- **Features**:
  - Separate LDA models for 8 major languages (en, fr, es, de, it, pt, ko, nl)
  - Automatic topic number optimization via coherence analysis (U_Mass metric)
  - Vocabulary filtering (terms appearing in ≥5 documents)
  - Extraction of phi (topic-word) and theta (document-topic) matrices with comment ID preservation
  - Runtime & energy consumption tracking

### 05-p07: Supporting Analysis
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

### 08: Aspect Extraction (Ollama Gemma 3)
- [p05_aspects_gemma3_7b.ipynb](p05_aspects_gemma3_7b.ipynb)

## Quarto

For visual presentation. (Work in progress)

- Corpus listing/description: [script00_listing.qmd](script00_listing.qmd)
- Faceted analysis: [script01_facet.qmd](script01_facet.qmd)
- ABSA (Quarto version): [script02_absa.qmd](script02_absa.qmd)

## Skills demonstrated

- NLP preprocessing and multilingual filtering (French, English, Spanish, German, Portuguese, Italian)
- Dependency parsing and POS/dependency statistics with spaCy
- ABSA and sentiment workflows (BERT and local LLM-based pipelines)
- Local LLM usage (Ollama / Gemma-based analysis notebooks)
- Reproducible research workflow with Git, Git LFS, and structured outputs
- t-SNE dimensionality reduction and semantic clustering

## Benchmark Results – Recent Runs

### AMOD Pipeline (p02) – Full Dataset Execution
| Metric | Value |
|--------|-------|
| **Input corpus** | 3.5M syntactic annotations (Airbnb reviews) |
| **AMOD pairs extracted** | 126,965 |
| **Adjectives after filtering** | 385 (freq ≥ 20) |
| **Unique nouns** | 3,225 |
| **Runtime** | 1,119 sec (~18.6 min) |
| **Energy** | 46.62 Wh |
| **CO2 footprint** | 2.61 gCO2e |
| **Hardware** | CPU only (no GPU detected in test environment) |
| **Visualizations** | t-SNE 2D projection (385 clusters), heatmap (20×20 top pairs) |

**Key Finding**: AMOD "great" dominates noun "location" (~4,000 co-occurrences), suggesting strong positive sentiment toward accommodation geography in reviews.


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

## Development Guidelines

### Pipeline Architecture

This project follows a **reproducible NLP pipeline** structured as:

1. **Data Filtering** – Language detection, deduplication, non-empty text validation
2. **Extraction** – Aspects, sentiment, syntactic features with local LLMs (Gemma/BERT)
3. **Normalization** – Optional text/label standardization
4. **Export** – CSV outputs with runtime/energy/eCO2 metrics

### Code Standards

#### Script Naming & I/O
- Prefix scripts with `pXX_` (e.g., `p05_aspects_gemma3_7b.py`)
- All input/output in `data/` folder (no hardcoded absolute paths)
- Include `--sample-size` parameter for all scripts

#### Progress & Observability
- Progress bars: `tqdm` for loops expected to run > 30 seconds
- Final output includes: runtime (seconds), energy (Wh), carbon footprint (gCO2e)
- Log timestamp and completion status

#### GPU & Parallelization
- **Detect available GPUs** via `torch.cuda.device_count()` with automatic fallback to CPU
- **Parallelize tasks** via GPU (up to 4 H100 workers) or CPU processes
- **Multiprocessing config**: Use `spawn` mode to avoid CUDA deadlocks in Jupyter (Linux)
- Per-worker logs: language, GPU#, runtime, energy consumption

#### Local LLM Integration (Ollama)
- Endpoint: `http://localhost:11434/api/generate`
- Core parameters: `model`, `prompt`, `stream=False`, `temperature`
- Error handling: Return empty output on network/JSON errors (don't crash pipelines)

#### Pipeline Structure (Notebook/Script)
Each analysis section should include a **markdown cell** explaining its purpose, followed by:
1. Imports + constants (POWER_WATTS, FR_GRID_KGCO2_PER_KWH, counters)
2. GPU detection & multiprocessing config
3. Technical helpers (progress, API calls, error handling)
4. Business logic helpers (parsing, normalization, entity extraction)
5. Sample preparation (filtering, deduplication)
6. Main processing loop (GPU/CPU-parallelized)
7. Aggregation & statistics (by language/model/device)
8. CSV exports (per-review + summary files)
9. Runtime summary (duration, energy, eCO2, end timestamp)

#### Output Format
- Per-review: `data/results_*_per_review.csv`
- Summary: `data/results_*_summary.csv`
- Normalized summary (optional): `data/results_*_summary_normalized.csv`
- Encoding: `utf-8` (always)

#### Validation Checklist
- ✓ Script runs on `--sample-size 5`
- ✓ Output columns are stable and documented
- ✓ No hidden kernel state dependencies
- ✓ Reproducible with same parameters
- ✓ Each section has mandatory explanatory markdown (2-3 sentences)
- ✓ GPU/CPU branching with fallback implemented
- ✓ Final outputs include runtime/energy/eCO2 metrics

---

**Full project conventions and detailed rules:**  
→ [.github/copilot-instructions.md](.github/copilot-instructions.md)
