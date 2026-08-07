# Lerian Helm Complete Reference

**Verified against upstream: 2026-08-07**

## Authoritative Sources
- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [golang-migrate GitHub](https://github.com/golang-migrate/migrate)

## Bitnami OCI Artifact Transition
Bitnami Helm charts have transitioned to OCI artifacts. Use the `oci://` scheme when pulling or upgrading charts.
Example:
```bash
helm upgrade --install my-release oci://registry-1.docker.io/bitnamicharts/postgresql --version 12.1.0
```

## golang-migrate v4 Specifics
Ensure `golang-migrate` v4 is used for database migrations. Verify the version before execution:
```bash
migrate -version
```
Example migration command:
```bash
migrate -path ./migrations -database "$DB_URL" up
```

## Security Standards
All deployments must comply with Kubernetes Restricted Pod Security Standards. Specifically, `values.yaml` must include:
```yaml
securityContext:
  allowPrivilegeEscalation: false
  seccompProfile:
    type: RuntimeDefault
```
Use `scripts/validate-security.sh` to enforce these settings.
