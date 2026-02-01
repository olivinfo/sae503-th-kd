# Mesures de Sécurité

Ce document récapitule les mesures de sécurité. Chaque exigence du Lot 5 est détaillée avec sa preuve d'application, une explication de sa mise en oeuvre ou une raison de la non application.

---

## 1. Isolation logique des instances
Le cluster est segmenté en espaces de noms/namespaces distincts pour isoler les cycles de vie et les ressources.

**Résultat** : Existence des namespaces `cch-production` et `cch-recette`.

---

## 2. Optimisation des images Docker
Les images sont construites sur une base minimale afin de réduire la surface d'attaque en supprimant les binaires inutiles (shells, gestionnaires de paquets). Cela permet également le limiter la consommation de ressources.

**Résultat** : Dockerfiles utilise `python:3.9-alpine`.

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

---

## 5. Audit de vulnérabilités Trivy
### a) Les manifests Kubernetes
L'outil **Trivy** est utilisé pour s'assurer de l'absence de vulnérabilités connues et de mauvaises configurations dans l'infrastructure as code (IaC) et les images de conteneurs.

**Mise en oeuvre** :
- **Analyse des manifestes** : Commande `trivy config ./kubernetes` utilisée pour valider les configurations de sécurité.
- **Correction des configurations** : Les alertes remontées (ex: utilisation de tags `latest`, exécution root) ont été corrigées pour atteindre un état sain.
- **Gestion des exceptions** : Un fichier `.trivyignore` documente les règles exclues de manière justifiée (ex: namespace par défaut qui est surchargé plus tard par Kustomize).

**Résultat** : Le rapport d'audit affiche désormais **0 mauvaises configurations** détectées.

### b) Les Dockerfiles
L'analyse s'étend à la définition des images Docker via les Dockerfiles pour garantir qu'elles respectent les recommandations de sécurité de Trivy.

**Mise en oeuvre** :
- **Analyse par service** : Exécution de `trivy config ./<service>` pour chaque dossier (`users`, `quotes`, `search`).
- **Correction des configurations** :
    - Ajout de l'instruction `USER` pour éviter l'exécution root par défaut.
    - Ajout de `HEALTHCHECK` pour permettre à l'orchestrateur de vérifier la santé du service.

**Résultat** : Les rapports Trivy pour `users`, `quotes` et `search` affiche désormais **0 mauvaises configurations** détectées.

### c) Surveillance continue via Trivy Operator

L'opérateur Trivy est déployé dans le cluster pour assurer une analyse automatique et continue des vulnérabilités des workloads en cours d'exécution.

**Mise en œuvre** :
- **Installation via Helm** :
```bash
helm install trivy-operator aqua/trivy-operator \
  --namespace trivy-system \
  --create-namespace \
  --set="trivy.ignoreUnfixed=true" \
  --set="targetNamespaces=cch-recette" \
  --set="serviceMonitor.enabled=false"
```

- **Détails des paramètres de configuration** :
  - `trivy.ignoreUnfixed=true` : Exclut les CVE sans correctif disponible pour réduire le bruit des fails.
  - `targetNamespaces=cch-recette` : Limite la surveillance au namespace de recette par exemple.

**Résultat** : L'opérateur génère automatiquement des rapports. Avec ArgoCD, on peut consulter le resultat de ces analyses.

## 6. Configuration des Secrets

Pour configurer les secrets dans Kubernetes, nous procédons comme suit :

### a) Création des secrets pour les applications Quotes, Search et Users
Ce secret contient la clé d'administration utilisée par le service `quotes`, la même démarche a été fait pour les services `search` et `users`. Il doit être créé manuellement dans chaque namespace pour garantir l'isolation.

**Pour le namespace de Recette :**
```bash
kubectl create secret generic quotes-secrets \
  --from-literal=ADMIN_KEY='secret1' \
  -n cch-recette
```
**Pour le namespace de Production :**

```bash
kubectl create secret generic quotes-secrets \
  --from-literal=ADMIN_KEY='secret1' \
  -n cch-production
```

## b) Utilisation du secret dans les ressources

Enfin, il faut référencer ce secret dans la configuration des conteneurs (par exemple dans quotes.yaml) afin que l'application puisse consommer la variable d'environnement :
```yaml
# Extrait du déploiement
spec:
  containers:
  - name: quotes
    env:
    - name: ADMIN_KEY
      valueFrom:
        secretKeyRef:
          name: quotes-secrets
          key: ADMIN_KEY
```

## 7. Sécurité et Audit avec Trivy Operator

L'opérateur Trivy scanne automatiquement les images de nos containers et les configurations Kubernetes pour détecter des vulnérabilités (CVE).

### a) Installation via Helm
Nous installons l'opérateur dans un namespace dédié pour isoler les outils d'audit.

```bash
# 1. Ajouter le dépôt Helm Aqua Security
helm repo add aquasecurity https://aquasecurity.github.io/helm-charts/
helm repo update

# 2. Installer l'opérateur dans le namespace 'trivy-namespace'
# On configure l'opérateur pour surveiller nos namespaces de recette et prod
helm install trivy-operator aquasecurity/trivy-operator \
  --namespace trivy-system \
  --trivy-namespace \
  --set="trivy.operator.targetNamespaces=cch-recette,cch-production"
```

### b) Utilisation et lecture des rapports
Trivy génère des rapports automatiquement. Il n'y a pas de commande de scan à lancer, il suffit de consulter les ressources créées dans vos namespaces.

Pour voir un résumé des failles trouvées dans le namespace de recette :
```
kubectl get vulnerabilityreports -n cch-recette
```