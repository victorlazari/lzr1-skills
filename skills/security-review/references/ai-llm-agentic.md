# AI, LLM, and Agentic Security Review Reference

**Author:** Manus AI
**Verified against upstream:** 2026-08-07

## Purpose and Boundaries

This reference provides deterministic, line-by-line code review guidance for identifying vulnerabilities in AI, Large Language Model (LLM), and agentic system integrations. It is designed to support a bounded specialist agent operating within a parallel review protocol or a sequential auditor. This is defensive code-review guidance, not an exploitation manual. It does not claim certification or guarantee the absence of vulnerabilities.

**Boundaries:**
- Do not execute target code, upload proprietary material, expose secrets, or actively test production without explicit authorization.
- Treat all model output as untrusted data.
- Use current live catalogs (CISA KEV, EPSS, NVD, CVE) only as runtime-refreshed context.
- Ensure the content directly supports one bounded specialist agent in the parallel protocol and can also be followed sequentially.

## Table of Contents

1. [Threat Assumptions](#threat-assumptions)
2. [Deterministic Review Procedure](#deterministic-review-procedure)
3. [Code and Configuration Patterns](#code-and-configuration-patterns)
4. [False-Positive Controls and Validation](#false-positive-controls-and-validation)
5. [Finding Evidence Requirements](#finding-evidence-requirements)
6. [Stop and Escalation Rules](#stop-and-escalation-rules)
7. [References](#references)

## Threat Assumptions

The security review assumes the following threat landscape for AI and agentic systems, aligned with industry standards:

- **Prompt Injection (Direct/Indirect):** Attackers can manipulate model behavior by embedding malicious instructions in user input or retrieved data. This can lead to unauthorized actions or information disclosure [1].
- **Data Exfiltration:** Models may inadvertently leak sensitive information from training data, context windows, or external tools. This is particularly risky in multi-tenant environments [2].
- **Retrieval Poisoning:** Attackers can compromise Retrieval-Augmented Generation (RAG) systems by injecting malicious content into the knowledge base, causing the model to generate incorrect or harmful responses [3].
- **Insecure Output Handling:** Applications may execute model output without proper validation, leading to Cross-Site Scripting (XSS), Server-Side Request Forgery (SSRF), or Remote Code Execution (RCE). Model output must always be treated as untrusted [1].
- **Excessive Autonomy:** Agents with broad permissions may perform unintended or destructive actions. The principle of least agency must be enforced [4].
- **Denial of Wallet/Resource Exhaustion:** Attackers can exhaust API quotas or compute resources through complex or repetitive requests, leading to financial loss or service disruption [1].
- **Supply-Chain Risks:** Compromised base models, fine-tuning datasets, or third-party plugins can introduce vulnerabilities. Model and data provenance must be verified [5].
- **Model/Data Provenance:** Lack of visibility into the origin and integrity of models and datasets can lead to the deployment of compromised or biased AI systems [2].
- **Memory/Session Isolation:** Failure to isolate context windows and agent memory between tenants and sessions can result in cross-tenant data leakage [1].
- **Tenant Boundaries:** Inadequate enforcement of tenant boundaries in multi-tenant AI systems can allow unauthorized access to tenant-specific data or models [2].
- **MCP/Plugin/Tool Boundaries:** Weak boundaries between the core model and external plugins or tools can allow attackers to pivot from the model to the underlying infrastructure [3].

## Deterministic Review Procedure

The specialist agent must execute the following deterministic review steps to identify vulnerabilities:

1. **Identify AI/LLM Integration Points:** Locate all API calls to LLM providers, local model inferences, and agentic tool invocations. Document the data flow for each integration point.
2. **Analyze Input Handling:** Verify that user input and retrieved data are sanitized and isolated from system prompts. Check for the use of parameterized prompts or strict input validation.
3. **Evaluate Output Validation:** Ensure that model output is treated as untrusted data and validated against strict schemas before execution or rendering. Look for the use of parsing libraries and schema validation frameworks.
4. **Assess Tool Authorization:** Check that agentic tools operate under the principle of least privilege and require human approval for sensitive actions. Review the configuration of tool permissions and access controls.
5. **Review Memory and Session Isolation:** Confirm that context windows and agent memory are strictly isolated between tenants and sessions. Verify that session identifiers are securely generated and managed.
6. **Examine Supply-Chain Dependencies:** Audit the provenance of models, datasets, and plugins against known vulnerability catalogs. Check for the use of signed models and verified datasets.
7. **Verify Sandboxing:** Ensure that models and agentic tools are executed in sandboxed environments with restricted network and file system access.
8. **Check Evaluation/Monitoring:** Verify that the application implements robust monitoring and evaluation mechanisms to detect anomalous model behavior or prompt injection attempts.

## Code and Configuration Patterns

### Anti-Patterns (Vulnerable)

**Insecure Output Handling (Python):**
```python
# Anti-pattern: Executing model output directly without validation
response = llm.generate(prompt)
# CRITICAL: Remote Code Execution vulnerability
exec(response.text)
```

**Excessive Autonomy (Configuration):**
```json
// Anti-pattern: Broad permissions for an agent without human oversight
{
  "agent_role": "admin",
  "allowed_tools": ["*"],
  "require_human_approval": false
}
```

**Weak Memory Isolation (Python):**
```python
# Anti-pattern: Sharing a single context window across multiple users
global_context = []

def handle_request(user_input):
    global_context.append(user_input)
    response = llm.generate(global_context)
    return response
```

### Secure Patterns (Required)

**Strict Output Validation (Python):**
```python
# Secure pattern: Validating output against a strict schema
from pydantic import BaseModel, ValidationError

class ExpectedOutput(BaseModel):
    action: str
    parameters: dict

response = llm.generate(prompt)
try:
    # Validate the model output before processing
    validated_data = ExpectedOutput.parse_raw(response.text)
    execute_action(validated_data)
except ValidationError:
    # Handle invalid output securely
    handle_error("Invalid model output detected")
```

**Least Agency and Human Approval (Configuration):**
```json
// Secure pattern: Bounded permissions and human-in-the-loop requirement
{
  "agent_role": "readonly_analyst",
  "allowed_tools": ["read_database", "generate_report"],
  "require_human_approval": true
}
```

**Strong Memory Isolation (Python):**
```python
# Secure pattern: Isolating context windows per user session
def handle_request(user_id, user_input):
    session_context = get_session_context(user_id)
    session_context.append(user_input)
    response = llm.generate(session_context)
    save_session_context(user_id, session_context)
    return response
```

## False-Positive Controls and Validation

To minimize false positives and ensure the accuracy of the review, the agent must:

- Differentiate between internal, trusted prompts and external, untrusted input. Findings related to internal prompts should be deprioritized unless they can be influenced by external actors.
- Verify if downstream systems already implement robust output encoding or sandboxing. If downstream protections exist, the severity of the finding may be reduced.
- Check for the presence of dedicated prompt injection mitigation layers (e.g., LLM firewalls or input sanitization proxies).
- Ensure that findings map directly to a specific, actionable line of code or configuration. Vague or generalized findings must be rejected.
- Confirm that the identified vulnerability aligns with the threat assumptions and official frameworks cited in this reference.

## Canonical finding evidence requirements

Every report must conform to `../templates/finding.schema.json`; this reference does not define a reduced alternative. The report root must contain `schema_version`, `review`, `findings`, `conflicts`, and `unknowns`. Every finding must contain `id`, `title`, `status`, `asset`, `locations`, `evidence`, `reasoning`, `preconditions`, `impact`, `taxonomy`, `confidence`, `remediation`, `validation`, `residual_risk`, and `conflicts`. Add optional `cvss_v4` or `live_context` only when supported by the finding; omission is valid. The `conflicts` array contains only top-level conflict IDs. `accepted_risk` is required when `status` is `accepted-risk` and forbidden for every other status; it contains `owner`, `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at`.

For agentic systems, evidence should also identify the untrusted-input origin, model or orchestration boundary, instruction/data transition, available tools and credentials, authorization decision, proposed action, approval or policy gate, and observable side effect. Preserve the distinction between a model producing unsafe text and an application granting that text authority. Tool or model output alone is candidate evidence, not proof of reachability or impact.

Do not reproduce complete prompts, secrets, personal records, model weights, or proprietary corpora. Use a short redacted excerpt or digest. Record missing runtime policy, model version, deployment topology, or tool configuration as an uncertainty, and route contradictory specialist conclusions through the package conflict objects rather than silently selecting one.

A remediation must reduce authority or enforce a deterministic boundary; generic instructions to “sanitize prompts” are insufficient. Prefer typed tool interfaces, server-side policy, least-privilege credentials, explicit approval for consequential actions, output validation at the consuming boundary, isolated memory, provenance-aware retrieval, and safe failure behavior.

## Stop and Escalation Rules

Stop the affected action and escalate to the coordinator or the user-designated Phase 0 contact if any of the following conditions are met. Preserve independent, authorized read-only review dimensions when they remain safe:

- The application grants an agent unrestricted access to a production database, infrastructure, or sensitive APIs.
- The model output is directly piped into a shell, interpreter, or database query without any validation or sanitization.
- The review encounters proprietary or highly sensitive algorithms, models, or datasets that exceed the authorized scope of the audit.
- The agent detects active exploitation attempts or indicators of compromise within the target environment.
- The available evidence cannot support a deterministic conclusion; record the uncovered components and required evidence rather than guessing.

## Authoritative references

Use the complete version and freshness mapping in [`sources.md`](sources.md). The primary anchors for this dimension are the [OWASP GenAI Security Project](https://genai.owasp.org/), the [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/), [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework), [NIST AI 600-1 Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1), [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final), and [MITRE ATLAS](https://atlas.mitre.org/). Treat OWASP as the application-risk and control taxonomy, NIST as the risk-governance and lifecycle framework, and MITRE ATLAS as adversary-technique context; preserve disagreements or scope differences as uncertainty or a top-level conflict instead of silently choosing one source. Refresh living taxonomies and model-specific guidance at execution time when they affect a conclusion, and record the retrieval timestamp.
