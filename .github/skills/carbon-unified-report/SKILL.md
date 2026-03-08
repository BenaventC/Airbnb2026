# Skill: Unified Carbon Emissions Report (AirBnB_NLP4socialscience)

## Goal
Standardize carbon tracking across all scripts/notebooks so every execution appends one row to a single shared file:
- `data/carbon_emissions_report.csv`

The report must use one fixed schema and remain consistent over time.

## When to use
- User asks to add or update carbon reporting in any script/notebook.
- A pipeline currently writes carbon metrics to script-specific files.
- Carbon columns differ across scripts and need harmonization.

## Required Output File
- Single shared file: `data/carbon_emissions_report.csv`
- Encoding: `utf-8`
- One row appended per execution.

## Required Column Schema (exact names)
1. `nom du script execute`
2. `nombre d'observations traitees`
3. `date d'execution`
4. `temps d'execution`
5. `total KWatt/heure`
6. `total eco2 en grammes`

Do not rename these columns.

## Required Semantics
- `nom du script execute`: script/notebook filename (e.g., `p02_aspects_gemma3_7b.py`, `P00c_review_gender_classification2.ipynb`).
- `nombre d'observations traitees`: number of processed records in the run (int).
- `date d'execution`: timestamp at end of run, format `%Y-%m-%d %H:%M:%S`.
- `temps d'execution`: total runtime in seconds for the end-to-end run (float).
- `total KWatt/heure`: total energy consumed in kWh (float).
- `total eco2 en grammes`: total emissions in gCO2e (float).

## Computation Standard
- Power assumption: keep project-level constant already used by the script.
- Carbon intensity assumption: keep project-level constant already used by the script.
- Core formula:
  - `energy_kwh = (power_watts * runtime_seconds) / (1000 * 3600)`
  - `eco2_g = energy_kwh * carbon_intensity_g_per_kwh`

## Integration Pattern
1. Compute runtime and carbon metrics in memory.
2. Build a one-row DataFrame with exact required columns and ordering.
3. Append this row to `data/carbon_emissions_report.csv`.
4. If file exists with wrong schema, rewrite file using only the required schema before continuing.
5. Print a concise synthesis table using the same column names.

## Notebook/Script Display Requirement
At end of execution, print a synthesis table with the exact same six columns as the CSV.

## Robustness Rules
- Never use absolute paths.
- Never block the whole pipeline on report-writing errors unless explicitly requested.
- If reporting cannot be written, print a clear warning and preserve primary pipeline outputs.

## Reusable Python Snippet
```python
from datetime import datetime
import os
import pandas as pd

script_name = os.path.basename(__file__) if '__file__' in globals() else 'notebook.ipynb'
processed_observations = int(num_items)
execution_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

total_time_seconds = float(runtime_seconds)
energy_kwh = (power_watts * total_time_seconds) / (1000 * 3600)
eco2_g = energy_kwh * carbon_intensity_g_per_kwh

expected_columns = [
    'nom du script execute',
    "nombre d'observations traitees",
    "date d'execution",
    "temps d'execution",
    'total KWatt/heure',
    'total eco2 en grammes',
]

row_df = pd.DataFrame([{
    'nom du script execute': script_name,
    "nombre d'observations traitees": processed_observations,
    "date d'execution": execution_date,
    "temps d'execution": round(total_time_seconds, 2),
    'total KWatt/heure': round(float(energy_kwh), 6),
    'total eco2 en grammes': round(float(eco2_g), 2),
}], columns=expected_columns)

report_path = os.path.join('data', 'carbon_emissions_report.csv')
if os.path.exists(report_path):
    existing_df = pd.read_csv(report_path)
    if list(existing_df.columns) == expected_columns:
        final_df = pd.concat([existing_df, row_df], ignore_index=True)
    else:
        final_df = row_df.copy()
else:
    final_df = row_df.copy()

final_df.to_csv(report_path, index=False, encoding='utf-8')
print(row_df.to_string(index=False))
```

## Validation Checklist
- Run with a small sample and confirm one new row is added.
- Confirm exact column names and order in CSV.
- Confirm synthesis print matches CSV schema.
- Confirm no additional carbon CSV is created.
