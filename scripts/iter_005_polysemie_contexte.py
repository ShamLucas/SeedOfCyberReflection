#!/usr/bin/env python3
"""
SeedOfCyberReflection — Itération 005 : la paire lever/coucher est-elle
polysémique, ou le résultat de 004 est-il fragile pour une autre raison ?

L'itération 004 a montré que le verdict "métaphore spécifique vs arc
générique" bascule entièrement selon qu'on inclut ou exclut une seule paire
sur cinq : lever/coucher ↔ début/fin (cosinus -0.0546 en 003, déjà suspectée
de polysémie — "lever" et "coucher" pris seuls ont des sens dominants sans
rapport avec le cycle du jour). Ce script teste directement cette hypothèse
plutôt que de trancher au jugé : on réembedde lever/coucher dans des phrases
qui forcent le sens temporel, et on regarde si l'offset se rapproche de
celui de début/fin.

Contrôle : la même reformulation en phrase, appliquée à une paire qui
fonctionnait déjà bien en mots nus (jour/nuit ↔ vie/mort, 0.2263 en 004).
Si le contrôle bouge autant que la paire suspecte, l'effet observé n'est pas
spécifique à la polysémie — c'est un artefact générique du passage
mot-nu → phrase, et l'hypothèse de 003/004 n'est pas confirmée.

Prédiction (DIRECTION de l'auteur, entrée 5) : le cosinus contextualisé de
lever/coucher ↔ début/fin passe de -0.0546 à une valeur positive, dans la
fourchette des quatre autres paires de 004 (0.10-0.23) — au moins ≥ 0.10.
Le contrôle jour/nuit ↔ vie/mort reste stable : écart absolu < 0.05 par
rapport à 0.2263. Si les deux prédictions tiennent, la lecture "propre"
(4 paires) de 004 devient la plus fiable, et le verdict penche vers une
part spécifique de la métaphore, pas un pur arc générique.

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

# Repères antérieurs, pour situer le résultat sans recalcul.
COSINUS_003_MOTS_NUS = -0.0546  # lever/coucher ↔ début/fin, en mots isolés
COSINUS_004_JOUR_NUIT = 0.2263  # jour/nuit ↔ vie/mort, en mots isolés (paire témoin)

# Paire testée : phrases qui forcent le sens temporel de lever/coucher.
SUSPECT_DAY = ("le lever du soleil", "le coucher du soleil")
SUSPECT_LIFE = ("début", "fin")  # déjà univoques, laissés en mots nus

# Paire témoin : même traitement (mise en phrase), sur une paire qui
# marchait déjà bien en mots nus — pour détecter un effet générique.
CONTROL_DAY = ("le jour se lève", "la nuit tombe")
CONTROL_LIFE = ("la vie commence", "la mort survient")


def cosine(u: np.ndarray, v: np.ndarray) -> float:
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))


def main() -> int:
    print(f"# Itération 005 — polysémie ou artefact générique ? — {date.today().isoformat()}")
    print(f"Modèle : {MODEL_NAME}")
    print(f"Repères : lever/coucher (mots nus, 003) = {COSINUS_003_MOTS_NUS}, "
          f"jour/nuit ↔ vie/mort (mots nus, 004) = {COSINUS_004_JOUR_NUIT}\n")

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(MODEL_NAME)

    def offset_pair(pair):
        a, b = pair
        va, vb = model.encode([a, b], normalize_embeddings=True)
        return va - vb

    # ------------------------------------------------------------------
    # (a) Paire suspecte, en contexte de phrase
    # ------------------------------------------------------------------
    day_off = offset_pair(SUSPECT_DAY)
    life_off = offset_pair(SUSPECT_LIFE)
    cos_suspect_ctx = cosine(day_off, life_off)

    print("## (a) lever/coucher ↔ début/fin, en contexte\n")
    print(f"Phrases jour  : {SUSPECT_DAY}")
    print(f"Paire vie     : {SUSPECT_LIFE} (mots nus, déjà univoques)")
    print(f"Cosinus contextualisé : {cos_suspect_ctx:.4f}")
    print(f"Cosinus mots nus (003) : {COSINUS_003_MOTS_NUS:.4f}")
    print(f"Delta : {cos_suspect_ctx - COSINUS_003_MOTS_NUS:+.4f}  "
          f"(prédiction : franchit le positif, ≥ 0.10)")

    # ------------------------------------------------------------------
    # (b) Paire témoin, même traitement
    # ------------------------------------------------------------------
    ctrl_day_off = offset_pair(CONTROL_DAY)
    ctrl_life_off = offset_pair(CONTROL_LIFE)
    cos_control_ctx = cosine(ctrl_day_off, ctrl_life_off)

    print("\n## (b) Témoin — jour/nuit ↔ vie/mort, même mise en phrase\n")
    print(f"Phrases jour  : {CONTROL_DAY}")
    print(f"Phrases vie   : {CONTROL_LIFE}")
    print(f"Cosinus contextualisé : {cos_control_ctx:.4f}")
    print(f"Cosinus mots nus (004) : {COSINUS_004_JOUR_NUIT:.4f}")
    print(f"Delta : {cos_control_ctx - COSINUS_004_JOUR_NUIT:+.4f}  "
          f"(prédiction : stable, écart absolu < 0.05)")

    # ------------------------------------------------------------------
    # (c) Figure : avant/après contextualisation, suspect vs témoin
    # ------------------------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 5))
    labels = ["lever/coucher ↔\ndébut/fin", "jour/nuit ↔\nvie/mort (témoin)"]
    before = [COSINUS_003_MOTS_NUS, COSINUS_004_JOUR_NUIT]
    after = [cos_suspect_ctx, cos_control_ctx]
    x = np.arange(len(labels))
    width = 0.32
    ax.bar(x - width / 2, before, width, label="mots nus", color="#adb5bd")
    ax.bar(x + width / 2, after, width, label="en contexte", color="#e76f51")
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(x, labels)
    ax.set_ylabel("cosinus des offsets")
    ax.set_title("Itération 005 — effet de la mise en contexte")
    ax.legend(fontsize=8)
    out = FIGS / "iter_005_polysemie_contexte.png"
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print(f"\nFigure enregistrée : {out.relative_to(REPO)}")

    print("\n## Question ouverte pour le soir")
    print("La paire suspecte franchit-elle le positif en contexte, pendant que le "
          "témoin reste stable ? Si oui, l'hypothèse de polysémie est confirmée et "
          "la lecture propre de 004 (écart 0.073, part spécifique de la métaphore) "
          "devient la plus fiable. Si le témoin bouge autant que la paire suspecte, "
          "c'est un artefact générique de la mise en phrase, pas une preuve de "
          "polysémie — la lecture à 5 paires de 004 (arc générique) reste la plus "
          "défendable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
