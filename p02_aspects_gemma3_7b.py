import argparse
import importlib.util
import json
import re
import time
from collections import Counter
from pathlib import Path
from urllib import error, request

import pandas as pd


POWER_WATTS = 150
FR_GRID_KGCO2_PER_KWH = 0.056
SCRIPT_START = time.perf_counter()

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"
SUPPORTED_LANGS = {"fr", "en", "es", "de", "pt", "it"}
NORMALIZATION_RULES = [
    (r"location|neighbou?rhood|area|proximity|transport|access", "location"),
    (r"clean|hygiene|tidy|spotless", "cleanliness"),
    (r"comfort|cozy|cosy|spacious|space", "comfort"),
    (r"amenit|equipment|kitchen|wifi|internet|facility", "amenities"),
    (r"value|price|cost|money", "value"),
    (r"host|welcome|hospitality|communication|responsive", "host_communication"),
    (r"quiet|noise|calm|peace", "quietness"),
    (r"bed|sleep|mattress", "sleep_quality"),
    (r"check[- ]?in|check[- ]?out|arrival|departure", "checkin_checkout"),
    (r"recommend", "recommendations"),
]


def progress(iterable, total: int, desc: str):
    if importlib.util.find_spec("tqdm") is not None:
        tqdm_mod = __import__("tqdm", fromlist=["tqdm"])
        return tqdm_mod.tqdm(iterable, total=total, desc=desc, leave=False)
    return iterable


def call_ollama(prompt: str, timeout_sec: int = 120) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        OLLAMA_API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=timeout_sec) as resp:
        body = resp.read().decode("utf-8")
    parsed = json.loads(body)
    return parsed.get("response", "").strip()


def _clean_aspect_list(items: list[str]) -> list[str]:
    cleaned = []
    for item in items:
        if not isinstance(item, str):
            continue
        value = re.sub(r"^\s*(?:[-*•]|\d+[\.)])\s*", "", item.strip().lower())
        value = " ".join(value.split())
        if value:
            cleaned.append(value)

    unique = []
    seen = set()
    for value in cleaned:
        if value not in seen:
            seen.add(value)
            unique.append(value)
    return unique[:7]


def _parse_aspects(raw: str) -> list[str]:
    if not raw:
        return []

    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)

    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return _clean_aspect_list(parsed)
        if isinstance(parsed, dict) and isinstance(parsed.get("aspects"), list):
            return _clean_aspect_list(parsed["aspects"])
    except json.JSONDecodeError:
        pass

    if "," in text:
        candidates = [part.strip() for part in text.split(",") if part.strip()]
        cleaned = _clean_aspect_list(candidates)
        if cleaned:
            return cleaned

    lines = [line for line in text.splitlines() if line.strip()]
    return _clean_aspect_list(lines)


def extract_aspects(comment: str) -> list[str]:
    prompt = (
        "You are an aspect extraction specialist with an absa spirit. "
        "From the following Airbnb review, extract between 3 and 7 main aspects/topics. "
        "Return ONLY valid JSON as an array of short strings, no explanation. "
        "Keep aspect labels concise and normalized.\n\n"
        f"Review:\n{comment[:1800]}"
    )

    try:
        raw = call_ollama(prompt)
    except (error.URLError, TimeoutError, json.JSONDecodeError):
        return []

    return _parse_aspects(raw)


def build_sample(df: pd.DataFrame, sample_size: str | int) -> pd.DataFrame:
    df_work = df.copy()
    df_work["lang_code"] = df_work["langue"].astype(str).str.lower().str.strip()

    df_filtered = df_work[df_work["lang_code"].isin(SUPPORTED_LANGS)].copy()
    valid_text_mask = df_filtered["comments"].notna() & (df_filtered["comments"].astype(str).str.strip() != "")
    df_filtered = df_filtered[valid_text_mask].copy()

    if isinstance(sample_size, str) and sample_size.lower() == "total":
        return df_filtered.reset_index(drop=True)

    n = int(sample_size)
    if n <= 0:
        raise ValueError("sample_size must be > 0 or 'total'")
    return df_filtered.head(min(n, len(df_filtered))).reset_index(drop=True)


def normalize_aspect(aspect: str) -> str:
    raw = str(aspect).lower().strip()
    for pattern, label in NORMALIZATION_RULES:
        if re.search(pattern, raw):
            return label
    return raw


