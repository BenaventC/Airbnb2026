import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.metrics import pairwise_distances


POWER_WATTS = 150
FR_GRID_KGCO2_PER_KWH = 0.056
SCRIPT_START = time.perf_counter()


try:
    from tqdm.auto import tqdm
except Exception:
    def tqdm(iterable=None, total=None, desc=None, leave=True):
        return iterable


def parse_sample_size(value: str):
    if isinstance(value, str) and value.lower() == "total":
        return "total"
    try:
        parsed = int(value)
    except Exception as exc:
        raise argparse.ArgumentTypeError("--sample-size doit être un entier > 0 ou 'total'") from exc

    if parsed <= 0:
        raise argparse.ArgumentTypeError("--sample-size doit être un entier > 0 ou 'total'")
    return parsed


def normalize_token_text(frame: pd.DataFrame) -> pd.Series:
    lemma = frame["lemma"].astype(str) if "lemma" in frame.columns else pd.Series("", index=frame.index)
    form = frame["form"].astype(str) if "form" in frame.columns else pd.Series("", index=frame.index)

    lemma_clean = lemma.where(~lemma.isin(["_", "", "nan", "None"]), "")
    form_clean = form.where(~form.isin(["_", "", "nan", "None"]), "")

    token_text = lemma_clean.where(lemma_clean != "", form_clean)
    return token_text.str.strip().str.lower()


def build_group_columns(frame: pd.DataFrame):
    candidates = ["id", "review_index", "lang", "sent_id"]
    group_cols = [column for column in candidates if column in frame.columns]

    if "sent_id" not in group_cols:
        raise ValueError("La colonne 'sent_id' est requise dans le CSV d'annotations")

    return group_cols


def sample_dataframe(frame: pd.DataFrame, sample_size):
    if sample_size == "total":
        return frame.copy(), "total"

    if "id" in frame.columns:
        selected_ids = frame["id"].drop_duplicates().head(sample_size)
        sampled = frame[frame["id"].isin(selected_ids)].copy()
        return sampled, str(sample_size)

    if "review_index" in frame.columns:
        selected_idx = frame["review_index"].drop_duplicates().head(sample_size)
        sampled = frame[frame["review_index"].isin(selected_idx)].copy()
        return sampled, str(sample_size)

    sampled = frame.head(sample_size).copy()
    return sampled, str(sample_size)


def extract_amod_pairs(frame: pd.DataFrame, group_cols):
    rows = []
    grouped = frame.groupby(group_cols, sort=False)

    iterator = tqdm(grouped, total=grouped.ngroups, desc="Extraction AMOD", leave=False)

    for sent_key, sent_df in iterator:
        if not isinstance(sent_key, tuple):
            sent_key = (sent_key,)

        sent_meta = dict(zip(group_cols, sent_key))

        nouns = sent_df[sent_df["upos"].astype(str).str.upper() == "NOUN"][["token_id", "token_text"]].copy()
        if nouns.empty:
            continue

        noun_map = nouns.drop_duplicates(subset=["token_id"]).set_index("token_id")["token_text"].to_dict()

        amods = sent_df[
            (sent_df["deprel"].astype(str).str.lower() == "amod")
            & (sent_df["upos"].astype(str).str.upper() == "ADJ")
        ]

        if amods.empty:
            continue

        for _, adj in amods.iterrows():
            try:
                head_id = int(adj["head"])
            except Exception:
                continue

            noun_text = noun_map.get(head_id)
            if not noun_text:
                continue

            adjective_text = str(adj["token_text"]).strip().lower()
            if not adjective_text:
                continue

            row = {
                **sent_meta,
                "adjective": adjective_text,
                "noun": noun_text,
                "adj_token_id": adj.get("token_id", np.nan),
                "noun_token_id": head_id,
            }
            rows.append(row)

    return pd.DataFrame(rows)


def compute_tsne(distance_matrix: np.ndarray, random_state: int):
    n_items = distance_matrix.shape[0]

    if n_items == 1:
        return np.array([[0.0, 0.0]])
    if n_items == 2:
        return np.array([[0.0, 0.0], [1.0, 0.0]])

    perplexity = min(30.0, max(2.0, float(n_items - 1) / 3.0))

    model = TSNE(
        n_components=2,
        metric="precomputed",
        init="random",
        learning_rate="auto",
        random_state=random_state,
        perplexity=perplexity,
    )
    return model.fit_transform(distance_matrix)


