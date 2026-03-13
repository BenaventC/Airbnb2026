# Skill: Color Palette Management (AirBnB_NLP4socialscience)

## Goal
Apply and maintain a unified reference color palette across all notebooks, Quarto scripts, and Mermaid diagrams in the project.

## When to use
- Any new notebook or script that includes plots, charts, or diagrams
- Any request to harmonize or update colors visually
- Any Mermaid diagram creation or update
- When adding new visualizations (Python/R/Mermaid)

---

## Reference Palette

| Role | Hex | Description |
|---|---|---|
| Primary / sage green | `#A3A381` | Main bars, lines, Input fill border, `palette[0]` |
| Secondary / golden beige | `#D7CE93` | Input fill, grid lines, `palette[1]` |
| Background / pale cream | `#EFEBCE` | Figure/axes background, Process fill, `palette[2]` |
| Accent / terracotta | `#D8A48F` | Highlights, Output fill, axis edges, links, `palette[3]` |
| Accent / muted rose | `#BB8487` | Linetype accents, Output border, `palette[4]` |
| Text / dark warm brown | `#3E3A33` | Labels, annotations (derived, not in palette array) |

---

## Python (Matplotlib / Seaborn)

### Required constants (at top of every notebook)
```python
PALETTE = ['#A3A381', '#D7CE93', '#EFEBCE', '#D8A48F', '#BB8487']
PALETTE_SEQ = ['#EFEBCE', '#D7CE93', '#A3A381', '#D8A48F', '#BB8487']
BG_COLOR   = '#EFEBCE'
GRID_COLOR = '#D7CE93'
EDGE_COLOR = '#D8A48F'
TEXT_COLOR = '#3E3A33'

import matplotlib as mpl
mpl.rcParams.update({
    'figure.facecolor': BG_COLOR,
    'axes.facecolor':   BG_COLOR,
    'axes.edgecolor':   EDGE_COLOR,
    'axes.labelcolor':  TEXT_COLOR,
    'xtick.color':      TEXT_COLOR,
    'ytick.color':      TEXT_COLOR,
    'grid.color':       GRID_COLOR,
})
import seaborn as sns
sns.set_theme(style='whitegrid', palette=PALETTE)
```

### Typical assignments
- Single-color bar: `color='#A3A381'`
- Histogram: `color='#D7CE93'`, KDE line: `color='#BB8487'`
- Diverging gradient (low → mid → high): `#BB8487` → `#EFEBCE` → `#A3A381`
- Sequential gradient (low → high): `#EFEBCE` → `#A3A381`

---

## R (ggplot2 / Quarto scripts)

### Required constant
```r
pal_b <- c("#A3A381", "#D7CE93", "#EFEBCE", "#D8A48F", "#BB8487")
```

### Theme setup
```r
theme_set(
  theme_minimal(base_size = 11) +
    theme(
      plot.background  = element_rect(fill = "#EFEBCE", color = NA),
      panel.background = element_rect(fill = "#EFEBCE", color = NA),
      panel.grid.major = element_line(color = "#D7CE93"),
      axis.line        = element_line(color = "#D8A48F")
    )
)
```

### Scales
- Discrete fill/color: `scale_fill_manual(values = pal_b)` / `scale_color_manual(values = pal_b)`
- Diverging gradient: `scale_color_gradient2(low="#D8A48F", mid="#D7CE93", high="#A3A381")`
- Sequential gradient: `scale_color_gradient(low="#BB8487", high="#A3A381")`

---

## Mermaid Diagrams

### Required init block
```
%%{init: {'theme': 'base', 'flowchart': { 'nodeSpacing': 18, 'rankSpacing': 20, 'diagramPadding': 6 }, 'themeVariables': { 'primaryColor': '#EFEBCE', 'primaryBorderColor': '#D8A48F', 'background': '#EFEBCE', 'mainBkg': '#EFEBCE', 'clusterBkg': '#EFEBCE', 'lineColor': '#D8A48F', 'edgeLabelBackground':'#EFEBCE'}} }%%
```

### Required block styles
```
style Row fill:#EFEBCE,stroke:#EFEBCE,color:#EFEBCE
style Input fill:#D7CE93,stroke:#A3A381,stroke-width:3px,color:#3E3A33
style Process fill:#EFEBCE,stroke:#D7CE93,stroke-width:3px,color:#3E3A33
style Output fill:#D8A48F,stroke:#BB8487,stroke-width:3px,color:#3E3A33
linkStyle default stroke:#D8A48F,stroke-width:2px,color:#BB8487
```

---

## Bulk replacement rules (when migrating old palettes)

| Old color | → New color | Role |
|---|---|---|
| `#98CFC2`, `#70B4A3`, `#B8D39E` | `#A3A381` | sage |
| `#F4C5CF`, `#E4D8CC` | `#D7CE93` | beige |
| `#FBF5EE` | `#EFEBCE` | cream |
| `#D4A33F`, `#E99288`, `#D8C6B5` | `#D8A48F` | terracotta |
| `#C75146`, `#BA443C` | `#BB8487` | rose |
| `#ffffff` (Mermaid only) | `#EFEBCE` | background |
| `#cfd8dc`, `#d9d9d9` (Mermaid only) | `#D8A48F` | lines/borders |
| `#90a4ae` (Mermaid only) | `#BB8487` | link labels |
| `#E8F4F8,stroke:#B0D4E3,...color:#0d47a1` (Input) | `#D7CE93,stroke:#A3A381,...color:#3E3A33` | Mermaid Input |
| `#FFF9E6,stroke:#FFE082,...color:#F57F17` (Process) | `#EFEBCE,stroke:#D7CE93,...color:#3E3A33` | Mermaid Process |
| `#E8F5E9,stroke:#A5D6A7,...color:#1B5E20` (Output) | `#D8A48F,stroke:#BB8487,...color:#3E3A33` | Mermaid Output |
