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

| Notebook | Purpose | Output |
|----------|---------|--------|
| **p00f** [Review Data Preparation](p00f_prepare_data.ipynb) | Last-year filtering, comment cleaning (`<br/>` replacement), `id` standardization, language detection, listing enrichment | `data/reviews_prepared.csv` (review-level enriched dataset) |
| **p01** [Syntactic Dependency](p01_syntactic_dependency_analysis.ipynb) | Multilingual POS tagging & dependency parsing (6 languages, GPU-accelerated) | Token annotations (CoNLL-U format) |
| **p02** [AMOD + t-SNE](p02_amod_adj_noun_tsne.ipynb) | Extract adjective-noun relations, semantic clustering | ADJ×NOUN crosstab, t-SNE projection |
| **p03** [BERT Sentiment](p03_bert_sentiment_analysis.ipynb) | Sentiment classification (multi-label) | Sentiment scores per review |
| **p04** [LDA Topics](p04_lda_topic_modeling.ipynb) | Multilingual topic modeling (8 languages) | Topic distributions, phi/theta matrices |
| **Gender, ABSA, Age** | Supporting notebooks (gender from names, aspect extraction, age estimation) | Classifier outputs, aspect scores |
| **p08-p09** [Aspect + ABSA](p08_aspects_gemma3_7b.ipynb) | Aspect extraction & ABSA using Ollama Gemma3 | Aspects, sentiments, probabilities |

## Quarto Reports
- [script00_listing.qmd](script00_listing.qmd) – Corpus description & statistics
- [script01_facet.qmd](script01_facet.qmd) – Faceted analysis by neighborhood/timeframe
- [script02_absa.qmd](script02_absa.qmd) – ABSA visualization

## Skills Demonstrated
- Multilingual NLP (French, English, Spanish, German, Portuguese, Italian)
- Dependency parsing & POS tagging with spaCy
- Sentiment analysis (BERT) & aspect-based sentiment (ABSA)
- Local LLM workflows (Ollama/Gemma)
- Topic modeling (LDA)
- Dimensionality reduction (t-SNE)
- Data preparation pipelines (cleaning, language detection, metadata enrichment)
- Reproducible research (Git, Git LFS, energy tracking)

## Repository Skills
- **Mermaid Pipeline Style**: standardized white-background pastel Mermaid flowcharts with three blocks (`DATA INPUTS`, `INTERNAL PROCESSING`, `OUTPUTS`) and vertical node stacks in each block.
- **English Notebook Style**: full markdown translation and editorial rewrite in polished English with elegant headings and technically faithful wording.

Both skills are documented in:
- `.github/skills/mermaid-pipeline/SKILL.md`
- `.github/skills/english-notebook-style/SKILL.md`


## Project Standards

All scripts follow reproducible NLP pipeline principles with energy tracking:

1. **Naming & I/O**: Scripts prefixed `pXX_` (e.g., `p01_syntactic_dependency_analysis.ipynb`). All data flows through `data/` folder.
2. **Sample parameter**: Every script must accept `Sample_Size` (int or `"total"`).
3. **Progress tracking**: Use `tqdm` for loops >30s; print `(runtime sec, energy Wh, CO2 gCO2e, end timestamp)`.
4. **GPU/CPU**: Auto-detect CUDA devices; assign tasks to ≤4 GPU workers; fallback CPU if none available.
5. **Markdown documentation**: Each major section title must have explanatory markdown (2–3 sentences) below it describing objective & transformations.
6. **Ollama integration** (local LLM): Call `http://localhost:11434/api/generate` with `stream=False`; catch network errors gracefully.
7. **Output format**: Per-review `results_*_per_review.csv` + summary `results_*_summary.csv` (utf-8 encoding)

## Environment
Python virtual environment: `.venv/` (canonical folder; `.venv-*` folders are deprecated)

VS Code interpreter: `${workspaceFolder}\.venv\Scripts\python.exe`

## Development Guidelines

### Core Pipeline Structure (10 Sections)
1. Imports + constants (`POWER_WATTS=350`, `FR_GRID_KGCO2_PER_KWH=0.0502`, timers, models)
2. GPU detection & multiprocessing (torch.cuda.device_count(), mp.spawn())
3. Technical helpers (progress bars, API calls, error handling)
4. Business helpers (parsing, normalization, entity extraction)
5. Sample preparation (filter languages, remove empty texts, apply Sample_Size)
6. Main extraction loop (parallelize via GPU/CPU, tqdm progress)
7. Aggregation & statistics (consolidate results, compute distributions)
8. Optional enrichment (e.g., left join with `listings.csv` before export)
9. CSV exports (per-review + summary files, utf-8)
10. Runtime summary (duration, Wh, gCO2e, end timestamp)

### Code Standards
- **GPU/CPU branching**: Auto-detect CUDA devices; assign up to 4 H100 workers per task; CPU fallback
- **Ollama integration**: Endpoint `http://localhost:11434/api/generate` with `stream=False`; timeout ~30s
- **Reproducibility**: Same input + params → identical output; no hidden kernel state
- **Validation**: Runs on `Sample_Size=5`; stable CSV columns; documented CI/CD friendly

See [.github/copilot-instructions.md](.github/copilot-instructions.md) for full detailed specifications.
