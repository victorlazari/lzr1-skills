# Hermes Agent Change Plan

**Change ID:** `{{change_id}}`

**Owner:** `{{owner}}`

**Prepared by:** `{{author}}`

**Planned window:** `{{timestamp_and_timezone}}`
**Status:** `{{draft | awaiting-consent | approved | executing | validated | rolled-back | blocked}}`

> This plan authorizes only the targets and effects listed below. New files, services, credentials, users, destinations, tools, or external effects require a revised plan and fresh consent.

## Objective and success criteria

{{Describe the requested outcome, business or technical purpose, and measurable completion criteria.}}

| Field | Value |
|---|---|
| Target revision/version | `{{immutable_revision_or_version}}` |
| Installation / environment | `{{method_runtime_os}}` |
| Profile / Hermes home | `{{redacted_profile_and_path}}` |
| Deployment / input trust | `{{deployment}}` / `{{controlled_mixed_untrusted}}` |
| Data sensitivity | `{{classification}}` |
| Approved execution identity | `{{user_service_account}}` |
| Approved window | `{{start_end_timezone}}` |
| Expiry of authorization | `{{timestamp_or_condition}}` |

## Current baseline

| Component | Current state | Evidence |
|---|---|---|
| Code/package | `{{revision_version_hash}}` | `{{source}}` |
| Configuration | `{{paths_hashes_permissions}}` | `{{redacted_check}}` |
| Services/listeners | `{{units_processes_bindings}}` | `{{inspection}}` |
| Providers/models | `{{provider_endpoint_host_model}}` | `{{runtime_discovery}}` |
| Tools/extensions | `{{tools_skills_plugins_mcp_hooks}}` | `{{inventory}}` |
| State/data | `{{sessions_memory_workspaces_logs}}` | `{{inventory}}` |

## Scope and exclusions

| In scope | Out of scope |
|---|---|
| `{{approved_targets_and_actions}}` | `{{explicitly_excluded_targets_and_actions}}` |

## Threat and side-effect review

| Risk surface | Planned control |
|---|---|
| Untrusted input | `{{classification_and_handling}}` |
| Host and terminal isolation | `{{whole_process_and_backend_boundaries}}` |
| Filesystem | `{{allowed_paths_symlink_policy_backup}}` |
| Network | `{{allowed_destinations_listener_policy}}` |
| Credentials | `{{named_secret_classes_scope_rotation}}` |
| External systems | `{{accounts_effects_idempotency_compensation}}` |
| Multi-user state | `{{session_workspace_memory_isolation}}` |
| Automation | `{{budgets_retries_expiry_kill_switch}}` |

## Proposed changes

| Step | Exact target | Proposed change | Why | Side effect | Reversible | Operator |
|---:|---|---|---|---|---|---|
| 1 | `{{file_key_service_account}}` | `{{redacted_diff_or_action}}` | `{{reason}}` | `{{effect}}` | `{{yes_no_and_method}}` | `{{identity}}` |

For configuration or code, attach a redacted before/after diff. For commands, list the exact reviewed command and working directory. For provider, gateway, or external-system changes, list endpoint host, identity, scope, and destination without secret values.

## Credential and data handling

| Item | Source | Destination | Storage | Exposure | Rotation/deletion |
|---|---|---|---|---|---|
| `{{credential_or_data_class}}` | `{{source}}` | `{{destination}}` | `{{location_and_permissions}}` | `{{provider_service_log}}` | `{{procedure}}` |

{{State whether any secret value will be read, transmitted, or entered, and by whom.}}

## Backup and rollback

| Component | Checkpoint / backup | Integrity | Restore procedure | Restore validation |
|---|---|---|---|---|
| Code/package | `{{revision_archive_or_snapshot}}` | `{{hash}}` | `{{procedure}}` | `{{test}}` |
| Configuration/service | `{{backup}}` | `{{hash_permissions}}` | `{{procedure}}` | `{{test}}` |
| State/data | `{{backup_export}}` | `{{hash}}` | `{{procedure}}` | `{{test}}` |
| External effect | `{{idempotency_or_compensation}}` | `{{remote_state_reference}}` | `{{procedure}}` | `{{reconciliation}}` |

**Rollback triggers:** {{List explicit failed gates, security events, time limits, or operator decisions that require rollback.}}

## Execution controls

| Control | Value |
|---|---|
| Time limit | `{{duration}}` |
| Cost/token budget | `{{budget_or_not_applicable}}` |
| Concurrency | `{{limit}}` |
| Retry policy | `{{count_classes_backoff}}` |
| Output size | `{{limit}}` |
| Kill switch | `{{exact_control_and_owner}}` |
| Logging/redaction | `{{policy}}` |

## Consent record

| Consent item | Decision | Approver | Time | Conditions |
|---|---|---|---|---|
| File/config/service mutation | `{{approved_denied_not-applicable}}` | `{{identity}}` | `{{timestamp}}` | `{{conditions}}` |
| Network/public exposure | `{{approved_denied_not-applicable}}` | `{{identity}}` | `{{timestamp}}` | `{{conditions}}` |
| Credential/data disclosure | `{{approved_denied_not-applicable}}` | `{{identity}}` | `{{timestamp}}` | `{{conditions}}` |
| External mutation/message | `{{approved_denied_not-applicable}}` | `{{identity}}` | `{{timestamp}}` | `{{conditions}}` |
| Persistent automation/service | `{{approved_denied_not-applicable}}` | `{{identity}}` | `{{timestamp}}` | `{{conditions}}` |

## Validation plan

| Gate | Test | Expected result | Evidence to retain | Rollback on failure |
|---|---|---|---|---|
| Configuration | `{{check}}` | `{{expected}}` | `{{artifact}}` | `{{yes_no}}` |
| Functional | `{{harmless_positive_test}}` | `{{expected}}` | `{{artifact}}` | `{{yes_no}}` |
| Authorization | `{{denied_identity_action}}` | `{{denied}}` | `{{artifact}}` | `{{yes_no}}` |
| Isolation | `{{path_env_network_negative_test}}` | `{{denied}}` | `{{artifact}}` | `{{yes_no}}` |
| Restart/recovery | `{{test}}` | `{{expected}}` | `{{artifact}}` | `{{yes_no}}` |
| External state | `{{reconciliation}}` | `{{exact_state}}` | `{{artifact}}` | `{{compensate}}` |

## Execution record

| Step | Start/end | Result | Evidence | Deviation / approval |
|---:|---|---|---|---|
| 1 | `{{timestamps}}` | `{{pass_fail_blocked}}` | `{{redacted_artifact}}` | `{{none_or_record}}` |

## Completion decision

{{State whether every success criterion passed, whether rollback occurred, and which residual risks remain.}}

| Role | Name | Decision | Date |
|---|---|---|---|
| Owner | `{{name}}` | `{{accept_reject}}` | `{{yyyy-mm-dd}}` |
| Reviewer | `{{name}}` | `{{accept_reject_conditions}}` | `{{yyyy-mm-dd}}` |
| Operator | `{{name}}` | `{{completed_rolled-back_blocked}}` | `{{yyyy-mm-dd}}` |
