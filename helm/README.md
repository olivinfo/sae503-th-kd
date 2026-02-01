# Chart Helm

## Installation

```bash
helm install cch ./helm/cch -n cch-helm --create-namespace
```

## Personnalisation

```bash
helm install cch ./helm/cch \
  --set image.tag=v1.0.0 \
  --set ingress.host=mon-ip.nip.io
```

## Valeurs par défaut

| Paramètre | Valeur |
|-----------|--------|
| `image.registry` | `ghcr.io/olivinfo` |
| `image.tag` | `latest` |
| `ingress.host` | `172.18.253.218.nip.io` |

## Désinstallation

```bash
helm uninstall cch -n cch-helm
```
