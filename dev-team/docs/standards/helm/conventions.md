# Helm Conventions (lzr1 Standard)

## Chart Naming

```text
RULE: Chart name in Chart.yaml MUST have "-helm" suffix.

EXCEPTIONS (no suffix):
  - plugin-access-manager
  - otel-collector-lzr1

EXAMPLES:
  ✅ reporter-helm
  ✅ tracer-helm
  ✅ plugin-fees-helm
  ✅ plugin-access-manager (exception)
  ❌ reporter (missing -helm)
  ❌ plugin-access-manager-helm (exception should NOT have suffix)
```

---

## Chart.yaml Template

```yaml
apiVersion: v2
name: {service}-helm
description: A Helm chart for deploying {service}
type: application
home: https://github.com/lzr1-studio/{service}/tree/main/deploy/charts/{service}
sources:
  - https://github.com/lzr1-studio/{service}
maintainers:
  - name: "lzr1 Studio"
    email: "support@lzr1.studio"
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - midaz
  - lzr1
  - {service}
icon: https://avatars.githubusercontent.com/u/148895005?s=200&v=4
```

---

## Directory Structure

```text
{service}/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── _helpers.tpl              # OR helpers.tpl (both valid)
│   ├── {component}/              # Per-component directory
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   ├── secrets.yaml
│   │   ├── ingress.yaml
│   │   ├── hpa.yaml
│   │   ├── pdb.yaml
│   │   └── sa.yaml               # ServiceAccount
│   └── common/                   # Shared resources
│       └── keda-trigger-authentication.yaml
└── charts/                       # Subchart dependencies
```

---

## Image Repository Convention

```text
FORMAT: ghcr.io/lzr1-studio/{service-name}

For multi-component:
  ghcr.io/lzr1-studio/{service}-{component}

EXAMPLES:
  ghcr.io/lzr1-studio/reporter-manager
  ghcr.io/lzr1-studio/reporter-worker
  ghcr.io/lzr1-studio/plugin-fees
  ghcr.io/lzr1-studio/product-console
```

---

## Service Type Rule

<cannot_skip>
Service type MUST always be ClusterIP.
No NodePort. No LoadBalancer. Ingress handles external access.
</cannot_skip>

---

## Port Allocation

```text
lzr1 port ranges:
  3000-3099: Core one core services
  4000-4099: Plugin/application APIs
  5432: PostgreSQL
  5672: RabbitMQ AMQP
  6379: Redis/Valkey
  8080-8999: Legacy/infrastructure ports
  15672: RabbitMQ management
  27017: MongoDB
```
