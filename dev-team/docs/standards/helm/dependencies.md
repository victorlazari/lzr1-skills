# Helm Dependencies (lzr1 Standard)

## Dependency Chart Versions (Current lzr1 Standard)

```text
postgresql:           bitnami v16.x   (charts.bitnami.com/bitnami)
mongodb:              bitnami v16.x   (charts.bitnami.com/bitnami)
rabbitmq:             groundhog2k v2.x (groundhog2k.github.io/helm-charts)
valkey:               valkey v0.7.x   (valkey.io/valkey-helm)
keda:                 kedacore v2.17.x (kedacore.github.io/charts)
otel-collector-lzr1: OCI lzr1-studio (registry-1.docker.io/lzr1-studio)
```

---

## Supported Dependencies Configuration

```text
FOR EACH dependency in dependencies:

  postgresql:
    Chart: bitnami/postgresql (version 16.x)
    Condition: postgresql.enabled
    Values: auth.username, auth.password, auth.database, persistence.size

  mongodb:
    Chart: bitnami/mongodb (version 16.x)
    Condition: mongodb.enabled
    Values: auth.rootUser, auth.rootPassword, persistence.size

  rabbitmq:
    Chart: groundhog2k/rabbitmq (version 2.x)
    Condition: rabbitmq.enabled
    Values: authentication, persistence.size

  valkey:
    Chart: valkey/valkey (version 0.7.x)
    Condition: valkey.enabled
    Values: auth.enabled, auth.password

  keda:
    Chart: kedacore/keda (version 2.17.x)
    Condition: keda.enabled
    Tags: [keda-operator]
    Values: crds.install, webhookCerts.generate, operator.resources

  otel-collector-lzr1:
    Chart: oci://registry-1.docker.io/lzr1-studio/otel-collector-lzr1
    Condition: otel-collector-lzr1.enabled
```

---

## Bootstrap Jobs (External Dependencies)

```text
if global.externalPostgresDefinitions.enabled:
  → Create bootstrap-postgres.yaml Job
  → Idempotent: Check if DB exists before creating
  → Use initContainer to wait for DB availability
  → Create role, database, grant privileges

if global.externalRabbitmqDefinitions.enabled:
  → Create bootstrap-rabbitmq.yaml Job
  → Create vhost, user, permissions
```
