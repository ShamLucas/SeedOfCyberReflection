#!/usr/bin/env python3
"""
SeedOfCyberReflection — Itération 001 : baseline de cartographie sémantique.

Mesure la régularité géométrique de quatre domaines sémantiques dans un espace
d'embeddings, pour calibrer l'instrument avant toute exploration.

Auteur : Claude (claude.ai). Exécutant : agent local.
Sortie : impression console (à logger dans results/) + figures dans results/figs/.

Dépendances : sentence-transformers, numpy, scikit-learn, matplotlib
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

# ---------------------------------------------------------------------------
# Domaines : listes de paires orientées (A, B) partageant une même relation.
# Tout est en français — le modèle est multilingue, et le français est la
# langue de cette expérience.
# ---------------------------------------------------------------------------

DOMAINS = {
    "genre": [
        ("roi", "reine"), ("acteur", "actrice"), ("homme", "femme"),
        ("oncle", "tante"), ("prince", "princesse"), ("serveur", "serveuse"),
        ("chanteur", "chanteuse"), ("directeur", "directrice"),
    ],
    "temporalite": [
        ("matin", "soir"), ("aube", "crépuscule"), ("hier", "demain"),
        ("printemps", "automne"), ("été", "hiver"), ("début", "fin"),
        ("naissance", "mort"), ("lever", "coucher"),
    ],
    "emotions": [
        ("joie", "tristesse"), ("confiance", "méfiance"), ("calme", "colère"),
        ("espoir", "désespoir"), ("courage", "peur"), ("amour", "haine"),
        ("sérénité", "angoisse"), ("enthousiasme", "ennui"),
    ],
    "parente": [
        ("père", "mère"), ("frère", "sœur"), ("fils", "fille"),
        ("grand-père", "grand-mère"), ("neveu", "nièce"), ("parrain", "marraine"),
        ("beau-père", "belle-mère"), ("cousin", "cousine"),
    ],
}


def cosine(u: np.ndarray, v: np.ndarray) -> float:
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))


def main() -> int:
    print(f"# Itération 001 — baseline — {date.today().isoformat()}")
    print(f"Modèle : {MODEL_NAME}\n")

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(MODEL_NAME)

    # Embeddings de tous les mots
    all_words = sorted({w for pairs in DOMAINS.values() for p in pairs for w in p})
    vecs = dict(zip(all_words, model.encode(all_words, normalize_embeddings=True)))

    # ------------------------------------------------------------------
    # Mesure (a) : cohérence des offsets analogiques par domaine
    # ------------------------------------------------------------------
    print("## (a) Cohérence des offsets (cosinus moyen entre offsets du domaine)\n")
    offset_scores = {}
    for name, pairs in DOMAINS.items():
        offsets = [vecs[a] - vecs[b] for a, b in pairs]
        sims = [cosine(u, v) for u, v in combinations(offsets, 2)]
        offset_scores[name] = (float(np.mean(sims)), float(np.std(sims)))
        print(f"- {name:12s} : moyenne={offset_scores[name][0]:.4f}  "
              f"écart-type={offset_scores[name][1]:.4f}")

    ranking = sorted(offset_scores, key=lambda k: -offset_scores[k][0])
    print(f"\nClassement observé : {' > '.join(ranking)}")
    print("Prédiction enregistrée : genre > parente > temporalite > emotions")

    # ------------------------------------------------------------------
    # Mesure (b) : compacité intra-domaine vs distance inter-domaines
    # ------------------------------------------------------------------
    print("\n## (b) Compacité (similarité cosinus moyenne)\n")
    domain_words = {n: sorted({w for p in ps for w in p}) for n, ps in DOMAINS.items()}
    centroids = {}
    for name, words in domain_words.items():
        m = np.stack([vecs[w] for w in words])
        intra = np.mean([cosine(u, v) for u, v in combinations(m, 2)])
        centroids[name] = m.mean(axis=0)
        print(f"- {name:12s} : intra={intra:.4f}")

    print("\nSimilarité entre centroïdes de domaines :")
    for a, b in combinations(DOMAINS, 2):
        print(f"- {a} ↔ {b} : {cosine(centroids[a], centroids[b]):.4f}")

    # ------------------------------------------------------------------
    # Mesure (c) : projections 2D pour l'œil du soir
    # ------------------------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    for ax, (name, pairs) in zip(axes.flat, DOMAINS.items()):
        words = domain_words[name]
        m = np.stack([vecs[w] for w in words])
        xy = PCA(n_components=2).fit_transform(m)
        pos = dict(zip(words, xy))
        for a, b in pairs:
            ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]],
                    "-", color="#bbbbbb", lw=0.8, zorder=1)
        ax.scatter(xy[:, 0], xy[:, 1], s=18, zorder=2)
        for w, (x, y) in pos.items():
            ax.annotate(w, (x, y), fontsize=8, xytext=(3, 3),
                        textcoords="offset points")
        ax.set_title(name)
    fig.suptitle("Itération 001 — PCA par domaine (traits = paires)")
    out = FIGS / "iter_001_pca_domains.png"
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print(f"\nFigure enregistrée : {out.relative_to(REPO)}")

    print("\n## Question ouverte pour le soir")
    print("Le classement observé confirme-t-il la prédiction ? "
          "Sinon, quel domaine surprend, et dans quel sens ?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
