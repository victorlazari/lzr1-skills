# Trivy Filtering, Suppression, and Exception Governance

**Verified against upstream:** 2026-08-07
**Primary source:** [Trivy filtering documentation](https://trivy.dev/docs/latest/configuration/filtering/)

## Contents

1. [Classify the control](#classify-the-control)
2. [Severity and status prioritization](#severity-and-status-prioritization)
3. [Plain ignore files](#plain-ignore-files)
4. [YAML ignore files](#yaml-ignore-files)
5. [Governance ledger](#governance-ledger)
6. [Rego filtering](#rego-filtering)
7. [VEX](#vex)
8. [Skip rules and coverage](#skip-rules-and-coverage)
9. [Exit policy](#exit-policy)
10. [Review checklist](#review-checklist)

## Classify the control

Filtering controls answer different questions and must not be treated as interchangeable.

| Control | Effect | Required evidence |
|---|---|---|
| Scanner selection | Excludes entire finding classes from analysis | Objective and explicit coverage limitation |
| Severity/status filter | Focuses displayed/actionable findings | Full chosen policy and unfiltered evidence when required |
| File/directory skip | Prevents analysis of selected content | Narrow path, rationale, owner, and coverage impact |
| Plain/YAML ignore | Suppresses matching identifiers | Scope, rationale, owner, evidence, approval, and expiry |
| Rego ignore policy | Applies executable decision logic per finding | Reviewed/tested policy, immutable identity, and change control |
| VEX | Applies an authoritative product-status assertion to a vulnerability | Product match, issuer authority, signature/provenance, timestamp, and status rationale |

Never describe a filtered or suppressed result as if the underlying condition did not exist.

## Severity and status prioritization

Use current command help to verify accepted values:

```bash
trivy <target-command> --help
```

Severity filtering commonly uses `--severity`; vulnerability-status filtering uses the current supported status options. Severity is a triage input, not exploitability. Record the severity source and any override. Do not silently remove `UNKNOWN`, unfixed, end-of-life, or vendor-disputed findings from audit evidence.

When two passes are needed, retain both:

1. a discovery pass with the broad agreed scope and non-blocking exit behavior;
2. a policy pass using the organization's explicit gate.

## Plain ignore files

The plain `.trivyignore` format supports vulnerability, misconfiguration, and secret identifiers, but not license findings in the official compatibility table verified above. It supports an inline expiration token:

```text
# Bounded exception; governance record SEC-1234
CVE-2025-12345 exp:2026-12-31

# Misconfiguration identifier
AVD-DS-0002 exp:2026-10-01

# Secret-rule identifier for a synthetic fixture
custom-test-token exp:2026-09-01
```

Comments are not a substitute for an approval record. Validate date behavior with the installed version before relying on it.

## YAML ignore files

The official documentation marks `.trivyignore.yaml` **experimental** and warns that backward compatibility may change. It must currently be selected explicitly with `--ignorefile` according to the verified documentation. Confirm this behavior in the installed release.

Supported top-level lists are:

- `vulnerabilities`;
- `misconfigurations`;
- `secrets`;
- `licenses`.

Supported entry fields are exactly:

| Field | Required | Type | Meaning |
|---|---:|---|---|
| `id` | Yes | string | Vulnerability, misconfiguration, secret-rule, or license identifier |
| `paths` | No | string array | Restricts the entry to matching paths; omission applies it across paths |
| `purls` | No | string array | Restricts a vulnerability entry to matching package URLs |
| `expired_at` | No | date (`yyyy-mm-dd`) | Expiration date; omission makes the entry indefinite |
| `statement` | No | string | Human-readable reason; not used by the filtering decision |

Example:

```yaml
vulnerabilities:
  - id: CVE-2025-12345
    purls:
      - "pkg:npm/example@1.2.3"
    paths:
      - "package-lock.json"
    expired_at: 2026-12-31
    statement: "SEC-1234: bounded exception while upgrade is validated"

misconfigurations:
  - id: AVD-DS-0002
    paths:
      - "examples/Dockerfile"
    expired_at: 2026-10-01
    statement: "SEC-1260: non-production example; removal planned"
```

`reason`, `owner`, `evidence`, `ticket`, `expires`, and `approved_by` are **not documented Trivy schema fields**. Do not put them in the Trivy file. Use `statement` and `expired_at` for supported machine input and keep richer metadata in a companion ledger.

Path-scoped license behavior has ecosystem limitations; consult the current official footnotes before relying on it. `purls` are currently documented only for vulnerability entries.

Always invoke experimental YAML explicitly:

```bash
trivy <target-command> --ignorefile ./.trivyignore.yaml <target>
```

Before adoption, run the installed Trivy build against a synthetic or non-production target to ensure the file parses and the intended finding alone is suppressed.

## Governance ledger

Maintain a separate protected ledger, for example `.trivyignore.governance.json`, with one record per exception:

```json
{
  "schema_version": 1,
  "exceptions": [
    {
      "type": "vulnerabilities",
      "id": "CVE-2025-12345",
      "scope": {
        "paths": ["package-lock.json"],
        "purls": ["pkg:npm/example@1.2.3"]
      },
      "owner": "service-team",
      "evidence": "SEC-1234",
      "rationale": "Bounded technical rationale",
      "created_at": "2026-08-07T00:00:00Z",
      "review_by": "2026-12-31",
      "approved_by": "security-reviewer",
      "state": "approved"
    }
  ]
}
```

The ledger does not affect Trivy. Its purpose is ownership, review, audit, and reconciliation. Protect it from unauthorized edits and secrets. A CI job can reject missing, expired, unapproved, duplicate, or overly broad records before running the scan.

Use [`scripts/setup_ignore.sh`](../scripts/setup_ignore.sh) to generate a **review-only** Trivy YAML proposal and companion governance JSON. The script refuses to overwrite files and does not modify an existing ignore file.

## Rego filtering

The official filtering page marks Rego-based finding suppression experimental at the verification date. The package must be `trivy` and expose an `ignore` rule; verify exact input schemas and helper libraries against the installed release.

Controls:

1. inspect representative JSON output to understand the actual input shape;
2. pin the policy repository commit and hash the loaded policy/data;
3. review Rego as executable policy code;
4. add positive and negative tests, including an assertion that unrelated findings remain visible;
5. fail closed on policy parse/evaluation errors;
6. record pre-policy and post-policy counts;
7. apply finite review/expiry even if the Rego language has no built-in expiry.

Do not copy a release-specific helper import without confirming it exists in the installed version.

## VEX

VEX applies only to vulnerabilities. It communicates product status such as affected, fixed, not affected, or under investigation; exact supported formats and status handling are release-sensitive.

Accept a VEX document only when:

- the product identifier unambiguously matches the target or component;
- the vulnerability identifier matches the finding;
- the issuer is authoritative for that product;
- signature/provenance and integrity are verified where available;
- timestamp, version, and status are current;
- a `not_affected` status includes an allowed justification or impact statement;
- pre-VEX and post-VEX evidence are retained.

A VEX statement does not delete the underlying vulnerability. Reject stale, unsigned when signatures are required, mismatched, or overly broad assertions. Consult the [current VEX documentation](https://trivy.dev/docs/latest/supply-chain/vex/) at execution time.

## Skip rules and coverage

`--skip-dirs`, `--skip-files`, and release-specific include/file-pattern controls change coverage before findings are produced. Record each rule, expansion result, and why the content is out of scope. Avoid generic exclusions such as all tests, all vendor code, all generated files, or broad glob roots without evidence.

Evaluate whether a skip rule hides:

- lockfiles and package manifests;
- IaC rendered or source forms;
- test fixtures that can still contain active secrets;
- vendored runtime dependencies;
- files copied into an image;
- generated deployment manifests.

## Exit policy

Trivy's report `--exit-code` controls the scan process status when findings match the selected policy. It does not prove output validity, database freshness, or upload success.

A robust CI flow separates:

1. execution/coverage failure;
2. policy-finding failure;
3. report parsing/validation failure;
4. evidence upload/publishing failure.

Preserve the Trivy exit code immediately. Do not mask it through a pipe or a later successful upload. Use a non-blocking discovery pass where broad evidence is required, followed by a deliberate policy pass or deterministic evaluation of the saved JSON.

## Review checklist

Before approving an exception, confirm:

- [ ] finding and target identities are exact;
- [ ] path/PURL scope is as narrow as possible;
- [ ] rationale describes technical context rather than convenience;
- [ ] evidence/ticket is accessible to reviewers;
- [ ] owner and approver are named by role/team;
- [ ] expiry/review date is finite and valid;
- [ ] unsupported keys are absent from the Trivy file;
- [ ] installed Trivy parses the ignore file;
- [ ] a positive test suppresses the intended finding;
- [ ] a negative test leaves unrelated findings visible;
- [ ] pre- and post-suppression counts are retained;
- [ ] CI rejects expired or ungoverned entries;
- [ ] the limitation is included in the final report.
