# Skill: Mermaid Pipeline Diagram Style (AirBnB_NLP4socialscience)

## Goal
Generate consistent Mermaid pipeline diagrams for notebooks/scripts with a clean white background and pastel blocks.

## When to use
- Any new pipeline notebook/script section intro
- Any request to add a workflow/flowchart diagram
- Any update to existing Mermaid diagrams for readability

## Required Layout Rules
1. Use `flowchart LR` for the global layout.
2. Build exactly 3 main blocks (subgraphs):
   - `DATA INPUTS` (blue group)
   - `INTERNAL PROCESSING` (yellow group)
   - `OUTPUTS` (green group)
3. Main blocks should be arranged horizontally (left to right).
4. Nodes inside each block should be arranged vertically (`direction TB`).

## Required Visual Style
- Utiliser la **palette de référence du projet** (voir `.github/skills/color-palette-management/SKILL.md`).
- Fond crème `#EFEBCE`, blocs pastel chauds, flèches terracotta.
- Labels courts orientés action.

### Base Mermaid init to reuse
```mermaid
%%{init: {'theme': 'base', 'flowchart': { 'nodeSpacing': 18, 'rankSpacing': 20, 'diagramPadding': 6 }, 'themeVariables': { 'primaryColor': '#EFEBCE', 'primaryBorderColor': '#D8A48F', 'background': '#EFEBCE', 'mainBkg': '#EFEBCE', 'clusterBkg': '#EFEBCE', 'lineColor': '#D8A48F', 'edgeLabelBackground':'#EFEBCE'}} }%%
```

### Group colors
- Input group: `fill:#D7CE93, stroke:#A3A381, color:#3E3A33`
- Process group: `fill:#EFEBCE, stroke:#D7CE93, color:#3E3A33`
- Output group: `fill:#D8A48F, stroke:#BB8487, color:#3E3A33`

### Arrow style
```mermaid
linkStyle default stroke:#D8A48F,stroke-width:2px,color:#BB8487
```

## Recommended Node Text Pattern
- Verb + object, max 2 lines where possible
- Examples:
  - `Load Reviews`
  - `Filter Last Year`
  - `Clean Comments`
  - `Export CSV`

## Reusable Template
```mermaid
%%{init: {'theme': 'base', 'flowchart': { 'nodeSpacing': 18, 'rankSpacing': 20, 'diagramPadding': 6 }, 'themeVariables': { 'primaryColor': '#ffffff', 'primaryBorderColor': '#d9d9d9', 'background': '#ffffff', 'mainBkg': '#ffffff', 'clusterBkg': '#ffffff', 'lineColor': '#cfd8dc', 'edgeLabelBackground':'#ffffff'}} }%%
flowchart LR
  subgraph Row[" "]
    direction LR

    subgraph Input["DATA INPUTS"]
      direction TB
      A["Input 1"]
      B["Input 2"]
      A --- B
    end

    subgraph Process["INTERNAL PROCESSING"]
      direction TB
      C["Step 1"]
      D["Step 2"]
      E["Step 3"]
      C --> D --> E
    end

    subgraph Output["OUTPUTS"]
      direction TB
      F["Output 1"]
      G["Output 2"]
      F --> G
    end
  end

  A -->|Load| C
  B -->|Join| E
  E -->|Export| F

  style Row fill:#EFEBCE,stroke:#EFEBCE,color:#EFEBCE
  linkStyle default stroke:#D8A48F,stroke-width:2px,color:#BB8487
  style Input fill:#D7CE93,stroke:#A3A381,stroke-width:3px,color:#3E3A33
  style Process fill:#EFEBCE,stroke:#D7CE93,stroke-width:3px,color:#3E3A33
  style Output fill:#D8A48F,stroke:#BB8487,stroke-width:3px,color:#3E3A33
```
