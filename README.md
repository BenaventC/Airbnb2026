# Airbnb2026

This repository contains experiments developed with [Master AISO](https://psl.eu/formation/master-intelligence-artificielle-et-societe) students in an applied teaching context. Airbnb corpora are explored, with Paris used as the reference dataset and extensions to other cities explored by students.

The project embodies a symbolist spirit: when things correspond, Large Language Models become subtle knives, cutting doors between worlds. *Inspired by Philip Pullman's "His Dark Materials" trilogy and Baudelaire's "Correspondances."* 

---

<div align="center">
  <img src="Images/leonoracarrington.jpg" alt="Leonora Carrington - Surreal Inspiration" width="320" />
  
  **Leonora Carrington** (1917–2011)  
  *Artist, feminist, ecologist & surrealist pioneer*
  
  > "Born in Lancashire, Carrington traversed continents and consciousness—from Florence to Paris, Spain to Mexico—weaving mythology, esotericism, and human-animal metamorphoses into radical visionary art."
  
  📍 **Now exhibiting** at [Musée du Luxembourg](https://museeduluxembourg.fr/fr/agenda/evenement/leonora-carrington) (Feb 18 – Jul 19, 2026)
</div>

---

## Python

### p01: Syntactic Analysis
- [p01_syntactic_dependency_analysis.ipynb](p01_syntactic_dependency_analysis.ipynb) - Dependency parsing and POS tagging

### p02: Adjective-Noun Analysis (TSNE)
- **Notebook**: [p02_amod_adj_noun_tsne.ipynb](p02_amod_adj_noun_tsne.ipynb)
- **Purpose**: TSNE clustering and visualization of adjective-noun relationships from syntactic dependencies
- **Script**: [p02_amod_adj_noun_tsne.py](p02_amod_adj_noun_tsne.py) - Main extraction and TSNE computation
- **Outputs**: Cross-tabulations, distance matrices, and TSNE embedding summaries

### p04: Topic Modeling (LDA)
- **Notebook**: [p04_lda_topic_modeling.ipynb](p04_lda_topic_modeling.ipynb)
- **Purpose**: Latent Dirichlet Allocation (LDA) for multilingual topic modeling on Airbnb reviews
- **Features**:
  - Separate LDA models for 8 major languages (en, fr, es, de, it, pt, ko, nl)
  - Automatic topic number optimization via coherence analysis (U_Mass metric)
  - Vocabulary filtering (terms appearing in ≥5 documents)
  - Extraction of phi (topic-word) and theta (document-topic) matrices with comment ID preservation
  - Runtime & energy consumption tracking

### p05-p07: Supporting Analysis
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
- ✓ Each section has explanatory markdown
- ✓ GPU/CPU branching with fallback implemented

---

**Full project conventions and detailed rules:**  
→ [.github/copilot-instructions.md](.github/copilot-instructions.md)