def main():
    parser = argparse.ArgumentParser(
        description="Extraction AMOD (ADJ->NOUN), tableau croisé, matrice de distance et projection t-SNE 2D"
    )
    parser.add_argument(
        "--input-csv",
        type=str,
        default="data/results_reviews_select_sample_annotations.csv",
        help="CSV d'annotations syntaxiques en entrée",
    )
    parser.add_argument(
        "--sample-size",
        type=parse_sample_size,
        default="total",
        help="Nombre de reviews à traiter (entier > 0) ou 'total'",
    )
    parser.add_argument(
        "--distance-metric",
        type=str,
        default="cosine",
        choices=["cosine", "euclidean", "manhattan"],
        help="Métrique pour la matrice de distance",
    )
    parser.add_argument(
        "--top-adjectives",
        type=int,
        default=0,
        help="Limiter le t-SNE aux N adjectifs les plus fréquents (0 = pas de limite)",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Graine aléatoire pour t-SNE",
    )

    args = parser.parse_args()

    input_csv = Path(args.input_csv)
    if not input_csv.exists():
        raise FileNotFoundError(f"Fichier introuvable: {input_csv}")

    output_pairs = Path("data/results_amod_pairs_per_review.csv")
    output_crosstab = Path("data/results_amod_crosstab_summary.csv")
    output_distance = Path("data/results_amod_distance_summary.csv")
    output_tsne = Path("data/results_amod_tsne_summary.csv")

    output_pairs.parent.mkdir(parents=True, exist_ok=True)

    print(f"Chargement du CSV: {input_csv}")
    df = pd.read_csv(input_csv)

    required_columns = {"sent_id", "token_id", "head", "upos", "deprel"}
    missing = sorted(required_columns.difference(df.columns))
    if missing:
        raise ValueError(f"Colonnes manquantes dans le CSV d'entrée: {missing}")

    df["token_text"] = normalize_token_text(df)
    df = df[df["token_text"].notna() & (df["token_text"].astype(str).str.strip() != "")].copy()

    df_sample, sample_label = sample_dataframe(df, args.sample_size)
    group_cols = build_group_columns(df_sample)

    print(f"Lignes d'annotations disponibles: {len(df)}")
    print(f"Sample_Size={sample_label} -> lignes traitées: {len(df_sample)}")

    pairs_df = extract_amod_pairs(df_sample, group_cols)

    if pairs_df.empty:
        pairs_df.to_csv(output_pairs, index=False, encoding="utf-8")
        pd.DataFrame().to_csv(output_crosstab, index=False, encoding="utf-8")
        pd.DataFrame().to_csv(output_distance, index=False, encoding="utf-8")
        pd.DataFrame().to_csv(output_tsne, index=False, encoding="utf-8")

        elapsed_sec = time.perf_counter() - SCRIPT_START
        energy_kwh = (POWER_WATTS / 1000.0) * (elapsed_sec / 3600.0)
        energy_wh = energy_kwh * 1000.0
        co2_g = energy_kwh * FR_GRID_KGCO2_PER_KWH * 1000.0

        print("Aucune paire AMOD (ADJ->NOUN) trouvée.")
        print(f"Temps total: {elapsed_sec:.2f} s")
        print(f"Énergie estimée: {energy_wh:.2f} Wh")
        print(f"CO2 estimé: {co2_g:.2f} gCO2e")
        return

    pairs_df.to_csv(output_pairs, index=False, encoding="utf-8")

    crosstab = pd.crosstab(pairs_df["adjective"], pairs_df["noun"]).astype(float)

    if args.top_adjectives and args.top_adjectives > 0:
        top_adj = crosstab.sum(axis=1).sort_values(ascending=False).head(args.top_adjectives).index
        crosstab = crosstab.loc[top_adj]

    crosstab.to_csv(output_crosstab, encoding="utf-8")

    distance_matrix = pairwise_distances(crosstab.values, metric=args.distance_metric)
    distance_df = pd.DataFrame(distance_matrix, index=crosstab.index, columns=crosstab.index)
    distance_df.to_csv(output_distance, encoding="utf-8")

    tsne_coords = compute_tsne(distance_matrix, random_state=args.random_state)
    tsne_df = pd.DataFrame(
        {
            "adjective": crosstab.index,
            "tsne_x": tsne_coords[:, 0],
            "tsne_y": tsne_coords[:, 1],
            "frequency": crosstab.sum(axis=1).values.astype(int),
            "unique_nouns": (crosstab > 0).sum(axis=1).values.astype(int),
        }
    )
    tsne_df.to_csv(output_tsne, index=False, encoding="utf-8")

    elapsed_sec = time.perf_counter() - SCRIPT_START
    energy_kwh = (POWER_WATTS / 1000.0) * (elapsed_sec / 3600.0)
    energy_wh = energy_kwh * 1000.0
    co2_g = energy_kwh * FR_GRID_KGCO2_PER_KWH * 1000.0

    print("\nExports terminés:")
    print(f"- Paires AMOD: {output_pairs}")
    print(f"- Tableau croisé ADJ x NOUN: {output_crosstab}")
    print(f"- Matrice de distance ({args.distance_metric}): {output_distance}")
    print(f"- Projection t-SNE 2D: {output_tsne}")

    print("\nRésumé:")
    print(f"- Nombre de paires AMOD: {len(pairs_df)}")
    print(f"- Adjectifs uniques: {crosstab.shape[0]}")
    print(f"- Noms uniques: {crosstab.shape[1]}")

    print("\nBilan temps/carbone:")
    print(f"Temps total: {elapsed_sec:.2f} s")
    print(f"Énergie estimée: {energy_wh:.2f} Wh")
    print(f"CO2 estimé: {co2_g:.2f} gCO2e")


if __name__ == "__main__":
    main()
