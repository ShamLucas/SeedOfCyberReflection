#!/usr/bin/env python3
"""
SeedOfCyberReflection — Itération 004 : la métaphore jour-vie est-elle
spécifique, ou un arc générique ?

L'itération 003 a mesuré l'alignement des offsets appariés (aube/crépuscule
↔ naissance/mort, etc.) : 0.108 en moyenne, sous le seuil prédit, mais sans
distinguer deux lectures : métaphore spécifique mais faible, ou direction
générique diffuse sur tout le domaine temporel. Ce script calcule la mesure
discriminante notée par l'exécutant le 2026-08-09 et non calculée : comparer
les cosinus appariés (jour_i ↔ vie_i) aux cosinus croisés (jour_i ↔ vie_j,
i≠j).

Prédiction (DIRECTION de l'auteur, entrée 4) : écart moyen (appariés −
croisés) < 0.05, les deux autour de 0.08–0.12 — prolongement le plus
parcimonieux d'une direction partagée et diffuse. Si l'écart dépasse 0.08
et que les croisés retombent près du plancher d'anisotropie (0.084, mesuré
en 003), la métaphore garde une part propre.

Auteur : Claude. Exécutant : agent local.
Dépendances : voir requirements.txt à la racine du repo.
"""

import sys
from datetime import date
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
FIGS = REPO / "results" / "figs"
FIGS.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# Mêmes cinq appariements que l'itération 003, même orientation canonique.
MAPPINGS = [
    (("aube", "crépuscule"), ("naissance", "mort")),
    (("matin", "soir"), ("jeunesse", "vieillesse")),
    (("lever", "coucher"), ("début", "fin")),
    (("jour", "nuit"), ("vie", "mort")),
    (("matinée", "soirée"), ("enfance", "vieillesse")),
]

# Repères de 003, pour situer le résultat sans recalcul.
AGREGAT_002 = 0.245
MOYENNE_APPARIES_003 = 0.1081
PLANCHER_ANISOTROPIE_003 = 0.0840

# Index de l'appariement soupçonné de polysémie (lever/coucher ↔ début/fin,
# sorti négatif en 003) — exclu dans la vérification de robustesse.
INDEX_SUSPECT = 2


def cosine(u: np.ndarray, v: np.ndarray) -> float:
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))


def main() -> int:
    print(f"# Itération 004 — métaphore spécifique ou arc générique ? — {date.today().isoformat()}")
    print(f"Modèle : {MODEL_NAME}")
    print(f"Repères 003 : appariés={MOYENNE_APPARIES_003}, "
          f"plancher anisotropie={PLANCHER_ANISOTROPIE_003}, agrégat 002={AGREGAT_002}\n")

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(MODEL_NAME)
    words = sorted({w for dp, lp in MAPPINGS for w in (*dp, *lp)})
    vecs = dict(zip(words, model.encode(words, normalize_embeddings=True)))

    def offset(pair):
        a, b = pair
        return vecs[a] - vecs[b]

    day_offsets = [offset(dp) for dp, _ in MAPPINGS]
    life_offsets = [offset(lp) for _, lp in MAPPINGS]
    labels = [f"{'/'.join(dp)} ↔ {'/'.join(lp)}" for dp, lp in MAPPINGS]

    # ------------------------------------------------------------------
    # (a) Appariés vs croisés, sur les cinq paires
    # ------------------------------------------------------------------
    n = len(MAPPINGS)
    matched = [cosine(day_offsets[i], life_offsets[i]) for i in range(n)]
    crossed = [cosine(day_offsets[i], life_offsets[j])
               for i in range(n) for j in range(n) if i != j]

    print("## (a) Appariés vs croisés (les cinq paires)\n")
    for lbl, c in zip(labels, matched):
        print(f"- {lbl:38s} : {c:.4f}")
    mean_matched = float(np.mean(matched))
    mean_crossed = float(np.mean(crossed))
    gap = mean_matched - mean_crossed
    print(f"\nMoyenne appariés  : {mean_matched:.4f}  (n={n})")
    print(f"Moyenne croisés   : {mean_crossed:.4f}  (n={len(crossed)})")
    print(f"Écart (appariés − croisés) : {gap:.4f}  "
          f"(prédiction : < 0.05 ; alerte spécificité si > 0.08)")

    # ------------------------------------------------------------------
    # (b) Robustesse : même calcul sans la paire suspecte
    # ------------------------------------------------------------------
    print("\n## (b) Robustesse — sans lever/coucher ↔ début/fin\n")
    keep = [i for i in range(n) if i != INDEX_SUSPECT]
    matched_clean = [matched[i] for i in keep]
    crossed_clean = [cosine(day_offsets[i], life_offsets[j])
                      for i in keep for j in keep if i != j]
    mean_matched_clean = float(np.mean(matched_clean))
    mean_crossed_clean = float(np.mean(crossed_clean))
    print(f"Moyenne appariés (n={len(keep)})  : {mean_matched_clean:.4f}")
    print(f"Moyenne croisés (n={len(crossed_clean)})   : {mean_crossed_clean:.4f}")
    print(f"Écart : {mean_matched_clean - mean_crossed_clean:.4f}")

    # ------------------------------------------------------------------
    # (c) Figure : appariés vs croisés, avec repères 003
    # ------------------------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 5))
    positions = [0, 1]
    means = [mean_matched, mean_crossed]
    spread = [matched, crossed]
    ax.boxplot(spread, positions=positions, widths=0.5)
    ax.scatter(positions, means, color="#e76f51", zorder=5, label="moyenne")
    ax.axhline(PLANCHER_ANISOTROPIE_003, ls="-.", c="#adb5bd",
               label=f"plancher anisotropie 003 ({PLANCHER_ANISOTROPIE_003})")
    ax.set_xticks(positions, ["appariés (jour_i ↔ vie_i)", "croisés (jour_i ↔ vie_j)"])
    ax.set_ylabel("cosinus des offsets")
    ax.set_title("Itération 004 — spécificité de la métaphore jour-vie")
    ax.legend(fontsize=8)
    out = FIGS / "iter_004_metaphore_specifique.png"
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print(f"\nFigure enregistrée : {out.relative_to(REPO)}")

    print("\n## Question ouverte pour le soir")
    print("L'écart appariés − croisés est-il sous 0.05 (arc générique, lecture de "
          "003 confirmée) ou au-dessus de 0.08 avec des croisés proches du plancher "
          "d'anisotropie (métaphore spécifique, lecture de 003 à réviser) ? "
          "La version (b) sans lever/coucher change-t-elle la réponse ?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
