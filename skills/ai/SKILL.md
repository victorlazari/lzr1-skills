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

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple AI system domains are involved, spawn all relevant specialists simultaneously — do not serialize them.
>
> **Single-reference note:** This skill uses one comprehensive reference file (`references/complete-reference.md`). Each specialist receives the full reference but is scoped to a specific config schema and concern domain — they analyze independently without sharing findings during their run.

### Domain Detection Table

Scan the task for signals that indicate which AI system domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference (Config/Section Focus) |
|---|---|---|---|
| `model`, `Claude`, `GPT`, `Gemini`, `Llama`, `select model`, `fine-tune`, `base model`, `architecture`, `Transformer`, `capability benchmark` | **Model Selection & Architecture** | Model Architect | `references/complete-reference.md` (model-registry.json, architecture sections, fine-tuning strategies) |
| `safety`, `alignment`, `bias`, `hallucination`, `guardrails`, `red-teaming`, `adversarial`, `jailbreak`, `MITRE ATLAS`, `STRIDE`, `data poisoning` | **AI Safety & Security** | Safety Specialist | `references/complete-reference.md` (security audit sections, MITRE ATLAS, differential privacy, PII sanitization) |
| `deployment`, `serving`, `inference`, `latency`, `throughput`, `auto-scaling`, `GPU`, `dynamic batching`, `blue-green`, `canary`, `OOM`, `drift` | **Deployment & Inference** | Deployment Specialist | `references/complete-reference.md` (inference-config.toml, deployment strategies, observability.yaml) |
| `cost`, `tokens`, `pricing`, `budget`, `efficiency`, `quantization`, `pruning`, `distillation`, `mixed precision`, `resource optimization` | **Cost & Resource Optimization** | Cost Optimizer | `references/complete-reference.md` (training-pipeline.yaml, resource optimization, model compression) |

### Spawning Logic

**Single domain detected** → Fall back to direct reference consultation (no spawning needed).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + `complete-reference.md` with instruction to focus on its designated config schemas and sections
- No specialist waits for another — all start at the same time
- Maximum concurrent domain specialists: 4 (separate from the existing bulk sub-agent cap of 10 for multi-model/multi-deployment operations)

### Cross-Domain Synthesizer

After all specialists complete, run one **AI System Synthesizer** with all outputs that:

1. **Identifies safety-performance contradictions** — e.g., Model Architect recommends a larger model for capability while Cost Optimizer recommends quantization that degrades the safety guardrails the Safety Specialist relies on
2. **Identifies deployment-architecture mismatches** — e.g., Deployment Specialist's dynamic batching config conflicts with the Model Architect's context window requirements
3. **Maps cost choices to safety implications** — any model compression or pruning recommendation is cross-checked against the Safety Specialist's adversarial robustness requirements before acceptance
4. **Sequences dependencies** — ensures model registry updates (Model Architect) precede inference config changes (Deployment Specialist) in the execution plan

> Synthesis focus for this skill: Enforces that no model upgrade, deployment change, or cost optimization is accepted without an explicit sign-off from the Safety Specialist's analysis. Surfaces the full tradeoff triangle — capability vs. safety vs. cost — before any recommendation is finalized.
