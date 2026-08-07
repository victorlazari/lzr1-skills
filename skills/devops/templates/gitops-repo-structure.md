# GitOps Repository Structure Template

This template demonstrates the recommended directory-based environment separation for modern GitOps workflows.

```text
gitops-repo/
├── apps/
│   ├── frontend/
│   │   ├── base/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── kustomization.yaml
│   │   ├── overlays/
│   │   │   ├── dev/
│   │   │   │   ├── patch.yaml
│   │   │   │   └── kustomization.yaml
│   │   │   ├── staging/
│   │   │   │   ├── patch.yaml
│   │   │   │   └── kustomization.yaml
│   │   │   └── prod/
│   │   │       ├── patch.yaml
│   │   │       └── kustomization.yaml
│   └── backend/
│       └── ...
├── infrastructure/
│   ├── base/
│   └── overlays/
│       ├── dev/
│       ├── staging/
│       └── prod/
└── clusters/
    ├── dev-cluster/
    │   └── sync.yaml (ArgoCD Application or Flux Kustomization)
    ├── staging-cluster/
    └── prod-cluster/
```

## Key Principles
1. **Directory-Based Separation:** Environments are separated by directories (`overlays/dev`, `overlays/prod`), not branches.
2. **Base and Overlays:** Use Kustomize to define common resources in `base/` and environment-specific patches in `overlays/`.
3. **Cluster Mapping:** The `clusters/` directory maps GitOps controllers to specific environments.
