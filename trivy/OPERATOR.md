# Trivy Operator

Opérateur déployé via Helm pour l'analyse continue des vulnérabilités des workloads Kubernetes.

## Installation

```bash
helm install trivy-operator aqua/trivy-operator \
  --namespace trivy-system \
  --create-namespace \
  --set="trivy.ignoreUnfixed=true" \
  --set="targetNamespaces=cch-recette" \
  --set="serviceMonitor.enabled=false"
```

## Paramètres

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| `trivy.ignoreUnfixed` | `true` | Ignore les CVE sans correctif |
| `targetNamespaces` | `cch-recette` | Namespace a surveillé |
| `serviceMonitor.enabled` | `false` | Métriques Prometheus désactivé |

## Consultation des rapports

```bash
# Vulnérabilités des images
kubectl get vulnerabilityreports -n cch-recette

# Audits de configuration
kubectl get configauditreports -n cch-recette

# Logs de l'opérateur
kubectl logs -n trivy-system deployment/trivy-operator
```

## Exemple de Résultat

```
NAME                                          REPOSITORY        TAG             SCANNER
replicaset-quotes-5c9d879785-quotes-service   olivinfo/quotes   V1.1.0-beta.6   Trivy
replicaset-redis-6c547c4494-redis-service     library/redis     7.4-alpine      Trivy
replicaset-search-5669c646c9-search-service   olivinfo/search   V1.1.0-beta.6   Trivy
replicaset-users-86dbbc798f-users-service     olivinfo/users    V1.1.0-beta.6   Trivy
```
