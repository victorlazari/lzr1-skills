---
name: ai
description: Advanced AI Specialist skill for designing, training, deploying, and troubleshooting AI models, neural networks, transformers, and LLMs. Triggers on requests involving AI architecture, model training, AI safety/security audits, or AI deployment/inference configuration.
---

# AI Specialist Skill

## Scope and Triggers

Use this skill when you need to:
- Design and implement advanced AI architectures including CNNs, RNNs, Transformers, and Large Language Models (LLMs).
- Develop and optimize end-to-end training pipelines, including data preparation, distributed training, and fine-tuning.
- Deploy machine learning models to production environments with dynamic batching, auto-scaling, and robust inference configurations.
- Perform comprehensive security audits on AI systems, addressing adversarial attacks, data poisoning, and model inversion.
- Troubleshoot and diagnose complex AI system issues such as GPU memory constraints, latency bottlenecks, and model drift.
- Manage AI configurations, model registries, and observability metrics.

**Cross-Skill Routing:**
- `security-review` — Route when the task is a general application or infrastructure security review not specific to AI models.
- `automation-and-scheduling` — Route when the task involves setting up automated pipelines or recurring data synchronization rather than AI model training.

## Preconditions

Before acting, detect the target environment, AI system domains involved, permissions, and user intent.
Identify if the task involves Architecture, Safety, Deployment, or Cost optimization.

## Source Freshness

AI models and security frameworks evolve rapidly. Do not rely on hardcoded model names or framework versions.
Always verify the current versions of MITRE ATLAS and NIST AI RMF online before conducting security audits.
Consult `references/ai-source-map.md` for authoritative sources and when to use them.

## Workflow

1. **Requirement Analysis & Architecture Design:**
   - Identify the AI task (e.g., NLP, Vision, Reinforcement Learning).
   - Select the appropriate architecture and pre-trained base model.
   - Define the mathematical foundations and performance metrics required.

2. **Data Preparation & Pipeline Setup:**
   - Collect, clean, normalize, and tokenize data.
   - Configure data pipelines for efficient batching and distributed training.

3. **Model Training & Fine-Tuning:**
   - Initialize the model and configure hyperparameters.
   - Execute training loops, utilizing hardware acceleration and mixed precision.
   - Apply fine-tuning strategies to adapt to specific tasks.

4. **Security & Compliance Audit:**
   - Conduct threat modeling using current MITRE ATLAS and NIST AI RMF guidelines.
   - Secure training data, ensure privacy, and test for adversarial vulnerabilities.

5. **Deployment & Inference Configuration:**
   - Package the model and update the model registry (`templates/model-registry.json`).
   - Configure the inference server (`templates/inference-config.toml`) for dynamic batching and auto-scaling.

6. **Monitoring & Troubleshooting:**
   - Set up observability (`templates/observability.yaml`) for metrics, logging, and drift detection.
   - Diagnose and resolve deployment errors, GPU memory issues, and latency bottlenecks.

## Multi-Specialist Protocol

When multiple AI system domains are involved, spawn all relevant specialists simultaneously.

### Domain Detection Table

| Task Signal (examples) | Domain | Specialist Agent | Reference (Config/Section Focus) |
|---|---|---|---|
| `model`, `select model`, `fine-tune`, `architecture`, `Transformer` | **Model Selection & Architecture** | Model Architect | `references/architecture.md` (`model-registry.json`) |
| `safety`, `alignment`, `bias`, `hallucination`, `guardrails`, `MITRE ATLAS` | **AI Safety & Security** | Safety Specialist | `references/security.md` |
| `deployment`, `serving`, `inference`, `latency`, `throughput`, `auto-scaling` | **Deployment & Inference** | Deployment Specialist | `references/deployment.md` (`inference-config.toml`, `observability.yaml`) |
| `cost`, `tokens`, `pricing`, `budget`, `efficiency`, `quantization` | **Cost & Resource Optimization** | Cost Optimizer | `references/architecture.md` (`training-pipeline.yaml`) |

### Spawning Logic

**Single domain detected** → Fall back to direct reference consultation (no spawning needed).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + specific reference file with instruction to focus on its designated config schemas and sections.
- No specialist waits for another — all start at the same time.
- Maximum concurrent domain specialists: 4.

### Cross-Domain Synthesizer

After all specialists complete, run one **AI System Synthesizer** with all outputs that:
1. **Identifies safety-performance contradictions** (e.g., capability vs. safety guardrails).
2. **Identifies deployment-architecture mismatches** (e.g., dynamic batching vs. context window).
3. **Maps cost choices to safety implications** (e.g., compression vs. adversarial robustness).
4. **Sequences dependencies** (e.g., registry updates precede inference config changes).

**Synthesis focus:** Enforces that no model upgrade, deployment change, or cost optimization is accepted without an explicit sign-off from the Safety Specialist's analysis. Surfaces the full tradeoff triangle — capability vs. safety vs. cost — before any recommendation is finalized.

## Safety and Validation

- **Read-only discovery:** Separate read-only discovery from mutations.
- **Confirmation required:** Require explicit confirmation before deploying models to production, modifying training pipelines, or accepting model/deployment changes.
- **Validation:** Validate all generated configuration schemas (YAML/JSON/TOML) using `scripts/validate-ai-config.py` before applying.
- **Safety Sign-off:** The workflow explicitly requires safety sign-off before accepting model or deployment changes.

## Failure Handling

- If validation fails, diagnose the error using the output of `validate-ai-config.py`, adjust the configuration, and re-validate.
- Do not repeat a failed action unchanged.
- If deployment fails, roll back to the previous known good configuration.

## Output Contract

The final output must include:
- The finalized architecture and deployment plan.
- Validated configuration schemas.
- Explicit safety sign-off and risk assessment.
- Evidence of successful validation checks.

## Resources

- `references/ai-source-map.md`: Structured map of authoritative sources (NIST AI RMF, MITRE ATLAS).
- `references/architecture.md`: Reference for Model Selection & Architecture and Cost Optimization.
- `references/security.md`: Reference for AI Safety & Security.
- `references/deployment.md`: Reference for Deployment & Inference.
- `scripts/validate-ai-config.py`: Deterministic script to validate configuration schemas.
- `templates/ai-core.yaml`: Template for global AI service settings.
- `templates/model-registry.json`: Template for the model registry schema.
- `templates/inference-config.toml`: Template for inference server configuration.
- `templates/training-pipeline.yaml`: Template for the training pipeline definition.
- `templates/observability.yaml`: Template for observability metrics and logging.
