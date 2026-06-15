---
name: ai
description: Advanced AI Specialist skill for designing, training, deploying, and troubleshooting AI models, neural networks, transformers, and LLMs.
---

# AI Specialist Skill

## When to Use

Use this skill when you need to:
- Design and implement advanced AI architectures including CNNs, RNNs, Transformers, and Large Language Models (LLMs).
- Develop and optimize end-to-end training pipelines, including data preparation, distributed training, and fine-tuning.
- Deploy machine learning models to production environments with dynamic batching, auto-scaling, and robust inference configurations.
- Perform comprehensive security audits on AI systems, addressing adversarial attacks, data poisoning, and model inversion.
- Troubleshoot and diagnose complex AI system issues such as GPU memory constraints, latency bottlenecks, and model drift.
- Manage AI configurations, model registries, and observability metrics.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple models to train/fine-tune | Training Agent | Parallel training of different model architectures or hyperparameters |
| Multiple datasets to preprocess | Data Prep Agent | Parallel data cleaning, tokenization, and augmentation |
| Multiple deployments to manage | Deployment Agent | Parallel deployment and scaling of inference endpoints |
| Comprehensive security audit | Security Auditor | Parallel vulnerability scanning and adversarial testing of models |
| Bulk troubleshooting | Diagnostics Agent | Parallel investigation of latency, memory, or drift issues across services |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Requirement Analysis & Architecture Design:**
   - Identify the AI task (e.g., NLP, Vision, Reinforcement Learning).
   - Select the appropriate architecture (e.g., Transformer, CNN) and pre-trained base model.
   - Define the mathematical foundations and performance metrics required.

2. **Data Preparation & Pipeline Setup:**
   - Collect, clean, normalize, and tokenize data.
   - Configure data pipelines for efficient batching and distributed training.
   - Address edge cases like sparse data and imbalanced classes.

3. **Model Training & Fine-Tuning:**
   - Initialize the model and configure hyperparameters (learning rate, batch size, optimizer).
   - Execute training loops, utilizing hardware acceleration (GPUs/TPUs) and mixed precision.
   - Apply fine-tuning strategies (Full, Partial, Adapters, Prompt Tuning) to adapt to specific tasks.

4. **Security & Compliance Audit:**
   - Conduct threat modeling (STRIDE, MITRE ATLAS).
   - Secure training data, ensure privacy (PII sanitization, differential privacy), and test for adversarial vulnerabilities.
   - Harden infrastructure and enforce strict IAM policies.

5. **Deployment & Inference Configuration:**
   - Package the model and update the model registry (`model-registry.json`).
   - Configure the inference server (`inference-config.toml`) for dynamic batching and auto-scaling.
   - Deploy using strategies like Blue/Green or Canary releases.

6. **Monitoring & Troubleshooting:**
   - Set up observability (`observability.yaml`) for metrics, logging, and drift detection.
   - Diagnose and resolve deployment errors, GPU memory issues (OOM), and latency bottlenecks.

## Core Principles

- **Scalability & Efficiency:** Always design for distributed training and optimized inference to handle massive datasets and high-throughput requests.
- **Security First:** Treat AI models and data pipelines as critical attack surfaces. Implement robust defenses against adversarial attacks and data poisoning.
- **Reproducibility:** Maintain strict version control for models, data, and configurations using standardized schemas.
- **Continuous Monitoring:** AI models degrade over time. Implement continuous monitoring for data and concept drift to trigger retraining.
- **Resource Optimization:** Efficiently manage GPU memory and compute resources through techniques like mixed precision, model pruning, and dynamic batching.

## Key References

- **Configuration Schemas:** `ai-core.yaml`, `model-registry.json`, `inference-config.toml`, `training-pipeline.yaml`, `observability.yaml`.
- **CLI Commands:** `ai init`, `ai model pull/push`, `ai train start/status`, `ai deploy create/update`.
- **Security Frameworks:** MITRE ATLAS, STRIDE for AI, NIST AI RMF.
- **Mathematical Foundations:** Linear Algebra, Calculus, Probability, Information Theory.
- **Advanced Architectures:** Transformers (Self-Attention, Multi-Head Attention), LLMs (GPT, BERT, T5).
