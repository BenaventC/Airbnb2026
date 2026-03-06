import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Visualisation 2D t-SNE des adjectifs AMOD")
    parser.add_argument(
        "--input-tsne",
        type=str,
        default="data/results_amod_tsne_summary.csv",
        help="CSV t-SNE produit par p03_amod_adj_noun_tsne.py",
    )
    parser.add_argument(
        "--output-png",
        type=str,
        default="data/results_amod_tsne_2d.png",
        help="Image PNG de sortie",
    )
    parser.add_argument(
        "--annotate-top",
        type=int,
        default=20,
        help="Nombre d'adjectifs les plus fréquents à annoter sur le graphe",
    )
    args = parser.parse_args()

    input_path = Path(args.input_tsne)
    output_path = Path(args.output_png)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {input_path}")

    df = pd.read_csv(input_path)
    if df.empty:
        raise ValueError("Le fichier t-SNE est vide, rien à tracer")

    required = {"adjective", "tsne_x", "tsne_y", "frequency"}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Colonnes manquantes dans le CSV t-SNE: {missing}")

    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(
        df["tsne_x"],
        df["tsne_y"],
        s=(df["frequency"].clip(lower=1) * 12),
        c=df["frequency"],
        cmap="viridis",
        alpha=0.8,
        edgecolors="black",
        linewidths=0.3,
    )

    top_n = max(0, int(args.annotate_top))
    if top_n > 0:
        to_annotate = df.sort_values("frequency", ascending=False).head(top_n)
        for _, row in to_annotate.iterrows():
            plt.text(row["tsne_x"], row["tsne_y"], str(row["adjective"]), fontsize=8)

    plt.title("Projection t-SNE 2D des adjectifs (relations AMOD)")
    plt.xlabel("t-SNE dimension 1")
    plt.ylabel("t-SNE dimension 2")
    plt.colorbar(scatter, label="Fréquence")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)

    print(f"Graphe exporté: {output_path}")


if __name__ == "__main__":
    main()
