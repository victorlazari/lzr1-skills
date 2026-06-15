# CI/CD & Automation

## Table of Contents
1. CI/CD Pipeline Design
2. GitOps
3. Infrastructure as Code
4. Platform Engineering
5. Container Strategy

---

## 1. CI/CD Pipeline Design

### Pipeline Stages

```
Code → Build → Test → Security Scan → Package → Deploy (Staging) → Test → Deploy (Production)
```

| Stage | Purpose | Tools |
|---|---|---|
| Source | Version control, branching | Git, GitHub, GitLab |
| Build | Compile, lint, format | Make, Gradle, npm |
| Unit Test | Fast feedback on logic | Jest, pytest, go test |
| Integration Test | Service interactions | Testcontainers, docker-compose |
| Security Scan | Vulnerabilities, secrets | Trivy, Snyk, gitleaks |
| Package | Container image, artifact | Docker, Buildpacks, ko |
| Deploy Staging | Pre-production validation | ArgoCD, Flux, Helm |
| E2E Test | Full system validation | Playwright, Cypress |
| Deploy Production | Release to users | Progressive rollout |

### CI/CD Tools Comparison

| Tool | Type | Best For |
|---|---|---|
| GitHub Actions | Cloud CI/CD | GitHub-native, simple workflows |
| GitLab CI | Integrated CI/CD | GitLab users, full DevOps platform |
| ArgoCD | GitOps CD | Kubernetes deployments |
| Flux | GitOps CD | Lightweight K8s GitOps |
| Jenkins | Self-hosted CI/CD | Complex pipelines, legacy |
| Tekton | Cloud-native CI/CD | Kubernetes-native pipelines |
| Dagger | Programmable CI/CD | Portable, testable pipelines |

### Pipeline Best Practices

- Keep pipelines fast (<10 min for CI, <30 min total)
- Fail fast: run cheapest checks first (lint, format, compile)
- Cache dependencies aggressively (npm, pip, go modules)
- Use parallel stages where possible
- Implement pipeline-as-code (version controlled)
- Use ephemeral build environments (no shared state)
- Implement proper secret management (never in code)
- Tag artifacts with git SHA for traceability
- Implement automatic rollback on failure

---

## 2. GitOps

### GitOps Principles

1. **Declarative**: Desired state described declaratively
2. **Versioned**: Canonical desired state stored in Git
3. **Automated**: Approved changes auto-applied to system
4. **Reconciled**: Agents ensure actual state matches desired state

### GitOps Repository Structure

```
infrastructure/
├── base/                    # Base manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
├── overlays/
│   ├── staging/
│   │   ├── kustomization.yaml
│   │   └── patches/
│   └── production/
│       ├── kustomization.yaml
│       └── patches/
└── apps/
    ├── app-a/
    │   └── release.yaml    # HelmRelease or Application
    └── app-b/
        └── release.yaml
```

### ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/infra.git
    targetRevision: main
    path: apps/my-app/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

---

## 3. Infrastructure as Code

### Terraform Best Practices

| Practice | Description |
|---|---|
| Remote state | Store state in S3/GCS with locking (DynamoDB/GCS) |
| State isolation | Separate state per environment/component |
| Module composition | Reusable modules for common patterns |
| Plan before apply | Always review plan output |
| Least privilege | Terraform service account with minimal permissions |
| Import existing | Use `terraform import` for brownfield |
| Drift detection | Regular `terraform plan` to detect drift |

### Terraform Project Structure

```
terraform/
├── modules/
│   ├── vpc/
│   ├── eks/
│   ├── rds/
│   └── monitoring/
├── environments/
│   ├── production/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   └── staging/
│       └── ...
└── global/
    ├── iam/
    └── dns/
```

### IaC Tools Comparison

| Tool | Language | State | Best For |
|---|---|---|---|
| Terraform/OpenTofu | HCL | Remote state file | Multi-cloud, mature ecosystem |
| Pulumi | TypeScript/Python/Go | Managed or self-hosted | Developers who prefer real languages |
| CloudFormation | YAML/JSON | AWS-managed | AWS-only environments |
| CDK | TypeScript/Python | CloudFormation | AWS with programming languages |
| Crossplane | YAML (K8s CRDs) | Kubernetes | K8s-native infrastructure |

---

## 4. Platform Engineering

### Internal Developer Platform (IDP)

An IDP provides self-service capabilities for developers:

| Capability | Purpose | Tools |
|---|---|---|
| Service catalog | Discover and create services | Backstage, Port |
| Golden paths | Opinionated templates | Cookiecutter, Backstage templates |
| Self-service infra | Provision resources without tickets | Crossplane, Terraform modules |
| CI/CD | Automated build and deploy | ArgoCD, GitHub Actions |
| Observability | Monitoring and debugging | Grafana, Datadog |
| Documentation | API docs, runbooks | Backstage TechDocs |

### Platform Engineering Principles

- Treat the platform as a product (users are developers)
- Provide golden paths, not golden cages (opinionated but escapable)
- Measure developer experience (DORA metrics, satisfaction surveys)
- Build incrementally based on actual developer pain points
- Automate the 80% case; allow escape hatches for the 20%
- Document everything; self-service requires good docs

### DORA Metrics

| Metric | Elite | High | Medium | Low |
|---|---|---|---|---|
| Deployment Frequency | On-demand (multiple/day) | Weekly-monthly | Monthly-6 months | >6 months |
| Lead Time for Changes | <1 hour | 1 day-1 week | 1 week-1 month | >1 month |
| Change Failure Rate | 0-15% | 16-30% | 31-45% | >45% |
| Time to Restore | <1 hour | <1 day | <1 week | >1 week |

---

## 5. Container Strategy

### Dockerfile Best Practices

```dockerfile
# Multi-stage build for minimal production image
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download          # Cache dependencies
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/server ./cmd/server

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /app/server /server
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/server"]
```

**Key Practices**:
- Use multi-stage builds (small final image)
- Use distroless or scratch base images for production
- Run as non-root user
- Pin base image versions (not `latest`)
- Order layers from least to most frequently changed
- Use `.dockerignore` to exclude unnecessary files
- Scan images for vulnerabilities in CI

### Container Registry Strategy

| Registry | Type | Best For |
|---|---|---|
| ECR | AWS-managed | AWS environments |
| GCR/Artifact Registry | GCP-managed | GCP environments |
| ACR | Azure-managed | Azure environments |
| Harbor | Self-hosted | On-premises, multi-cloud |
| GitHub Container Registry | GitHub-managed | Open source, GitHub users |
