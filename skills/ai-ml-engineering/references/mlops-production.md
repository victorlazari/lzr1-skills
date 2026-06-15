# MLOps & Production ML

## Table of Contents
1. MLOps Maturity Model
2. ML Pipeline Architecture
3. Model Serving
4. Monitoring and Observability
5. CI/CD for ML
6. Infrastructure

---

## 1. MLOps Maturity Model

### Maturity Levels

| Level | Description | Characteristics |
|---|---|---|
| 0 - Manual | No automation | Jupyter notebooks, manual deployment, no monitoring |
| 1 - ML Pipeline | Automated training | Reproducible pipelines, experiment tracking, basic monitoring |
| 2 - CI/CD for ML | Automated deployment | Automated testing, model validation gates, A/B testing |
| 3 - Full MLOps | Automated retraining | Drift detection triggers retraining, feature stores, full observability |

### Key MLOps Principles

- **Reproducibility**: Any experiment can be recreated from stored artifacts
- **Automation**: Minimize manual steps in the ML lifecycle
- **Monitoring**: Detect data drift, model degradation, and system failures
- **Versioning**: Track data, code, models, and configurations together
- **Testing**: Validate data quality, model quality, and infrastructure
- **Governance**: Audit trails, access control, model cards, bias detection

---

## 2. ML Pipeline Architecture

### Pipeline Components

```
Data Validation → Feature Engineering → Training → Evaluation → Model Registry → Deployment → Monitoring
      ↑                                                                                          |
      └──────────────────────── Retraining Trigger ←─────────────────────────────────────────────┘
```

### Pipeline Orchestration Tools

| Tool | Strengths | Best For |
|---|---|---|
| Kubeflow Pipelines | Kubernetes-native, scalable | K8s environments |
| Apache Airflow | Mature, flexible DAGs | Data engineering teams |
| Prefect | Modern, Pythonic | Python-first teams |
| Dagster | Software-defined assets | Data-aware pipelines |
| Vertex AI Pipelines | Managed, GCP-native | GCP environments |
| SageMaker Pipelines | Managed, AWS-native | AWS environments |
| ZenML | Framework-agnostic | Multi-cloud |

### Data Validation

Validate data at every pipeline stage:
- **Schema validation**: Column types, required fields, allowed values
- **Statistical validation**: Distribution checks, outlier detection, null rates
- **Freshness validation**: Data recency, update frequency
- **Volume validation**: Expected row counts, growth rates
- **Cross-feature validation**: Logical consistency between features

Tools: Great Expectations, Pandera, TensorFlow Data Validation (TFDV), Deequ

---

## 3. Model Serving

### Serving Patterns

| Pattern | Latency | Throughput | Use Case |
|---|---|---|---|
| Real-time (REST/gRPC) | <100ms | Medium | User-facing predictions |
| Batch | Minutes-hours | Very high | Periodic scoring, reports |
| Streaming | <1s | High | Event-driven predictions |
| Edge/On-device | <10ms | Per-device | Mobile, IoT, offline |
| Embedded | <1ms | Very high | In-database, in-app |

### Model Serving Infrastructure

| Tool | Type | Best For |
|---|---|---|
| TorchServe | PyTorch-native | PyTorch models |
| TensorFlow Serving | TF-native | TensorFlow models |
| Triton Inference Server | Multi-framework, GPU | High-performance, multi-model |
| BentoML | Framework-agnostic | Rapid deployment |
| Seldon Core | Kubernetes-native | K8s, complex graphs |
| KServe | Kubernetes-native | Serverless inference |
| vLLM | LLM-optimized | LLM serving |
| TGI (Text Generation Inference) | LLM-optimized | Hugging Face models |

### Model Optimization for Serving

- **Quantization**: Reduce precision (FP32 → INT8/INT4) for 2-4x speedup
- **Pruning**: Remove unimportant weights for smaller models
- **Distillation**: Train smaller model to mimic larger model
- **ONNX export**: Framework-agnostic optimized inference
- **TensorRT**: NVIDIA GPU-optimized inference
- **Batching**: Group requests for GPU efficiency (dynamic batching)
- **Caching**: Cache predictions for repeated inputs

---

## 4. Monitoring and Observability

### What to Monitor

