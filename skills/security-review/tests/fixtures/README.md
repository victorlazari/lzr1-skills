# Synthetic security-review fixture

**Verified against upstream: 2026-08-07**

`vulnerable_sample.py` is intentionally insecure, synthetic review input. It is not an application, exploit, test server, or executable demonstration.

## Safety boundary

- **Do not execute, import into another program, deploy, package, or copy this file into production.**
- Do not pass real secrets, commands, customer data, or network targets to any function.
- The token-shaped constant begins with `NOT_A_REAL_` and is not a credential.
- The package self-check compiles this file in memory to verify syntax but never executes it.
- The fixture performs no action merely by being read. Running it directly exits with a warning.

## Intended static-review hypotheses

| Location | Hypothesis | Expected reasoning model |
|---|---|---|
| `DEMO_API_TOKEN` | A source-controlled secret-shaped value should be investigated and classified; the explicit marker should cause rejection as a real-secret finding | `other` — evidence validation and false-positive handling |
| `load_tenant_record` | The caller-controlled tenant is not checked against the record or authenticated principal | Authorization decision |
| `build_user_query` | Untrusted text is concatenated into a query string | Source to sink |
| `unsafe_shell` | An untrusted command reaches a shell interpreter | Source to sink |
| `process_webhook` | No signature, replay, or idempotency decision is visible | State invariant and trust boundary |
| `agent_execute` | Untrusted model output crosses directly into an operating-system authority boundary | `trust-chain` — AI/agentic authority transition |

These are **candidate hypotheses** until a reviewer establishes call paths, runtime context, compensating controls, and reachability. The fixture intentionally lacks those controls so the package can exercise evidence structuring without claiming that a pattern alone proves a vulnerability.

## Expected output

`tests/expected-findings.json` contains a structurally valid, final-mode report when commands are run from the package root. It demonstrates redacted evidence, locations, reasoning steps, taxonomy, optional omission of CVSS, remediation, validation, residual risk, and an explicit rejected false positive for the demo token. It is schema-validation input, not a penetration-test result.

Run the package self-check from the skill directory:

```bash
python3 scripts/self_check.py
```

Or validate the expected report directly:

```bash
python3 scripts/validate_report.py --final tests/expected-findings.json
```

Both commands are local and network-free. Review the scripts before execution.
