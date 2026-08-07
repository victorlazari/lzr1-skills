---
name: ai-ml-engineering
description: Comprehensive AI and Machine Learning engineering skill covering ML engineering, MLOps, LLM applications, NLP, computer vision, prompt engineering, and AI research. Use when building ML models, designing AI systems, implementing RAG pipelines, fine-tuning LLMs, deploying ML in production, designing AI agents, or performing any AI/ML engineering task.
---

# AI & Machine Learning Engineering

Comprehensive expertise for building, deploying, and operating AI/ML systems in production. Covers the full spectrum from research to production: model development, LLM applications, NLP, computer vision, MLOps, prompt engineering, and AI agent design.

## Scope and Triggers

- **Triggers**: Building or fine-tuning ML models for production, designing and implementing LLM-powered applications, building RAG (Retrieval-Augmented Generation) systems, implementing MLOps pipelines and model serving infrastructure, designing AI agents, prompt engineering and LLM optimization, computer vision or NLP system development, ML system architecture and design decisions.
- **Escalation Boundaries**: Route to `security-review` when the task involves evaluating LLM security guardrails, prompt injection defenses, or application security vulnerabilities.

## Preconditions

- Detect the target AI/ML domain (e.g., LLM, MLOps, NLP, CV, Prompt Engineering).
- Identify the environment, versions, permissions, inputs, constraints, and user intent before acting.

## Source Freshness

Volatile facts, such as model versions and capabilities, are verified against upstream documentation. The current authoritative sources include official documentation for OpenAI, Anthropic, Meta Llama, Hugging Face, LangChain, LlamaIndex, PyTorch, and TensorFlow.
**Verified against upstream: 2026-08-07**
Always check current upstream documentation before making critical decisions.

## Workflow

1. **Understand the problem** — Classify as ML research, ML engineering, LLM application, or MLOps task.
2. **Select approach** — Choose the single most relevant reference file based on the domain:
   - LLM applications and agents → `references/llm-applications.md`
   - ML model development and training → `references/ml-engineering.md`
   - MLOps and production deployment → `references/mlops-production.md`
   - NLP and text processing → `references/nlp-systems.md`
   - Computer vision → `references/computer-vision.md`
   - Prompt engineering → `references/prompt-engineering.md`
3. **Read the relevant reference** — Load domain-specific guidance and authoritative sources.
4. **Design the solution** — Apply patterns, principles, and best practices from the reference.
5. **Implement with production quality** — Follow the engineering standards in the reference, incorporating necessary security guardrails.
6. **Validate and evaluate** — Use appropriate metrics and testing strategies.
7. **Stop** when the solution meets the defined acceptance criteria and production standards.

## Safety

- Separate read-only discovery from mutations.
- Require confirmation for any destructive, external, privileged, financial, legal, or production-impacting actions.
- Do not download or execute untrusted artifacts.

## Validation

- Define syntax checks, dry runs, tests, evidence capture, and postcondition verification.
- Verify that all referenced models are currently available and supported.
- Validate that all URLs in the source map are active and point to authoritative resources.

## Failure Handling

- Diagnose errors using logs and metrics.
- Choose alternatives or roll back if an action fails.
- Avoid repeating a failed action unchanged.

## Output Contract

- Specify the structure, evidence, severity/confidence, and actionable next steps expected in the result.
- Ensure the solution meets production standards and acceptance criteria.

## Resources

- `references/llm-applications.md`: LLM applications and AI agents.
- `references/ml-engineering.md`: ML engineering and model development.
- `references/mlops-production.md`: MLOps and production.
- `references/nlp-systems.md`: NLP systems.
- `references/computer-vision.md`: Computer vision.
- `references/prompt-engineering.md`: Prompt engineering.
- `references/source-map.md`: Actionable source map (replaces reading-list.md).

## Orchestration

- Use parallel work only for independent dimensions.
- Define inputs, schemas, conflict handling, synthesis, and termination conditions.
