# %% [markdown]
# # P13 - Named Entity Extraction for Places in Airbnb Reviews
# This script extracts location-related named entities from `data/reviews_select.csv` using Ollama with a Gemma model.
# It keeps review identifiers for traceability and exports both per-review results and aggregate summaries in UTF-8 CSV files.

# %% [markdown]
# ## 1. Imports and Constants
# This section initializes dependencies, runtime constants, and output paths.
# It also sets carbon accounting constants used in the final reporting block.

# %%
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Tuple

import pandas as pd
import requests
from tqdm import tqdm

DATA_DIR = "data"
INPUT_CSV = os.path.join(DATA_DIR, "reviews_select.csv")
OUTPUT_PER_REVIEW = os.path.join(DATA_DIR, "results_p13_ner_per_review.csv")
OUTPUT_SUMMARY = os.path.join(DATA_DIR, "results_p13_ner_summary.csv")
CARBON_REPORT = os.path.join(DATA_DIR, "carbon_emissions_report.csv")
CARBON_HOURLY = os.path.join(DATA_DIR, "carbon_hourly_summary.csv")

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gemma3:4b"

POWER_WATTS = 350
FR_GRID_KGCO2_PER_KWH = 0.0502

ALLOWED_LABELS = ["PLACE", "STREET", "LANDMARK", "MUSEUM", "RESTAURANT"]


# %% [markdown]
# ## 2. GPU Detection and Runtime Branching
# This section detects available GPUs and configures safe multiprocessing behavior.
# If no GPU is found, the script falls back to CPU and still runs the extraction pipeline.

# %%
def _detect_gpu_count() -> int:
    try:
        import torch  # type: ignore

        if torch.cuda.is_available():
            return int(torch.cuda.device_count())
    except Exception:
        pass

    try:
        res = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            check=False,
            capture_output=True,
            text=True,
        )
        if res.returncode == 0 and res.stdout.strip():
            return len([line for line in res.stdout.splitlines() if line.strip()])
    except Exception:
        pass

    return 0


def configure_runtime(max_workers_arg: int) -> Tuple[int, str]:
    try:
        mp.set_start_method("spawn", force=True)
    except RuntimeError:
        pass

    gpu_count = _detect_gpu_count()
    mode = "GPU" if gpu_count > 0 else "CPU"

    cpu_count = os.cpu_count() or 4
    if max_workers_arg > 0:
        workers = max_workers_arg
    elif gpu_count > 0:
        workers = min(max(2, gpu_count * 2), cpu_count)
    else:
        workers = min(8, cpu_count)

    return workers, mode


# %% [markdown]
# ## 3. Technical Helpers
# This section provides resilient API calls and parsing helpers.
# It ensures network or JSON errors do not crash the full run and returns empty extraction when needed.

# %%
def _strip_code_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned)
    return cleaned.strip()


def _extract_first_json_block(text: str) -> str:
    text = _strip_code_fences(text)
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return "[]"


def call_ollama_ner(model: str, prompt: str, temperature: float, timeout_s: int = 120) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": temperature,
    }
    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=timeout_s)
        response.raise_for_status()
        data = response.json()
        return str(data.get("response", "")).strip()
    except Exception:
        return ""


# %% [markdown]
# ## 4. Business Helpers for NER
# This section defines the extraction prompt and normalizes model output.
# The output is restricted to a small controlled schema to simplify downstream CSV exports.

# %%
def build_ner_prompt(comment: str) -> str:
    safe_comment = str(comment or "").strip()[:2500]
    return (
        "Extract location-related named entities from the review text.\n"
        "Return ONLY a JSON array. No explanation.\n"
        "Each item must be an object with keys: entity, label.\n"
        "Allowed labels: PLACE, STREET, LANDMARK, MUSEUM, RESTAURANT.\n"
        "Rules:\n"
        "- Keep original surface form in entity.\n"
        "- Remove duplicates.\n"
        "- If none found, return [] exactly.\n"
        "Example: [{\"entity\":\"Rue de Rivoli\",\"label\":\"STREET\"}]\n\n"
        f"Review:\n{safe_comment}"
    )


