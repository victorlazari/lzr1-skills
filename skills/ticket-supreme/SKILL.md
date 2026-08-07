---
name: ticket-supreme
description: Advanced architecture and implementation guide for enterprise-grade ticketing and issue-tracking systems, focusing on high availability, real-time communication, SLA management, security, omnichannel integration, and AI/ML capabilities.
---

# Ticket System Supreme Specialist

## Scope and Triggers

This skill handles the design, architecture, and implementation of enterprise-grade customer support centers and ticket systems. It activates when tasks involve complex operational requirements, high availability, real-time communication protocols, nuanced SLA management, stringent security and compliance measures, omnichannel integration techniques, AI/ML-driven automation, and data migration strategies.

**Non-goals:** This skill does not cover basic helpdesk setup, end-user training, or non-technical customer service policies.

## Preconditions

Before acting, detect the target environment, versions, permissions, inputs, constraints, and user intent. Verify the scale requirements (e.g., expected concurrent agents, ticket volume) and existing infrastructure.

## Source Freshness

Volatile facts (e.g., specific API endpoints, tool versions, or compliance regulations) must be verified against current upstream documentation at runtime. See the `references/` directory for focused technical material.

## Workflow

1. **Discover:** Analyze the target environment, constraints, and user intent.
2. **Plan:** Design architecture, scaling, and real-time communication patterns.
3. **Implement Security:** Apply RBAC, RLS, PII redaction, and AI-specific security measures.
4. **Integrate AI/ML:** Implement modern LLM-based capabilities (e.g., summarization, automated response generation).
5. **Migrate Data:** Execute data migration strategies using cloud-native tools (if applicable).
6. **Validate:** Verify system behavior, SLA management, and security controls.
7. **Stop:** Terminate when all acceptance criteria are met or progress stalls.

## Safety

- **Read-only discovery:** Always perform read-only discovery before making any mutations.
- **Confirmation:** Require explicit user confirmation for destructive, external, privileged, financial, legal, or production-impacting actions (e.g., data migration, schema changes).

## Validation

- Define syntax checks, dry runs, tests, evidence capture, and postcondition verification.
- Validate AI/ML outputs for prompt injection or data leakage.
- Ensure SLA recalculations are deterministic and timezone-aware.

## Failure Handling

- Diagnose errors using logs and system metrics.
- Choose alternative approaches if a specific tool or pattern fails.
- Roll back changes if a mutation fails or causes instability.
- Do not repeat a failed action unchanged.

## Output Contract

The result must include:
- A structured summary of the implemented architecture and features.
- Evidence of successful validation (e.g., test results, dry run outputs).
- Severity/confidence levels for any identified risks or limitations.
- Actionable next steps for the user.

## Resources

- `references/architecture-patterns.md`: Detailed guidance on high availability, scaling, and real-time communication.
- `references/security-compliance.md`: Focused reference on RBAC, RLS, PII redaction, and AI-specific security risks.
- `references/ai-ml-integration.md`: Specific guidance on modern LLM-based capabilities for ticket systems.
- `references/data-migration.md`: Strategies and patterns for data migration, including cloud-native tools.

## Orchestration

Use parallel work only for independent dimensions. Define inputs, schemas, conflict handling, synthesis, and termination conditions.

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple microservices to design | Architecture Designer | Parallel design of stateless microservices |
| Multiple databases to scale | Database Optimizer | Parallel sharding and replication planning |
| Multiple omnichannel integrations | Integration Specialist | Parallel implementation of email, social, and webhook ingestion |
| Multiple AI/ML models to train | AI/ML Engineer | Parallel development of ticket deflection, categorization, and sentiment analysis models |

**Cross-skill routing:**
- `ai-teammates`: Route when specialized professional roles are needed for parallel execution.
- `automation-and-scheduling`: Route when implementing automated ticket categorization, SLA timers, or webhook event handling.
- `security-review`: Route when validating application code against security breaches, logical flaws, or AI-specific risks.
