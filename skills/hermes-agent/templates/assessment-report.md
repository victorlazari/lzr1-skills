# Hermes Agent Assessment Report

**Assessment ID:** `{{assessment_id}}`

**Prepared by:** `{{assessor}}`

**Assessment date:** `{{yyyy-mm-dd}}`

**Target owner:** `{{owner}}`
**Decision:** `{{go | conditional-go | no-go | advisory-only}}`

> This report describes the tested Hermes Agent revision and deployment scope. It does not certify that untested paths or future versions are secure.

## Executive assessment

{{Summarize the objective, deployment posture, material findings, completed actions, and decision in two or three paragraphs.}}

| Measure | Result |
|---|---|
| Target revision/version | `{{immutable_revision_or_version}}` |
| Installation method | `{{method}}` |
| Profile / Hermes home | `{{redacted_profile_and_path}}` |
| Deployment | `{{personal | shared | production}}` |
| Input trust | `{{controlled | mixed | untrusted}}` |
| Data sensitivity | `{{classification}}` |
| Assessed entrypoints | `{{cli_tui_gateway_api_acp_library}}` |
| Assessment coverage | `{{covered_areas}}` |
| Out-of-scope areas | `{{explicit_exclusions}}` |

## Immutable baseline

| Component | Evidence |
|---|---|
| Executable and source | `{{path_and_source_without_secrets}}` |
| Upstream provenance | `{{repository_release_commit_digest}}` |
| Runtime / environment | `{{python_environment_os_architecture}}` |
| Dependency state | `{{lock_state_or_hash}}` |
| Configuration | `{{paths_hashes_permissions_nonsecret_summary}}` |
| Provider and model | `{{provider_endpoint_host_transport_model}}` |
| Extensions | `{{skills_plugins_mcp_hooks_memory_providers}}` |
| Services and listeners | `{{service_user_units_bind_addresses_ports}}` |
| State and persistence | `{{sessions_memory_workspaces_logs_backups}}` |

## Authorization and trust model

{{Describe who authorized the assessment, what actions were permitted, and which user confirmations were required.}}

| Boundary | Classification and evidence |
|---|---|
| User and inbound content | `{{trusted_sources_and_untrusted_sources}}` |
| Model/provider | `{{provider_data_flow_and_assumptions}}` |
| Host process | `{{identity_authority_and_boundary}}` |
| Terminal/code backend | `{{backend_mounts_env_network_limits}}` |
| Host-side tools | `{{browser_plugins_mcp_gateway_and_other_paths}}` |
| External systems | `{{accounts_destinations_scopes_and_effects}}` |
| Multi-user isolation | `{{session_workspace_memory_credential_negative_tests}}` |

## Data and credential flow

| Data or credential class | Source | Destination | Storage / retention | Control |
|---|---|---|---|---|
| `{{class}}` | `{{source}}` | `{{destination}}` | `{{retention}}` | `{{minimization_authorization}}` |

{{State what was redacted and whether any secret values were intentionally inspected.}}

## Findings

| ID | Severity | Status | Finding | Evidence | Required action | Owner / due |
|---|---|---|---|---|---|---|
| `{{HERMES-001}}` | `{{critical | high | medium | low | info}}` | `{{open | fixed | accepted | not-applicable}}` | `{{concise_finding}}` | `{{redacted_evidence}}` | `{{remediation}}` | `{{owner_date}}` |

For each critical or high finding, explain exploit preconditions, affected authority/data, demonstrated versus theoretical impact, and why the severity is justified. Record false positives and rejected hypotheses separately.

## Approved changes

| Change ID | Approved scope | Before | After | Side effects | Validation | Rollback |
|---|---|---|---|---|---|---|
| `{{CHG-001}}` | `{{files_keys_services}}` | `{{redacted_before}}` | `{{redacted_after}}` | `{{effects}}` | `{{tests}}` | `{{restore_method}}` |

{{Confirm that no action outside the approved scope was taken.}}

## Validation evidence

| Gate | Test | Expected | Actual | Result | Evidence |
|---|---|---|---|---|---|
| `{{configuration}}` | `{{command_or_inspection}}` | `{{expected}}` | `{{actual}}` | `{{pass_fail_blocked}}` | `{{artifact_or_redacted_output}}` |

Include positive and denied-path tests for filesystem, network, credentials, authorization, multi-user isolation, timeout/cancel, restart, and rollback when applicable. A successful command exit is not sufficient without postcondition checks.

## External effects and reconciliation

| System | Intended effect | Observed state | Duplicate/partial risk | Reconciliation / compensation |
|---|---|---|---|---|
| `{{system}}` | `{{effect}}` | `{{verified_state}}` | `{{risk}}` | `{{action_or_not_required}}` |

## Residual risk, unknowns, and exceptions

| Item | Type | Impact | Compensating control | Owner | Expiry / revalidation trigger |
|---|---|---|---|---|---|
| `{{item}}` | `{{risk | unknown | exception}}` | `{{impact}}` | `{{control}}` | `{{owner}}` | `{{date_or_trigger}}` |

{{State clearly which claims could not be verified and why.}}

## Rollback and recovery status

| Recovery element | Location / reference | Restore test | Status | Owner |
|---|---|---|---|---|
| Code / package | `{{revision_or_backup}}` | `{{test}}` | `{{ready_not-ready}}` | `{{owner}}` |
| Configuration / service | `{{backup_or_diff}}` | `{{test}}` | `{{ready_not-ready}}` | `{{owner}}` |
| Sessions / memory / data | `{{backup_or_export}}` | `{{test}}` | `{{ready_not-ready}}` | `{{owner}}` |
| External compensation | `{{procedure}}` | `{{test_or_reconciliation}}` | `{{ready_not-ready}}` | `{{owner}}` |

## Evidence register

| Artifact | Source / command | Time | Hash or immutable identity | Redaction |
|---|---|---|---|---|
| `{{artifact}}` | `{{source}}` | `{{timestamp}}` | `{{hash_revision}}` | `{{none_or_method}}` |

## Sources

| Claim | First-party source | Verification date |
|---|---|---|
| `{{claim}}` | `{{url_or_immutable_source_path}}` | `{{yyyy-mm-dd}}` |

## Sign-off

| Role | Name | Decision | Date |
|---|---|---|---|
| Owner | `{{name}}` | `{{approve_reject}}` | `{{yyyy-mm-dd}}` |
| Security / reviewer | `{{name}}` | `{{approve_reject_conditions}}` | `{{yyyy-mm-dd}}` |
| Operator | `{{name}}` | `{{acknowledged}}` | `{{yyyy-mm-dd}}` |