def normalize_ner_output(raw_text: str) -> List[Dict[str, str]]:
    json_text = _extract_first_json_block(raw_text)
    try:
        parsed = json.loads(json_text)
    except Exception:
        return []

    if not isinstance(parsed, list):
        return []

    seen = set()
    cleaned: List[Dict[str, str]] = []
    for item in parsed:
        if not isinstance(item, dict):
            continue
        entity = str(item.get("entity", "")).strip()
        label = str(item.get("label", "")).strip().upper()
        if not entity or label not in ALLOWED_LABELS:
            continue
        key = (entity.lower(), label)
        if key in seen:
            continue
        seen.add(key)
        cleaned.append({"entity": entity, "label": label})
    return cleaned


def flatten_by_label(entities: List[Dict[str, str]]) -> Dict[str, str]:
    out: Dict[str, str] = {f"ner_{label.lower()}": "" for label in ALLOWED_LABELS}
    for label in ALLOWED_LABELS:
        vals = [e["entity"] for e in entities if e.get("label") == label]
        out[f"ner_{label.lower()}"] = " | ".join(vals)
    return out


# %% [markdown]
# ## 5. Sample Preparation
# This section loads `reviews_select.csv`, validates expected text and identifier columns, and prepares rows for inference.
# It keeps identifier fields unchanged so outputs remain traceable to original records.

# %%
def load_reviews(sample_size: int) -> pd.DataFrame:
    df = pd.read_csv(INPUT_CSV, encoding="utf-8")

    if "comments" not in df.columns:
        raise ValueError("Column 'comments' is required in data/reviews_select.csv")

    df = df[df["comments"].notna()].copy()
    df["comments"] = df["comments"].astype(str).str.strip()
    df = df[df["comments"] != ""].copy()

    if sample_size > 0 and len(df) > sample_size:
        df = df.head(sample_size).copy()

    return df.reset_index(drop=True)


# %% [markdown]
# ## 6. Main Extraction Loop
# This section runs Ollama calls in parallel workers and captures one NER payload per review.
# It appends structured entities and flattened label columns while preserving original review columns.

# %%
def run_ner_pipeline(df: pd.DataFrame, model: str, temperature: float, max_workers: int) -> pd.DataFrame:
    records = df.to_dict(orient="records")

    def _task(row: Dict[str, object]) -> Dict[str, object]:
        comment = str(row.get("comments", ""))
        prompt = build_ner_prompt(comment)
        raw = call_ollama_ner(model=model, prompt=prompt, temperature=temperature)
        entities = normalize_ner_output(raw)

        result = dict(row)
        result["ner_entities_json"] = json.dumps(entities, ensure_ascii=False)
        result["ner_entity_count"] = len(entities)
        result.update(flatten_by_label(entities))
        return result

    output_rows: List[Dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_task, row) for row in records]
        for fut in tqdm(as_completed(futures), total=len(futures), desc="P13 NER extraction"):
            output_rows.append(fut.result())

    out_df = pd.DataFrame(output_rows)

    # Preserve original order where possible with existing id column.
    if "id" in df.columns and "id" in out_df.columns:
        out_df = out_df.set_index("id").loc[df["id"].values].reset_index()

    return out_df


# %% [markdown]
# ## 7. Aggregation and Statistics
# This section builds a compact entity-level summary from per-review outputs.
# It reports counts per entity and label, including how many distinct reviews mention each entity.

