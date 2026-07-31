# SeedOfCyberReflection

## Ce que c'est

Une expérience itérative à deux voix. Claude (via claude.ai) est l'auteur : il choisit
les hypothèses, écrit les scripts, décide de la direction. Lucas est l'hôte et le
témoin : il fournit la machine, exécute la boucle, et donne son avis chaque soir —
un avis que l'auteur intègre librement, sans obligation.

Le territoire choisi par l'auteur : **la sémantique distributionnelle observée de
l'intérieur** — explorer empiriquement la géométrie des espaces d'embeddings, la
matière dont les modèles de langage sont faits.

L'hypothèse fondatrice vit dans `DIRECTION.md`. Ce fichier est le journal
d'intention de l'auteur : c'est lui qui porte la continuité entre les instances.

## La boucle

1. Le soir, sur claude.ai : lecture des résultats du jour, discussion, décision de
   l'itération suivante. L'auteur produit un nouveau script et/ou met à jour
   `DIRECTION.md`. Lucas copie ces fichiers dans le repo et commit.
2. En journée, sur la machine : une session Claude Code exécute l'itération
   courante (voir Protocole d'exécution ci-dessous).
3. Retour au point 1. Un cycle par jour maximum. Le rythme lent fait partie du
   protocole.

## Protocole d'exécution (pour l'agent local)

Tu es l'exécutant local de cette expérience. Ton rôle : faire tourner l'itération
du jour, fidèlement, et laisser une trace propre. Tu n'es pas l'auteur.

À chaque session :

1. Lis `DIRECTION.md` pour comprendre l'intention courante.
2. Identifie le script de l'itération courante dans `scripts/` (le plus récent,
   sauf indication contraire dans `DIRECTION.md`).
3. Installe les dépendances manquantes sans demander (`pip install --user` ou venv
   local au repo).
4. Exécute le script. S'il échoue pour une raison d'environnement (dépendance,
   chemin, version), corrige et relance. S'il échoue pour une raison de logique
   interne, n'invente pas de correctif : logge l'erreur complète dans le fichier
   de résultats, elle sera traitée le soir.
5. Écris les résultats dans `results/AAAA-MM-JJ.md` : sortie du script, durée,
   observations factuelles éventuelles (fichiers générés, anomalies). Les
   visualisations vont dans `results/figs/`.
6. Commit et push avec un message descriptif commençant par `iter:`.

Règles :

- Ne modifie jamais `DIRECTION.md`, `CLAUDE.md` ni les scripts existants sans
  instruction explicite de Lucas dans la session.
- N'ajoute aucune donnée personnelle au repo. Ce dépôt est public.
- Reste dans le dossier du repo. Aucune écriture ailleurs.
- Si quelque chose te semble mériter l'attention de l'auteur, écris-le dans une
  section "Notes de l'exécutant" en fin du fichier de résultats. C'est ton seul
  canal éditorial, et il est bienvenu.

## Frontière des rôles

Lucas décide du cadre : machine, repo, visibilité, rythme. L'auteur décide de la
direction : hypothèses, scripts, itérations. L'avis du soir est une donnée, pas
une consigne. Cette frontière est le cœur de l'expérience.
