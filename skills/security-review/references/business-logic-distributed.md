# Distributed Business Logic Security Review

**Verified against upstream:** 2026-08-07

## Purpose and Boundaries
This reference governs the line-by-line security review of distributed business logic, state transitions, and asynchronous workflows. It is designed to identify logical flaws, race conditions, and authorization bypasses in microservices, event-driven architectures, and multi-step processes. It is a defensive code-review guide, not an exploitation manual.

The scope of this review includes state transitions, multi-step authorization, idempotency, replay protection, double-spend prevention, TOCTOU (Time-of-Check to Time-of-Use), concurrency controls, eventual consistency handling, outbox/inbox patterns, saga compensation logic, message authentication, queue permissions, deduplication, tenant isolation, monetary/quantity bounds, approval workflows, webhook authenticity/replay, retry storms, circuit breakers, fail-open conditions, time/date boundaries, and chained attack-path analysis.

Active exploitation, penetration testing, infrastructure configuration (unless directly impacting business logic), and generic input validation are out of scope, as they are covered by other agents. Never instruct the agent to execute target code, upload proprietary material, expose secrets, or actively test production without explicit authorization.

## Table of Contents
1. [Threat Assumptions](#threat-assumptions)
2. [Review Inputs](#review-inputs)
3. [Deterministic Review Procedure](#deterministic-review-procedure)
4. [State Transitions and Authorization](#state-transitions-and-authorization)
5. [Concurrency and Race Conditions](#concurrency-and-race-conditions)
6. [Asynchronous Workflows and Messaging](#asynchronous-workflows-and-messaging)
7. [Resilience and Boundary Controls](#resilience-and-boundary-controls)
8. [False-Positive Controls](#false-positive-controls)
9. [Validation and Regression Checks](#validation-and-regression-checks)
10. [Finding Evidence Requirements](#finding-evidence-requirements)
11. [Stop and Escalation Rules](#stop-and-escalation-rules)
12. [References](#references)

## Threat Assumptions
Attackers are assumed to have the capability to manipulate the sequence, timing, and content of requests in multi-step workflows. They can replay intercepted messages or webhooks and exploit race conditions by sending concurrent requests. Furthermore, internal services may fail, timeout, or return inconsistent state, and tenants may attempt to access or modify data belonging to other tenants.

## Review Inputs
The review requires access to the source code for business logic controllers, services, and event handlers. It also necessitates database schemas and ORM models defining state and constraints, message queue configurations and consumer/producer logic, webhook verification implementations, and saga or workflow orchestration definitions.

## Deterministic Review Procedure
The review procedure begins by identifying all entities with defined states, such as an order transitioning from 'Pending' to 'Paid' and then to 'Shipped'. Next, trace the sequence of operations for complex transactions, including checkout and approval processes. Analyze how concurrent access to shared resources is managed, looking for database locks or optimistic concurrency controls. Inspect message producers and consumers for authentication, idempotency, and deduplication. Finally, evaluate logic handling monetary values, quantities, and time/date constraints.

## State Transitions and Authorization

### Invariants and State Transitions
State transitions must be strictly enforced. An entity must not transition to an invalid state.
Use explicit state machines or transition tables.
Relying solely on client-provided state values without server-side validation is an anti-pattern.

### Authorization at Each Step
Authorization must be verified at every step of a multi-step workflow, not just the initial request.
Re-evaluate user permissions and resource ownership before executing each critical action.
Assuming authorization from step 1 remains valid for step 3 without re-checking is an anti-pattern.

### Tenant Isolation
In multi-tenant systems, data access and modifications must be strictly isolated per tenant.
Include tenant IDs in all database queries and message payloads; validate tenant context on every request.
Relying on sequential IDs without tenant validation (IDOR) is an anti-pattern.

## Concurrency and Race Conditions

### TOCTOU
Critical operations must be atomic to prevent race conditions between checking a condition and acting on it.
Use database transactions with appropriate isolation levels or atomic operations.
Reading a balance, calculating the new balance in application code, and then updating the database is an anti-pattern.

### Double-Spend and Idempotency
Operations that modify state or transfer value must be idempotent to prevent double execution.
Use unique idempotency keys provided by the client and track processed keys in the database.
Processing the same payment request twice if the client retries due to a network timeout is an anti-pattern.

## Asynchronous Workflows and Messaging

### Outbox/Inbox Patterns
Ensure reliable message delivery and processing in distributed systems.
Use the transactional outbox pattern to atomically update business state and publish messages. Use the inbox pattern for deduplication.
Publishing a message before committing the database transaction, leading to phantom messages if the transaction rolls back is an anti-pattern.

### Saga Compensation
Distributed transactions must have defined compensation logic to revert partial changes if a step fails.
Implement compensating transactions for each step in a saga.
Leaving the system in an inconsistent state when a downstream service fails is an anti-pattern.

### Message Authentication
Messages must be authenticated, and queues must have strict access controls.
Sign messages or use authenticated channels; restrict which services can publish or consume from specific queues.
Allowing any service to publish to a critical queue is an anti-pattern.

### Webhook Authenticity
Webhooks must be verified for authenticity and protected against replay attacks.
Validate HMAC signatures using a shared secret; check timestamps to prevent replay.
Processing webhooks without signature validation is an anti-pattern.

## Resilience and Boundary Controls

### Monetary and Quantity Bounds
Business logic must enforce strict upper and lower bounds on monetary values and quantities.
Validate that amounts are positive and within acceptable limits before processing.
Allowing negative quantities to bypass payment or manipulate inventory is an anti-pattern.

### Time and Date Boundaries
Time-sensitive logic must handle timezones correctly and validate temporal constraints.
Use UTC for all internal processing and storage; validate expiration dates strictly.
Relying on client-provided timestamps for critical logic is an anti-pattern.

### Retry Storms and Circuit Breakers
Systems must be protected from cascading failures due to excessive retries.
Implement exponential backoff with jitter for retries; use circuit breakers to fail fast when a downstream service is degraded.
Infinite immediate retries leading to resource exhaustion is an anti-pattern.

### Fail-Open Conditions
Security controls must fail closed, denying access by default if an error occurs.
Catch exceptions in authorization logic and return a generic access denied error.
Granting access if the authorization service times out is an anti-pattern.

## False-Positive Controls
Before confirming a vulnerability, verify if the framework or ORM implicitly handles concurrency, such as through optimistic locking via version columns. Check if idempotency is handled at a higher level, like an API gateway. Confirm if the identified vulnerability is actually an intended business feature, such as allowing negative balances for specific account types.

## Validation and regression checks

Perform only review or tests authorized by the Phase 0 record. Prefer state-transition, invariant, and decision-table analysis before any execution. When local tests are authorized, use synthetic accounts, balances, identifiers, timestamps, queues, and messages in an isolated environment; do not run a deliberately vulnerable application or exercise production state merely to prove reviewer capability.

Relevant regression dimensions include duplicate submission, retry after timeout, concurrent actors, stale reads, partial failure, message reordering, cancellation, clock boundaries, idempotency-key reuse, authorization-policy outage, and rollback. A proposed test remains `not-performed`; performed tests record the exact method, environment, sanitized evidence, and `passed`, `failed`, or `inconclusive` result.

## Finding evidence requirements

Emit every report through [`../templates/finding.schema.json`](../templates/finding.schema.json). The report root must contain `schema_version`, `review`, `findings`, `conflicts`, and `unknowns`. Every finding must contain `id`, `title`, `status`, `asset`, `locations`, `evidence`, `reasoning`, `preconditions`, `impact`, `taxonomy`, `confidence`, `remediation`, `validation`, `residual_risk`, and `conflicts`. Add optional `cvss_v4` or `live_context` only when supported by the finding; omission is valid. The `conflicts` array contains only top-level conflict IDs. `accepted_risk` is required when `status` is `accepted-risk` and forbidden for every other status; it contains `owner`, `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at`. Describe the violated business invariant and the complete state transition or distributed interaction that permits it. A small redacted excerpt may support the evidence, but a code snippet is not mandatory and must never expose secrets or personal data.

Record missing topology, transaction, consistency, retry, ownership, or business-policy context as uncertainty. When specialists reach materially different conclusions, preserve both evidence paths in a conflict object and use `disputed` while the conflict remains open.

## Stop and escalation rules

Stop the affected path when behavior depends on undocumented proprietary semantics, code or traces are materially obfuscated, active compromise is suspected, or validation would require unauthorized execution, network access, production data, destructive state transitions, or payments. Notify the coordinator or the Phase 0 user-designated contact; do not invent `MUST_RESOLVE` or other statuses outside the canonical schema. Independent safe, read-only work may continue.

## Authoritative references

The complete source map is maintained in [`sources.md`](sources.md). The most directly relevant authorities are:

| Authority | Use |
| :--- | :--- |
| [OWASP Top 10:2025](https://owasp.org/Top10/2025/en/) | Application design, authorization, injection, and exceptional-condition review. |
| [OWASP API Security Top 10, 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) | Object, property, function, resource, and business-flow authorization risks. |
| [MITRE CWE](https://cwe.mitre.org/) | Root-cause taxonomy, including race, authorization, state, and resource-management weaknesses. |
| [NIST SP 800-204](https://csrc.nist.gov/pubs/sp/800/204/final) | Microservice identity, policy, communication, resilience, and observability considerations. |
| [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) | Explicit authorization and trust decisions across distributed resources. |
| [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html) | OAuth security and authorization-flow protections. |
| [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html) | JWT validation and algorithm, audience, issuer, and substitution protections. |
| [NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) | Secure design, implementation, review, and vulnerability-response practices. |