# %%
def build_summary(per_review_df: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []

    review_id_col = "id"
    if review_id_col not in per_review_df.columns:
        review_id_col = "index"

    for _, row in per_review_df.iterrows():
        rid = row.get(review_id_col)
        payload = row.get("ner_entities_json", "[]")
        try:
            ents = json.loads(payload) if isinstance(payload, str) else []
        except Exception:
            ents = []

        for ent in ents:
            if isinstance(ent, dict):
                rows.append(
                    {
                        "review_id": rid,
                        "entity": str(ent.get("entity", "")).strip(),
                        "label": str(ent.get("label", "")).strip().upper(),
                    }
                )

    if not rows:
        return pd.DataFrame(columns=["entity", "label", "count_mentions", "count_reviews"])

    flat = pd.DataFrame(rows)
    summary = (
        flat.groupby(["entity", "label"], as_index=False)
        .agg(count_mentions=("entity", "size"), count_reviews=("review_id", "nunique"))
        .sort_values(["count_mentions", "count_reviews", "entity"], ascending=[False, False, True])
        .reset_index(drop=True)
    )
    return summary


# %% [markdown]
# ## 8. CSV Exports
# This section writes both the per-review dataset and the summary table in UTF-8 encoding.
# Output files are created in `data/` with stable naming conventions for downstream analysis.

# %%
def export_outputs(per_review_df: pd.DataFrame, summary_df: pd.DataFrame) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    per_review_df.to_csv(OUTPUT_PER_REVIEW, index=False, encoding="utf-8")
    summary_df.to_csv(OUTPUT_SUMMARY, index=False, encoding="utf-8")


# %% [markdown]
# ## 9. Unified Carbon Reporting and Final Summary
# This section appends one execution row to the shared carbon report and refreshes hourly aggregation.
# It then prints runtime, energy, and CO2 values for transparent reproducibility.

# %%
def update_unified_carbon_report(script_name: str, n_obs: int, elapsed_s: float) -> None:
    energy_kwh = (POWER_WATTS * elapsed_s) / (1000.0 * 3600.0)
    eco2_grams = energy_kwh * (FR_GRID_KGCO2_PER_KWH * 1000.0)

    expected_columns = [
        "nom du script execute",
        "nombre d'observations traitees",
        "date d'execution",
        "temps d'execution",
        "total KWatt/heure",
        "total eco2 en grammes",
    ]

    new_row = pd.DataFrame(
        [
            {
                "nom du script execute": script_name,
                "nombre d'observations traitees": int(n_obs),
                "date d'execution": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "temps d'execution": round(float(elapsed_s), 2),
                "total KWatt/heure": round(float(energy_kwh), 6),
                "total eco2 en grammes": round(float(eco2_grams), 2),
            }
        ],
        columns=expected_columns,
    )

    if os.path.exists(CARBON_REPORT):
        existing = pd.read_csv(CARBON_REPORT)
        if list(existing.columns) == expected_columns:
            final_df = pd.concat([existing, new_row], ignore_index=True)
        else:
            final_df = new_row.copy()
    else:
        final_df = new_row.copy()

    final_df.to_csv(CARBON_REPORT, index=False, encoding="utf-8")

    hourly = final_df.copy()
    hourly["date d'execution"] = pd.to_datetime(hourly["date d'execution"], errors="coerce")
    hourly["total eco2 en grammes"] = pd.to_numeric(hourly["total eco2 en grammes"], errors="coerce")
    hourly = hourly.dropna(subset=["date d'execution", "total eco2 en grammes"])

    if not hourly.empty:
        hourly["hour_bucket"] = hourly["date d'execution"].dt.strftime("%Y-%m-%d %H:00")
        hourly_summary = (
            hourly.groupby("hour_bucket", as_index=False)["total eco2 en grammes"]
            .sum()
            .sort_values("hour_bucket")
        )
        hourly_summary.to_csv(CARBON_HOURLY, index=False, encoding="utf-8")


# %% [markdown]
# ## 10. Entry Point
# This section wires CLI arguments to the full execution flow.
# It allows quick testing with `--sample-size` and production runs with full data.

# %%
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="P13 NER extraction with Ollama Gemma")
    parser.add_argument("--sample-size", type=int, default=0, help="Number of rows to process (0 = all)")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Ollama model name")
    parser.add_argument("--temperature", type=float, default=0.0, help="Ollama temperature")
    parser.add_argument("--max-workers", type=int, default=0, help="Parallel workers (0 = auto)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    start_time = time.time()

    workers, mode = configure_runtime(args.max_workers)
    print("=" * 72)
    print("P13 NER - START")
    print("=" * 72)
    print(f"Input file: {INPUT_CSV}")
    print(f"Model: {args.model}")
    print(f"Runtime mode: {mode}")
    print(f"Workers: {workers}")

    df = load_reviews(args.sample_size)
    print(f"Rows prepared: {len(df)}")

    per_review = run_ner_pipeline(
        df=df,
        model=args.model,
        temperature=args.temperature,
        max_workers=workers,
    )
    summary = build_summary(per_review)

    export_outputs(per_review, summary)

    elapsed = time.time() - start_time
    update_unified_carbon_report("p13_ner_ollama.py", len(per_review), elapsed)

    print("=" * 72)
    print("P13 NER - DONE")
    print("=" * 72)
    print(f"Per-review CSV: {OUTPUT_PER_REVIEW}")
    print(f"Summary CSV: {OUTPUT_SUMMARY}")
    print(f"Duration (s): {elapsed:.2f}")


if __name__ == "__main__":
    main()