def build_normalized_summary(summary_df: pd.DataFrame) -> pd.DataFrame:
    if summary_df.empty:
        return pd.DataFrame(columns=["aspect_norm", "count", "relative_frequency"])

    df = summary_df.copy()
    df["aspect_norm"] = df["aspect"].map(normalize_aspect)
    agg = df.groupby("aspect_norm", as_index=False)["count"].sum()
    agg = agg.sort_values("count", ascending=False)
    total = max(int(agg["count"].sum()), 1)
    agg["relative_frequency"] = agg["count"] / total
    return agg


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract 3-7 main aspects from Airbnb comments using gemma3:4b via Ollama.")
    parser.add_argument("--sample-size", default="50", help="Integer or 'total'. Default: 50")
    parser.add_argument("--input", default="data/reviews_select.csv", help="Input CSV path")
    parser.add_argument("--out-review", default="data/results_aspects_gemma3_7b_per_review.csv", help="Per-review output CSV")
    parser.add_argument("--out-summary", default="data/results_aspects_gemma3_7b_summary.csv", help="Summary output CSV")
    parser.add_argument("--normalize", action="store_true", help="Also export normalized aspect summary")
    parser.add_argument("--out-summary-normalized", default="data/results_aspects_gemma3_7b_summary_normalized.csv", help="Normalized summary output CSV")
    args = parser.parse_args()

    sample_param = args.sample_size
    if str(sample_param).lower() != "total":
        sample_param = int(sample_param)

    print("Loading data...")
    df = pd.read_csv(args.input, index_col=0)
    df_sample = build_sample(df, sample_param)
    print(f"Total rows loaded: {len(df)}")
    print(f"Rows selected for analysis: {len(df_sample)}")

    rows = []
    aspect_counter = Counter()

    iterator = progress(df_sample.iterrows(), total=len(df_sample), desc="Aspect extraction")
    for review_idx, row in iterator:
        text = str(row.get("comments", "")).strip()
        if not text:
            continue

        aspects = extract_aspects(text)
        for aspect in aspects:
            aspect_counter[aspect] += 1

        review_id = row.get("id", review_idx)
        try:
            review_id = str(int(review_id))
        except Exception:
            review_id = str(review_id)

        rows.append(
            {
                "id": review_id,
                "review_index": review_idx,
                "lang": row.get("lang_code", ""),
                "n_aspects": len(aspects),
                "aspects": json.dumps(aspects, ensure_ascii=False),
            }
        )

    per_review_df = pd.DataFrame(rows)

    total_aspects = sum(aspect_counter.values())
    summary_rows = []
    for aspect, count in aspect_counter.most_common():
        rel_freq = (count / total_aspects) if total_aspects else 0.0
        summary_rows.append({"aspect": aspect, "count": count, "relative_frequency": rel_freq})

    summary_df = pd.DataFrame(summary_rows)

    out_review = Path(args.out_review)
    out_summary = Path(args.out_summary)
    out_summary_normalized = Path(args.out_summary_normalized)
    out_review.parent.mkdir(parents=True, exist_ok=True)
    out_summary.parent.mkdir(parents=True, exist_ok=True)
    out_summary_normalized.parent.mkdir(parents=True, exist_ok=True)

    per_review_df.to_csv(out_review, index=False, encoding="utf-8")
    summary_df.to_csv(out_summary, index=False, encoding="utf-8")

    normalized_df = pd.DataFrame()
    if args.normalize:
        normalized_df = build_normalized_summary(summary_df)
        normalized_df.to_csv(out_summary_normalized, index=False, encoding="utf-8")

    elapsed_sec = time.perf_counter() - SCRIPT_START
    energy_kwh = (POWER_WATTS / 1000) * (elapsed_sec / 3600)
    eco2_kg = energy_kwh * FR_GRID_KGCO2_PER_KWH
    eco2_g = eco2_kg * 1000

    print("\nDone.")
    print(f"Per-review output: {out_review}")
    print(f"Summary output: {out_summary}")
    if args.normalize:
        print(f"Normalized summary output: {out_summary_normalized}")
    print(f"Unique aspects: {len(summary_df)}")
    if args.normalize:
        print(f"Unique normalized aspects: {len(normalized_df)}")
    print(f"Runtime: {elapsed_sec:.2f} s")
    print(f"Energy: {energy_kwh * 1000:.2f} Wh")
    print(f"eCO2: {eco2_g:.2f} gCO2e")


if __name__ == "__main__":
    main()
