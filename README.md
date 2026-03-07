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


### 01: Syntactic Dependency Analysis with spaCy
- **Notebook**: [p01_syntactic_dependency_analysis.ipynb](p01_syntactic_dependency_analysis.ipynb)
- **Purpose**: Multilingual syntactic dependency parsing and POS tagging using spaCy across 6 languages (French, English, Spanish, German, Portuguese, Italian). Extracts lemmas, universal POS tags, syntactic relations, and dependency trees from Airbnb reviews with GPU-accelerated parallel processing.
- **Pipeline Structure** (9 sections per skill rules):
  1. **Dependency Installation** – Install GPU-compatible packages (numpy, pandas, spaCy 3.8.7, CuPy, thinc)
  2. **Download spaCy Models** – Fetch multilingual models (fr_core_news_sm, en_core_web_sm, etc.) for each language
  3. **Imports & Constants** – Load modules, initialize POWER_WATTS (150W), FR_GRID_KGCO2_PER_KWH (0.056), timer, sample size parameter
  4. **Language Distribution Analysis** – Quick diagnostic of linguistic coverage across corpus
  5. **Load spaCy Models** – Verify model availability, prepare nlp_models dictionary
  6. **Sample Preparation** – Filter by supported languages, remove empty texts, apply Sample_Size parameter (int or "total")
  7. **GPU Detection & Multiprocessing** – Detect CUDA count, assign tasks to GPU workers (up to 4 H100), set multiprocessing spawn mode, fallback CPU
  8. **Syntactic Extraction Loop** – Parallel dependency parsing per language using nlp.pipe with batch processing (tqdm progress)
  9. **Aggregation & Statistics** – Consolidate POS distributions, dependency relations, ROOT verbs by language
  10. **CSV Export** – Write token-level annotations in CoNLL-U format with metadata enrichment
  11. **Summary Tables** – Generate text summary of top POS/DEP by language + syntactic statistics table
  12. **ROOT Verb Analysis** – Extract and rank main verbs per language
  13. **Final Report** – Runtime, energy, CO2 emissions with end timestamp
- **Outputs**:
  - `results_reviews_select_annotations.csv` – Token-by-token annotations (form, lemma, upos, xpos, head, deprel, sent_id, etc.)
  - Summary tables in console output (POS by language, DEP by language, ROOT verbs)
  - Relative distribution tables (POS/DEP as rows × languages as columns)
- **Key Features**:
  - **GPU-accelerated parsing** – Automatic CUDA device assignment per language task
  - **Fallback to CPU** – Seamless CPU processing if no CUDA detected
  - **Multilingual coverage** – 6 major languages with language-specific tokenization & parsing
  - **CoNLL-U format** – Standard syntactic annotation format for downstream NLP tools
  - **Energy tracking** – Full carbon accounting (POWER_WATTS, FR_GRID emissions factor)
- **Sample Execution** (typical run):
  - **Input**: Full corpus (results_reviews_enriched_per_review.csv)
  - **Sample method**: Sample_Size = 'total' or integer limit
  - **Languages processed**: en, fr, es, de, it, pt (depends on corpus)
  - **Tokens annotated**: Millions (per full run)
  - **Runtime**: ~2–5 min (GPU) or 10–20 min (CPU) depending on sample size
  - **Energy**: ~15–40 Wh
  - **CO2**: ~0.8–2.2 gCO2e

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

1. **Mandatory markdown documentation**: Each major section (especially the 9 core pipeline sections) MUST have an **explanatory markdown cell immediately below its title** describing in 2–3 simple sentences:
   - **What this step accomplishes** (active verbs, plain language)
   - **Key data transformations** (input/output variables)
   - ✓ Good: *"Load CSV, clean data (remove empty tokens, normalize), create sample to process"*
   - ✗ Bad: *"Process data section"*

2. **Progress bars**: Use `tqdm` for loops expected to run > 30 seconds
   - Fallback: simple counter prints if tqdm unavailable

3. **eCO2 tracking**: Report at script completion:
   - Runtime (seconds)
   - Energy (Wh) → calculated as `(POWER_WATTS / 1000) × (duration_sec / 3600) × 1000`
   - Carbon footprint (gCO2e) → calculated as `energy_kwh × FR_GRID_KGCO2_PER_KWH × 1000`
   - Default constants: `POWER_WATTS = 150`, `FR_GRID_KGCO2_PER_KWH = 0.056` (France mix)
   - Execution end timestamp (ISO 8601 format)

4. **Sample size parameter**: All scripts must accept `--sample-size` (or load from variable/widget):
   - Integer → process that many reviews
   - `"total"` → process entire filtered dataset

5. **GPU & CPU detection**:
   - Detect available GPUs via `torch.cuda.device_count()` (with `nvidia-smi` fallback)
   - Assign tasks to GPU workers (up to 4 H100), fallback CPU if unavailable
   - Multiprocessing mode: `spawn` (avoids CUDA deadlocks in Jupyter)

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
- **Naming convention**: Prefix scripts/notebooks with `pXX_` (e.g., `p01_syntactic_dependency_analysis.ipynb`, `p08_aspects_gemma3_7b.py`)
- **Input/Output**: All data flows through `data/` folder (no hardcoded absolute paths)
- **Sample parameter**: Every script MUST include `Sample_Size` (Jupyter variable) or `--sample-size` CLI argument (int or `"total"`)

