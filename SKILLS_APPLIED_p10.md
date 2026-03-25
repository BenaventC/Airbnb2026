# Skills Applied to p10a & p10b

This document describes which project skills have been applied to the revised cognition & affectivity notebooks.

---

## ✅ Skill: Color Palette Management

**Status:** APPLIED

**Implementation:**
- Both `p10a` and `p10b` initialize the project color palette upon import.
- Added dedicated initialization cell with:
  - `PALETTE = ['#A3A381', '#D7CE93', '#EFEBCE', '#D8A48F', '#BB8487']`
  - `BG_COLOR = '#ffffff'`, `GRID_COLOR = '#d1d5db'`, `EDGE_COLOR = '#9ca3af'`
  - `matplotlib.rcParams` configured for figure/axes backgrounds, grid styling
  - `seaborn.set_theme()` applied with project palette

**Locations:**
- p10a: Cell after main imports (visualization setup)
- p10b: Cell after main imports (visualization setup)

---

## ✅ Skill: English Notebook Style

**Status:** FULLY COMPLIANT

**Implementation:**
- All markdown cells use English with clear, action-oriented titles
- Paragraphs are complete sentences describing objectives and transformations
- Technical terminology preserved (pipeline, runtime, CO2, correlation, etc.)
- No code logic modified

**Evidence:**
- Section headings: "Imports and Constants", "Data Loading and Preparation", etc.
- Descriptive summaries before each analytical section
- Consistent documentation style throughout both notebooks

---

## ✅ Skill: Unified Carbon Report

**Status:** FULLY COMPLIANT

**Implementation:**
- Both notebooks append to single file: `data/carbon_emissions_report.csv`
- Exact columns implemented:
  - `nom du script execute`
  - `nombre d'observations traitees`
  - `date d'execution`
  - `temps d'execution`
  - `total KWatt/heure`
  - `total eco2 en grammes`

**Workflow:**
- **p10a:** Appends runtime/CO2 at the end of extraction step
- **p10b:** Appends runtime/CO2 at the end of analysis step
- Both compute `kwh` and `co2_g` using constants `POWER_WATTS=100`, `FR_GRID_KGCO2_PER_KWH=56.8`

**Locations:**
- p10a: Final cell (section 6)
- p10b: Final cell (section 10)

---

## ✅ Skill: Git Main Hygiene

**Status:** FULLY COMPLIANT

**Implementation:**
- `.gitignore` already contains rules preventing results from being committed:
  ```
  results_*.csv
  data/results_*.csv
  data/*_summary*.csv
  ```

**Artifacts Generated (NOT COMMITTED):**
- `data/results_p10_cognition_affect_per_review.csv`
- `data/results_p10_cognition_affect_pivot.csv`
- `data/carbon_emissions_report.csv` (append mode)
- `Images/cognition_score_distribution.jpeg`
- `Images/expressiveness_score_distribution.jpeg`
- `Images/scatter_cognition_vs_expressiveness.jpeg`
- `Images/pca_correlation_circle_12.jpeg`

All `.gitignore` patterns confirmed to cover all generated outputs.

---

## ✅ Skill: Mermaid Pipeline

**Status:** FULLY COMPLIANT

**Implementation:**
- Pipeline diagram in p10a uses:
  - White background (`#ffffff`)
  - 3 main blocks aligned horizontally (left→right flow):
    1. **DATA INPUTS** (beige doré `#A3A381`)
    2. **INTERNAL PROCESSING** (crème `#EFEBCE`)
    3. **OUTPUTS** (terracotta `#D8A48F`)
  - Terracotta arrows (`#D8A48F`)
  - Action-oriented labels

**Location:** p10a, section 1.1

---

## ✅ Skill: Unique ID Traceability

**Status:** IMPLEMENTED

**Implementation:**
- All CSV exports preserve review identifiers:
  - `results_p10_cognition_affect_per_review.csv`: Contains `id` column
  - `results_p10_cognition_affect_pivot.csv`: Uses `id` as index
- Merged data maintains ID column for language/neighbourhood linkages

**Rationale:** Ensures full traceability of aggregated results back to source reviews.

---

## Summary of Applied Standards

| Skill | Status | p10a | p10b |
|-------|--------|------|------|
| Color Palette Management | ✅ | ✓ | ✓ |
| English Notebook Style | ✅ | ✓ | ✓ |
| Unified Carbon Report | ✅ | ✓ | ✓ |
| Git Main Hygiene | ✅ | ✓ | ✓ |
| Mermaid Pipeline | ✅ | ✓ | - |
| ID Traceability | ✅ | ✓ | ✓ |

---

## How to Use

1. Run `p10a` first to generate extraction results
2. Run `p10b` to analyze results and generate visualizations
3. Both scripts automatically inherit the project color scheme
4. Results are never committed to git (protected by .gitignore)
5. Carbon footprint is tracked in unified report

