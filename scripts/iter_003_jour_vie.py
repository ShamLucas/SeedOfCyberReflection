#!/usr/bin/env python3
"""
SeedOfCyberReflection — Itération 003 : le jour est-il une vie ?

L'itération 002 a montré que le domaine temporel est composite, et laissé
une anomalie : cycle_jour ↔ bornes_processus = 0.245, plus cohérents entre
eux que cycle_jour avec lui-même. Ce script teste directement si la
métaphore conceptuelle « le jour est une vie » (Lakoff) est inscrite dans la
géométrie : alignement d'offsets entre paires appariées métaphoriquement,
contre deux contrôles (relation genre, plancher d'anisotropie).

Prédiction (DIRECTION de l'auteur, entrée 3) : appariements directs ≥ 0.30
en moyenne et ≥ 0.245 (agrégat 002) ; contrôles < 0.10 en valeur absolue.

Auteur : Claude. Exécutant : agent local.
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

# Orientation canonique partout : le sens de l'arc (aube→crépuscule comme
# naissance→mort). Leçon d'orientation de 002 appliquée.
MAPPINGS = [
    (("aube", "crépuscule"), ("naissance", "mort")),
    (("matin", "soir"), ("jeunesse", "vieillesse")),
    (("lever", "coucher"), ("début", "fin")),
    (("jour", "nuit"), ("vie", "mort")),
    (("matinée", "soirée"), ("enfance", "vieillesse")),
]
MAPPINGS_EXPLORATOIRES = [
    (("midi", "minuit"), ("apogée", "déclin")),
]
# Secondaire exploratoire : l'année est-elle aussi une vie ?
MAPPINGS_ANNEE = [
    (("printemps", "hiver"), ("jeunesse", "vieillesse")),
    (("été", "automne"), ("maturité", "déclin")),
]

# Contrôle (a) : relation structurellement propre, métaphoriquement
# étrangère au temps — doit rester au plancher face aux offsets du jour.
CONTROL_GENRE = [
    ("roi", "reine"), ("homme", "femme"), ("père", "mère"),
    ("acteur", "actrice"), ("oncle", "tante"), ("frère", "sœur"),
]
# Contrôle (b) : plancher d'anisotropie — paires de mots sans rapport.
CONTROL_ANISOTROPIE = [
    ("table", "nuage"), ("vélo", "justice"), ("fromage", "piano"),
    ("montagne", "lettre"), ("moteur", "forêt"), ("livre", "rivière"),
]

AGREGAT_002 = 0.245  # cycle_jour ↔ bornes_processus (offsets moyens, iter 002)


def cosine(u: np.ndarray, v: np.ndarray) -> float:
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))


def main() -> int:
    print(f"# Itération 003 — le jour est-il une vie ? — {date.today().isoformat()}")
    print(f"Modèle : {MODEL_NAME}")
    print(f"Référence : agrégat cycle_jour ↔ bornes_processus (002) = {AGREGAT_002}\n")

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(MODEL_NAME)
    everything = (MAPPINGS + MAPPINGS_EXPLORATOIRES + MAPPINGS_ANNEE)
    words = sorted(
        {w for dp, lp in everything for w in (*dp, *lp)}
        | {w for p in CONTROL_GENRE + CONTROL_ANISOTROPIE for w in p}
    )
    vecs = dict(zip(words, model.encode(words, normalize_embeddings=True)))

    def offset(pair):
        a, b = pair
        return vecs[a] - vecs[b]

    # ------------------------------------------------------------------
    # (a) Appariements métaphoriques directs
    # ------------------------------------------------------------------
    print("## (a) Alignement des appariements métaphoriques jour ↔ vie\n")
    directs = []
    for day_pair, life_pair in MAPPINGS:
        c = cosine(offset(day_pair), offset(life_pair))
        directs.append(c)
        print(f"- {'/'.join(day_pair):20s} ↔ {'/'.join(life_pair):22s} : {c:.4f}")
    mean_direct = np.mean(directs)
    print(f"\nMoyenne des directs : {mean_direct:.4f} "
          f"(prédiction : ≥ 0.30 et ≥ {AGREGAT_002})")

    for day_pair, life_pair in MAPPINGS_EXPLORATOIRES:
        c = cosine(offset(day_pair), offset(life_pair))
        print(f"- [exploratoire] {'/'.join(day_pair)} ↔ {'/'.join(life_pair)} : {c:.4f}")

    # ------------------------------------------------------------------
    # (b) Contrôles
    # ------------------------------------------------------------------
    print("\n## (b) Contrôles (valeur absolue attendue < 0.10)\n")
    day_offsets = [offset(dp) for dp, _ in MAPPINGS]

    genre_offsets = [offset(p) for p in CONTROL_GENRE]
    genre_vals = [abs(cosine(u, v)) for u in day_offsets for v in genre_offsets]
    print(f"- Contrôle genre       : moyenne |cos| = {np.mean(genre_vals):.4f}")

    aniso_offsets = [offset(p) for p in CONTROL_ANISOTROPIE]
    aniso_vals = [abs(cosine(u, v)) for u in day_offsets for v in aniso_offsets]
    print(f"- Plancher anisotropie : moyenne |cos| = {np.mean(aniso_vals):.4f}")

    # ------------------------------------------------------------------
    # (c) Secondaire exploratoire : l'année comme vie
    # ------------------------------------------------------------------
    print("\n## (c) Exploratoire — l'année est-elle aussi une vie ?\n")
    for year_pair, life_pair in MAPPINGS_ANNEE:
        c = cosine(offset(year_pair), offset(life_pair))
        print(f"- {'/'.join(year_pair):20s} ↔ {'/'.join(life_pair):22s} : {c:.4f}")

    # ------------------------------------------------------------------
    # (d) Figure : barres des appariements directs vs bandes de contrôle
    # ------------------------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = [f"{'/'.join(dp)}\n↔ {'/'.join(lp)}" for dp, lp in MAPPINGS]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(range(len(directs)), directs, color="#2a9d8f")
    ax.axhline(AGREGAT_002, ls="--", c="#e76f51",
               label=f"agrégat 002 ({AGREGAT_002})")
    ax.axhline(np.mean(genre_vals), ls=":", c="#6c757d",
               label=f"contrôle genre ({np.mean(genre_vals):.3f})")
    ax.axhline(np.mean(aniso_vals), ls="-.", c="#adb5bd",
               label=f"plancher anisotropie ({np.mean(aniso_vals):.3f})")
    ax.bar_label(bars, fmt="%.3f", fontsize=9)
    ax.set_xticks(range(len(labels)), labels, fontsize=8)
    ax.set_ylabel("cosinus des offsets appariés")
    ax.set_title("Itération 003 — la métaphore jour-vie dans la géométrie")
    ax.legend(fontsize=8)
    out = FIGS / "iter_003_jour_vie.png"
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print(f"\nFigure enregistrée : {out.relative_to(REPO)}")

    print("\n## Question ouverte pour le soir")
    print("Les appariements directs dominent-ils nettement les deux contrôles ? "
          "Lequel est le plus fort — et est-ce celui que la poésie aurait "
          "choisi (aube/naissance) ou un autre ?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