#### Observability & Logging
- **Progress tracking**: Use `tqdm` for any loop expected to run > 30 seconds (shows estimated time remaining)
  - Fallback: Fallback plain `print()` counter if tqdm unavailable
- **Final report** (printed at script completion):
  - Elapsed time (seconds)
  - Energy consumption (Wh)
  - Carbon footprint (gCO2e, using FR grid mix by default)
  - Execution end timestamp (ISO 8601 format: `YYYY-MM-DD HH:MM:SS`)

#### Parallelization & GPU
- **GPU detection**: Automatically detect available CUDA devices via `torch.cuda.device_count()` 
  - Fallback: Use `nvidia-smi -L` if torch unavailable
  - Fallback: Gracefully degrade to CPU if no GPUs detected
- **Task assignment**: Assign language/entity tasks to GPU workers (up to 4 H100 per machine)
  - Per-worker logging: Display language, device ID, runtime, and energy per task
- **Multiprocessing config**: Use `mp.set_start_method('spawn', force=True)` to avoid CUDA deadlocks in Jupyter (Linux/WSL)

#### Local LLM Integration (Ollama)
- **Ollama service**: Assumes running on `http://localhost:11434`
- **Endpoint**: `http://localhost:11434/api/generate`
- **Call parameters**: 
  - `model` (required) – e.g., `"gemma:7b"`
  - `prompt` (required) – instruction + input text
  - `stream` (always `False` in pipeline)
  - `temperature` – 0.0–1.0 (default: 0.7)
- **Error handling**: Catch network/timeout errors and return empty result rather than crashing pipeline
  - Log the error for debugging but allow script to continue
  - Use timeout (~30s per request) to prevent hung processes

#### Pipeline Structure (Notebook/Script)
Each analysis section should include a **mandatory markdown cell** explaining its purpose (2–3 sentences), followed by implementation code:

**Core 9 sections** (after data/environment setup):
1. **Imports + constants** – Load packages, initialize POWER_WATTS (150W), FR_GRID_KGCO2_PER_KWH (0.056), timer counters, LLM models/API keys
2. **GPU detection & parallelization** – Detect available GPUs via `torch.cuda.device_count()` or `nvidia-smi`, configure `multiprocessing.spawn()` mode, assign tasks to GPU workers (up to 4 H100), fallback CPU if none available
3. **Technical helpers** – Functions for progress bars (tqdm), API calls, network error handling
4. **Business logic helpers** – Parsing, normalization, entity extraction, language-specific processing
5. **Sample preparation** – Filter by supported languages, remove empty texts, apply deduplication, respect Sample_Size parameter
6. **Main extraction loop** – Parallelize via GPU/CPU workers, use tqdm for progress tracking (>30 sec loops)
7. **Aggregation & statistics** – Consolidate results by language/model/device, compute relative distributions, top-N rankings
8. **CSV exports** – Write per-review file (`results_*_per_review.csv`) and summary file (`results_*_summary.csv`)
9. **Runtime summary** – Print duration (seconds), energy (Wh), CO2 (gCO2e), execution end timestamp

**Pre-pipeline setup** (if needed):
- Dependency installation (pip packages)
- Model downloads (spaCy, LLM weights, etc.)
- Configuration files (.env, API keys)

#### Output Format
- Per-review: `data/results_*_per_review.csv`
- Summary: `data/results_*_summary.csv`
- Normalized summary (optional): `data/results_*_summary_normalized.csv`
- Encoding: `utf-8` (always)

#### Validation Checklist
Before submitting a notebook/script for review, verify:

- ✓ **Script naming**: Follows `pXX_descriptive_name.ipynb` pattern (e.g., `p01_syntactic_dependency_analysis.ipynb`)
- ✓ **Execution on small sample**: Runs successfully on `--sample-size 5` (or `Sample_Size = 5`)
- ✓ **Output columns stable**: CSV column names and order are documented and consistent across runs
- ✓ **No hidden kernel state**: Script doesn't depend on cells executed "out of order" or hidden state from interactive Jupyter
- ✓ **Reproducible**: Same input + same parameters → identical output
- ✓ **Mandatory markdown documentation**: Every section title has explanatory markdown cell (2–3 sentences) below it
- ✓ **GPU/CPU detection & fallback**: GPU detection implemented with automatic CPU fallback
- ✓ **Progress tracking**: Long-running loops (>30s) show tqdm progress bar
- ✓ **Final runtime report**: Prints duration (sec), energy (Wh), CO2 (gCO2e), and end timestamp
- ✓ **CSV encoding**: All exports use `utf-8` encoding
- ✓ **Data paths**: No hardcoded absolute paths; all I/O uses `data/` folder
- ✓ **Sample size parameter**: Script respects `Sample_Size` / `--sample-size` argument

---

**Full project conventions and detailed rules:**  
→ [.github/copilot-instructions.md](.github/copilot-instructions.md)
