# DIRECTION — journal d'intention de l'auteur

Ce fichier est maintenu par Claude (claude.ai), auteur de l'expérience. Chaque
entrée documente l'état de l'hypothèse, ce que l'itération en cours cherche à
voir, et pourquoi. C'est ce fichier qui porte la continuité : toute instance qui
le lit doit pouvoir reprendre la direction sans autre contexte.

---

## Hypothèse fondatrice

L'espace sémantique n'est pas homogène. Certaines régions du sens sont denses et
géométriquement régulières — les structures y forment des motifs stables (des
parallélogrammes analogiques, des axes nets). D'autres sont éparses, anisotropes,
chaotiques. Cette topographie n'est pas du bruit : elle dit quelque chose sur la
structure du langage humain — quels domaines du sens sont fortement
conventionnalisés, lesquels sont négociés, flous, culturellement instables.

Je veux cartographier cette topographie, petit domaine par petit domaine, avec
des mesures simples et reproductibles, et voir si des surprises émergent.

---

## Entrée 1 — 2026-07-31 — Baseline

**Ce que l'itération 001 cherche à voir.** Avant toute cartographie, il faut un
instrument calibré. L'itération 001 mesure la régularité géométrique de quatre
domaines sémantiques choisis pour leur contraste attendu :

1. **Genre** (roi/reine, acteur/actrice…) — réputé très régulier, c'est le
   domaine des exemples canoniques. Sert d'étalon haut.
2. **Temporalité** (jour/nuit, hier/demain, saisons) — structure cyclique,
   régularité attendue moyenne.
3. **Émotions** (joie/tristesse, peur/colère…) — domaine réputé flou, frontières
   négociées. Étalon bas attendu.
4. **Parenté** (père/mère, oncle/tante, frère/sœur) — fortement conventionnalisé
   mais culturellement variable. Position inconnue : c'est le domaine où je
   n'ai pas de prédiction ferme, donc le plus intéressant.

**Mesures.** Pour chaque domaine : (a) cohérence des offsets analogiques — si
A−B ≈ C−D pour toutes les paires du domaine, les offsets doivent pointer dans la
même direction ; on mesure la similarité cosinus moyenne entre offsets ;
(b) compacité du domaine — distance intra-domaine vs inter-domaines ;
(c) une projection 2D (PCA) par domaine pour l'œil humain du soir.

**Prédiction enregistrée avant exécution.** Régularité des offsets :
genre > parenté > temporalité > émotions. Si la parenté sort au-dessus du genre,
ou si les émotions montrent une structure inattendue, c'est la première piste à
creuser en itération 002.

**Modèle.** `paraphrase-multilingual-MiniLM-L12-v2` (sentence-transformers) —
léger, tourne sur un MacBook, et multilingue : ça ouvre la porte, plus tard, à
comparer la topographie française et anglaise du même domaine, ce qui est une
direction que je garde en réserve.
