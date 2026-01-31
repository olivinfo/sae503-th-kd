# Mesures de Sécurité

Ce document récapitule les mesures de sécurité. Chaque exigence du Lot 5 est détaillée avec sa preuve d'application, une explication de sa mise en oeuvre ou une raison de la non application.

---

## 1. Isolation logique des instances
Le cluster est segmenté en espaces de noms/namespaces distincts pour isoler les cycles de vie et les ressources.

**Résultat** : Existence des namespaces `cch-production` et `cch-recette`.

---

## 2. Optimisation des images Docker
Les images sont construites sur une base minimale afin de réduire la surface d'attaque en supprimant les binaires inutiles (shells, gestionnaires de paquets). Cela permet également le limiter la consommation de ressources.

**Résultat** : Dockerfiles utilise `python:3.9-slim`.

---

## 3. Gestion des tags avec discernement
La politique de tagging a été adaptée pour garantir l'immuabilité et la traçabilité des déploiements.

Nous distinguons plusieurs environnements tags (`develop`, `main`), mais aussi des tags immuables (`SHA-commit`, `SemVer`) pour un contrôle précis des versions déployées. Un tag latest est tout de même proposé.

**Résultat** : Workflow GitHub Actions générant des tags en fonction de la branche `develop` ou `main`, un tag au format `vX.Y.Z-` ou `vX.Y.Z-{beta,alpha,...}.N` est ajouté, basés sur les titres de merge générant le build. Le tag latest est attribué au dernier build réalisé sur la branche `main`. Une surcouche de kustomization permet de séléctionner une version précise via le tag `SemVer` ou éventuellement `SHA-commit`

---

## 4. Configuration d'un securityContext
Un contexte de sécurité est appliqué au niveau des conteneurs (pods Kubernetes) pour restreindre leurs privilèges au strict minimum nécessaire.

Les mesures suivantes sont appliquées dans les manifestes de déploiement :
- **Exécution non-root** : Force l'utilisation d'un utilisateur sans privilèges (`runAsNonRoot: true`, UID/GID `10001`).
- **Système de fichiers en lecture seule** : Empêche toute modification du système de fichiers racine par l'application (`readOnlyRootFilesystem: true`).
- **Pas d'escalade de privilèges** : Interdit aux processus d'acquérir plus de droits que ceux conférés initialement (`allowPrivilegeEscalation: false`).
- **Suppression des capabilities** : Toutes les capacités Linux par défaut sont retirées (`drop: ["ALL"]`) pour réduire la surface d'attaque en cas de compromission.

**Résultat** : Présence du bloc `securityContext` dans `quotes.yaml`, `users.yaml` et `search.yaml`.
