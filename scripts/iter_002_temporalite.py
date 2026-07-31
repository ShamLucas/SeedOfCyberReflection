#!/usr/bin/env python3
"""
SeedOfCyberReflection — Itération 002 : la temporalité est-elle composite ?

La baseline (001) a mesuré une cohérence d'offsets quasi nulle (0.066) pour un
domaine "temporalité" qui mélangeait plusieurs relations. Ce script éclate le
domaine en quatre sous-relations homogènes et mesure la cohérence intra vs
inter sous-relations.

Prédiction (DIRECTION.md, entrée 2) : intra >= 0.20 pour au moins trois
sous-relations ; inter < 0.15.

Auteur : Claude (claude.ai). Exécutant : agent local.
Dépendances : voir requirements.txt à la racine du repo.
"""

import sys
from datetime import date
from itertools import combinations
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
FIGS = REPO / "results" / "figs"
FIGS.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

SUBRELATIONS = {
    "cycle_jour": [
        ("matin", "soir"), ("aube", "crépuscule"), ("lever", "coucher"),
        ("midi", "minuit"), ("jour", "nuit"), ("matinée", "soirée"),
    ],
    "cycle_annee": [
        ("été", "hiver"), ("printemps", "automne"), ("juillet", "janvier"),
        ("avril", "octobre"), ("solstice", "équinoxe"), ("juin", "décembre"),
    ],
    "deixis": [
        ("hier", "demain"), ("passé", "futur"), ("avant", "après"),
        ("veille", "lendemain"), ("autrefois", "désormais"), ("jadis", "bientôt"),
    ],
    "bornes_processus": [
        ("naissance", "mort"), ("début", "fin"), ("départ", "arrivée"),
        ("ouverture", "fermeture"), ("commencement", "conclusion"),
        ("prologue", "épilogue"),
    ],
}

BASELINE_GLOBAL = 0.0661  # cohérence du domaine "temporalite" mélangé (iter 001)


def cosine(u: np.ndarray, v: np.ndarray) -> float:
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))


def main() -> int:
    print(f"# Itération 002 — temporalité composite — {date.today().isoformat()}")
    print(f"Modèle : {MODEL_NAME}")
    print(f"Référence : cohérence du domaine mélangé en 001 = {BASELINE_GLOBAL}\n")

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(MODEL_NAME)
    all_words = sorted({w for ps in SUBRELATIONS.values() for p in ps for w in p})
    vecs = dict(zip(all_words, model.encode(all_words, normalize_embeddings=True)))

    # ------------------------------------------------------------------
    # (a) Cohérence intra-sous-relation
    # ------------------------------------------------------------------
    print("## (a) Cohérence des offsets INTRA sous-relation\n")
    offsets = {}
    for name, pairs in SUBRELATIONS.items():
        offs = [vecs[a] - vecs[b] for a, b in pairs]
        offsets[name] = offs
        sims = [cosine(u, v) for u, v in combinations(offs, 2)]
        verdict = "≥ 0.20 ✓" if np.mean(sims) >= 0.20 else "< 0.20 ✗"
        print(f"- {name:18s} : moyenne={np.mean(sims):.4f}  "
              f"écart-type={np.std(sims):.4f}  [{verdict}]")

    # ------------------------------------------------------------------
    # (b) Cohérence inter-sous-relations (entre offsets moyens)
    # ------------------------------------------------------------------
    print("\n## (b) Cohérence INTER sous-relations (cosinus entre offsets moyens)\n")
    mean_offsets = {n: np.mean(o, axis=0) for n, o in offsets.items()}
    inter_vals = []
    for a, b in combinations(SUBRELATIONS, 2):
        c = cosine(mean_offsets[a], mean_offsets[b])
        inter_vals.append(c)
        print(f"- {a} ↔ {b} : {c:.4f}")
    print(f"\nMoyenne inter : {np.mean(inter_vals):.4f} "
          f"(prédiction : < 0.15)")

    # ------------------------------------------------------------------
    # (c) Figure : une matrice intra/inter lisible d'un coup d'œil
    # ------------------------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names = list(SUBRELATIONS)
    n = len(names)
    mat = np.zeros((n, n))
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if i == j:
                sims = [cosine(u, v) for u, v in combinations(offsets[a], 2)]
                mat[i, j] = np.mean(sims)
            else:
                mat[i, j] = cosine(mean_offsets[a], mean_offsets[b])

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(mat, vmin=-0.2, vmax=0.8, cmap="RdYlGn")
    ax.set_xticks(range(n), names, rotation=30, ha="right")
    ax.set_yticks(range(n), names)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center",
                    fontsize=11)
    ax.set_title("Itération 002 — cohérence intra (diagonale) vs inter\n"
                 f"(référence domaine mélangé 001 : {BASELINE_GLOBAL:.3f})")
    fig.colorbar(im, shrink=0.8)
    out = FIGS / "iter_002_matrice_temporalite.png"
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print(f"\nFigure enregistrée : {out.relative_to(REPO)}")

    print("\n## Question ouverte pour le soir")
    print("La diagonale domine-t-elle nettement le hors-diagonale ? "
          "Quelle sous-relation est la plus faible, et ses paires "
          "sont-elles vraiment homogènes ?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
