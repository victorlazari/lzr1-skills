---
name: quality-assurance
description: Comprehensive quality assurance skill covering test strategy, test automation, performance testing, security testing, AI testing, and QA processes for software products. Use when designing test strategies, writing test plans, building automation frameworks, conducting performance testing, establishing QA processes, or planning security/AI testing.
---

# Quality Assurance

Expert-level QA covering test strategy, automation, performance testing, security testing, AI testing, and quality processes for software products.

## Scope and Triggers

- **In Scope**: Designing test strategies, test plans, automation frameworks, performance testing, security testing strategy, AI testing strategy, QA process design, bug triage, test environment management, and release quality gates.
- **Triggers**: Use when the user asks to design a test strategy, build an automation framework, plan performance/security/AI testing, or establish QA processes.
- **Out of Scope / Escalation**:
  - For deep, line-by-line code security review or vulnerability scanning, route to `security-review`.
  - For prolonged interaction acting as a specific QA persona, route to `ai-teammates`.

## Preconditions

1. Detect the target domains (Strategy, Automation, Performance, Security, AI) from the task context.
2. Identify the product, stack, and quality goals.
3. Verify permissions and constraints before planning any automated execution.

## Source Freshness

Volatile facts, such as specific tool versions or OWASP Top 10 rankings, are marked with a `Verified against upstream` date. Always check current official documentation before execution.

## Workflow

1. **Detect Domains**: Scan the task for signals indicating which domains apply (Strategy, Automation, Performance, Security, AI).
2. **Spawn Specialists**:
   - If a single domain is detected, load the corresponding reference file and proceed.
   - If multiple domains are detected, spawn all relevant specialists simultaneously (max 3 concurrently). Each specialist receives the full task context and its dedicated reference file.
3. **Plan**: Each specialist formulates a domain-specific plan based on its reference file.
4. **Synthesize**: Run the QA Synthesizer to identify contradictions, gaps, and dependencies between specialist plans. Produce a unified, actionable QA recommendation or test plan, explicitly noting trade-offs and safety boundaries.
5. **Execute/Design**: Create test cases, data, and environments based on the unified plan.
6. **Stop Condition**: Stop when the unified plan covers all detected domains, passes safety validation, and produces the expected output contract.

## Safety

- **Read-only**: Discovery and planning are read-only.
- **Confirmation Required**: Require confirmation before executing automated tests against production environments.
- **Validation**: Validate test framework configurations against known safe defaults. Ensure security testing tools do not perform destructive actions without explicit authorization. Verify that AI testing datasets do not contain PII or sensitive data.

## Validation

- Syntax checks: Ensure test scripts pass syntax validation (e.g., `bash -n`, Python compilation).
- Dry runs: Use dry-run modes for automated tests where feasible.
- Postcondition: Verify that the test plan covers all detected domains and explicitly addresses safety boundaries.

## Failure Handling

- If a test fails, diagnose the error using logs and screenshots.
- Do not repeat a failed action unchanged. Adjust the test data, environment, or script logic.
- If a destructive action fails, provide rollback guidance.

## Output Contract

- **Structure**: A unified QA recommendation or test plan.
- **Evidence**: Explicit trade-off annotations, safety boundaries, and references to authoritative sources.
- **Actionable Next Steps**: Clear instructions for executing the test plan or building the automation framework.

## Resources

- **Test strategy**: `references/test-strategy.md`
- **Test automation**: `references/test-automation.md`
- **Performance testing**: `references/performance-testing.md`
- **Security testing**: `references/security-testing.md`
- **AI testing**: `references/ai-testing.md`
- **Recommended reading**: `references/reading-list.md`

## Orchestration: Multi-Specialist Protocol

### Domain Detection Table

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `test plan`, `strategy` | **Test Strategy** | Strategy Specialist | `references/test-strategy.md` |
| `automation`, `framework` | **Test Automation** | Automation Specialist | `references/test-automation.md` |
| `performance`, `load` | **Performance Testing** | Performance Specialist | `references/performance-testing.md` |
| `security`, `vulnerability` | **Security Testing** | Security Specialist | `references/security-testing.md` |
| `ai`, `machine learning` | **AI Testing** | AI Specialist | `references/ai-testing.md` |

### Cross-Domain Synthesizer

After all specialists complete, run one **QA Synthesizer** with all specialist outputs that:
1. **Identifies contradictions** between specialist recommendations for the same component.
2. **Identifies gaps** — requirements addressed by no specialist.
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation.
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions.