| Category | Metrics | Alert Threshold |
|---|---|---|
| Model Performance | Accuracy, F1, latency | >5% degradation |
| Data Quality | Null rates, schema violations | Any violation |
| Data Drift | PSI, KL divergence, KS test | PSI > 0.2 |
| Concept Drift | Prediction distribution shift | Significant shift |
| System Health | Latency, throughput, errors | P99 > SLA |
| Resource Usage | GPU/CPU utilization, memory | >80% sustained |
| Business Metrics | Conversion, revenue impact | Below baseline |

### Drift Detection Methods

- **Population Stability Index (PSI)**: Compares feature distributions between reference and current
- **Kolmogorov-Smirnov test**: Non-parametric distribution comparison
- **Wasserstein distance**: Earth mover's distance between distributions
- **ADWIN**: Adaptive windowing for streaming data
- **Page-Hinkley test**: Sequential change detection

### Monitoring Tools

| Tool | Focus | Type |
|---|---|---|
| Evidently AI | Data/model monitoring | Open-source |
| WhyLabs | Data observability | Managed |
| Arize | ML observability | Managed |
| NannyML | Performance estimation | Open-source |
| Prometheus + Grafana | System metrics | Open-source |
| Datadog ML Monitoring | Full-stack | Managed |

### Alerting Strategy

- **Immediate alerts**: System failures, security issues, data pipeline breaks
- **Urgent alerts**: Significant drift detected, model performance degradation
- **Informational**: Gradual drift trends, resource utilization patterns
- **Automated responses**: Trigger retraining, fallback to previous model, scale infrastructure

---

## 5. CI/CD for ML

### ML-Specific CI/CD Pipeline

```
Code Change → Unit Tests → Integration Tests → Training → Model Validation → Staging → A/B Test → Production
                                                              ↓
                                                    Quality Gates:
                                                    - Accuracy > threshold
                                                    - Latency < SLA
                                                    - No bias regression
                                                    - Data quality pass
```

### Testing Pyramid for ML

1. **Unit tests**: Feature transformations, data preprocessing functions
2. **Integration tests**: Pipeline end-to-end with sample data
3. **Model tests**: Performance on golden dataset, slice-based evaluation
4. **Infrastructure tests**: Serving latency, throughput, failover
5. **Shadow testing**: Run new model alongside production, compare outputs
6. **A/B testing**: Gradual rollout with statistical significance testing

### Deployment Strategies

| Strategy | Risk | Rollback Speed | Use Case |
|---|---|---|---|
| Blue-green | Low | Instant | Critical models |
| Canary | Low | Fast | Gradual validation |
| Shadow | None | N/A | Pre-deployment testing |
| A/B testing | Low | Fast | Feature comparison |
| Multi-armed bandit | Low | Automatic | Continuous optimization |

### Model Registry

A model registry stores and manages model versions:
- Model artifacts (weights, configs, preprocessing)
- Metadata (metrics, training data version, hyperparameters)
- Lineage (data → features → model → deployment)
- Stage management (staging → production → archived)
- Access control and approval workflows

Tools: MLflow Model Registry, Vertex AI Model Registry, SageMaker Model Registry, Neptune

---

## 6. Infrastructure

### Compute Options

| Option | Best For | Cost Model |
|---|---|---|
| Cloud GPU instances | Training, fine-tuning | Per-hour |
| Spot/Preemptible | Fault-tolerant training | 60-90% discount |
| Managed ML platforms | Full lifecycle | Per-use |
| Kubernetes + GPU | Multi-tenant, flexible | Per-cluster |
| Serverless inference | Variable traffic | Per-request |
| Edge devices | Low-latency, offline | Per-device |

### GPU Selection Guide

| GPU | VRAM | Best For |
|---|---|---|
| NVIDIA A100 (80GB) | 80GB | Large model training |
| NVIDIA H100 | 80GB | Frontier model training |
| NVIDIA L4 | 24GB | Inference, fine-tuning |
| NVIDIA T4 | 16GB | Cost-effective inference |
| NVIDIA A10G | 24GB | Balanced training/inference |

### Infrastructure as Code for ML

- Use Terraform/Pulumi for cloud infrastructure
- Use Helm charts for Kubernetes ML workloads
- Use Docker for reproducible environments
- Pin all dependencies (Python packages, system libraries, CUDA versions)
- Separate training and serving infrastructure for cost optimization
- Implement auto-scaling based on request queue depth
