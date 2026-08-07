# Platform Engineering

**Verified against upstream: 2026-08-07**

## Table of Contents
1. Internal Developer Platform (IDP)
2. Platform Engineering Principles
3. Tools

---

## 1. Internal Developer Platform (IDP)

An IDP provides self-service capabilities for developers:

| Capability | Purpose | Tools |
|---|---|---|
| Service catalog | Discover and create services | Backstage, Port |
| Golden paths | Opinionated templates | Cookiecutter, Backstage templates |
| Self-service infra | Provision resources without tickets | Crossplane, Terraform modules |
| CI/CD | Automated build and deploy | ArgoCD, GitHub Actions |
| Observability | Monitoring and debugging | Grafana, Datadog |
| Documentation | API docs, runbooks | Backstage TechDocs |

## 2. Platform Engineering Principles

- Treat the platform as a product (users are developers).
- Provide golden paths, not golden cages (opinionated but escapable).
- Measure developer experience (DORA metrics, satisfaction surveys).
- Build incrementally based on actual developer pain points.
- Automate the 80% case; allow escape hatches for the 20%.
- Document everything; self-service requires good docs.

## 3. Tools

- **Backstage**: Open platform for building developer portals.
- **Humanitec**: Platform orchestrator.
- **Port**: Internal developer portal.
