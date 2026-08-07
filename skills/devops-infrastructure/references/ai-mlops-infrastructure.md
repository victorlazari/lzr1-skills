# AI/MLOps Infrastructure

**Verified against upstream: 2026-08-07**

## Table of Contents
1. AI/ML Workloads on Kubernetes
2. GPU Orchestration
3. Model Versioning & Serving
4. Tools

---

## 1. AI/ML Workloads on Kubernetes

- Use Kubernetes for scalable and reproducible ML pipelines.
- Leverage Kubeflow for end-to-end ML workflows.
- Implement resource quotas and limits for compute-intensive tasks.

## 2. GPU Orchestration

- Configure GPU nodes and device plugins (e.g., NVIDIA device plugin).
- Use GPU sharing techniques (e.g., MIG - Multi-Instance GPU, time-slicing) to optimize utilization.
- Monitor GPU metrics (utilization, memory, temperature) using Prometheus and Grafana.

## 3. Model Versioning & Serving

- Version models using tools like MLflow or DVC.
- Serve models using scalable inference servers (e.g., Triton Inference Server, KServe, Seldon Core).
- Implement A/B testing and canary deployments for model updates.

## 4. Tools

- **Kubeflow**: Machine learning toolkit for Kubernetes.
- **MLflow**: Open source platform for the machine learning lifecycle.
- **Ray**: Framework for scaling AI and Python applications.
- **KServe**: Highly scalable and standards-based model inference platform on Kubernetes.
