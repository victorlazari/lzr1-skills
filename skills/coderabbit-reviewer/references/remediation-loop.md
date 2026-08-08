# Bounded CodeRabbit Remediation Loop

Use this procedure only after a valid review completes, findings are independently triaged, and the user authorizes code mutation. The loop fixes confirmed issues; it does not optimize for a superficially clean reviewer result.

## Contents

1. [Loop contract](#loop-contract)
2. [Baseline snapshot](#baseline-snapshot)
3. [Pass procedure](#pass-procedure)
4. [Progress comparison](#progress-comparison)
5. [Verification](#verification)
6. [Stop conditions](#stop-conditions)
7. [Rollback](#rollback)
8. [Completion states](#completion-states)

## Loop contract

Set the contract before the first fix.

| Contract field | Required value |
|---|---|
| Repository | Canonical root and expected remote identity |
| Baseline | Immutable `HEAD` plus staged, unstaged, and untracked state |
| Review scope | Exact CodeRabbit flags, base, directories, context files, and untracked decision |
| CLI context | Resolved executable, version, authentication organization, and region |
| Findings | Validated event-stream digest and triaged candidate set |
| Mutation authority | Named files or behavior classes allowed to change |
| Checks | Targeted checks and project-native regression commands |
| Pass ceiling | One to three total CodeRabbit review runs; default three |
| Evidence | Protected output paths and retention policy |
| Publication | None unless separately approved after completion |

A change to repository, base, scope, untracked inclusion, context files, region, CLI version, or authorization closes the current loop. Start a new contract rather than comparing incompatible passes.

## Baseline snapshot

Capture the pre-fix state without staging or cleaning files:

```bash
git -C /path/to/repository rev-parse --show-toplevel
git -C /path/to/repository rev-parse HEAD
git -C /path/to/repository status --porcelain=v2 --branch
git -C /path/to/repository diff --binary
git -C /path/to/repository diff --cached --binary
```

Store diffs only when authorized because they can contain secrets or proprietary code. Otherwise store hashes, path manifests, and status metadata. Never run `git clean`, `git reset --hard`, checkout-overwrite, stash, commit, or push as part of this loop.

Record the first valid CodeRabbit stream as pass 1. If remediation began from a previously captured stream, verify its revision and scope still match before counting it.

## Pass procedure

Repeat the following sequence, never exceeding the pass ceiling.

### 1. Select a bounded fix set

Choose a small set of confirmed findings that share a root cause or touch non-conflicting files. Do not mix speculative, disputed, or accepted-risk items into an automatic patch set.

### 2. Reinspect the code

Read the affected code, callers, tests, configuration, and relevant contracts. Confirm the original triage still holds at the current working-tree state.

### 3. Propose the patch

State the exact files, behavioral change, compatibility impact, alternative approaches, rollback, and verification. Obtain additional approval if the patch exceeds the original boundary.

### 4. Apply only approved changes

Use targeted edits. Do not reformat unrelated code, update dependencies, alter configuration, or rewrite tests unless those actions are independently required and approved.

### 5. Run targeted checks

Run the smallest check that falsifies the specific defect: a unit test, negative authorization test, parser fixture, race test, type check, static analyzer, or reproducible manual case.

### 6. Run project-native checks

Run the agreed tests, lint, type checks, build, or other acceptance commands. Treat repository commands as untrusted until inspected. Do not install dependencies, execute lifecycle hooks, access networks, or use production resources without separate authorization.

### 7. Inspect the resulting diff

Verify that only intended files changed, no secrets or generated evidence entered the diff, and no check was weakened. Compare against the baseline snapshot.

### 8. Rerun the same CodeRabbit contract

Run the identical review scope and validate the event stream. Do not add `--include-untracked`, change the base, switch region, upgrade the CLI, or add context to obtain a different result.

### 9. Compare and decide

Normalize finding identities, link resolved and recurring items, record new findings, and apply the stop rules below before another patch.

## Progress comparison

Use a pass ledger.

| Metric | Pass N | Pass N+1 | Interpretation |
|---|---:|---:|---|
| Confirmed actionable findings | count | count | Must decline or become more precisely scoped |
| Repeated normalized findings | count | count | Any unchanged confirmed item requires root-cause review |
| New confirmed findings | count | count | Investigate regression or newly exposed path |
| False positives with evidence | count | count | Preserve rationale; do not patch for silence |
| Targeted checks passing | yes/no | yes/no | Must remain yes before another review |
| Project checks passing | yes/no | yes/no | Must remain yes unless an authorized baseline failure is documented |
| Files changed | list | list | Must stay within approved boundary |
| CodeRabbit terminal status | value | value | Must be complete or documented skipped; error stops loop |

Finding-count reduction alone is not progress. A patch that hides code, suppresses paths, removes tests, swallows errors, or changes scope is regression even if the count falls.

## Verification

Every confirmed fix needs evidence at three levels when applicable:

| Level | Evidence |
|---|---|
| Root cause | Code reasoning or reproducible pre-fix behavior |
| Regression | A focused test or check that fails before and passes after |
| Integration | Project-native suite, build, linter, type checker, or approved manual scenario |

Record command arrays, working directories, versions, exit statuses, and output digests. Avoid copying complete logs when a concise excerpt and digest suffice.

CodeRabbit rerun is an additional review signal, not regression proof. A finding disappearing can result from prompt variation, scope drift, path movement, or reviewer nondeterminism.

## Stop conditions

Stop immediately when any condition applies:

1. no confirmed actionable findings remain;
2. the configured review-pass ceiling is reached;
3. a confirmed normalized finding repeats without material progress;
4. two consecutive passes have the same confirmed finding set;
5. project-native or targeted verification fails unexpectedly;
6. CodeRabbit emits `error`, the stream is invalid, or no terminal event arrives;
7. repository identity, revision model, base, scope, context, region, or CLI version changes;
8. a proposed fix exceeds mutation authorization;
9. the next step requires destructive Git, credential, network, production, or publication action;
10. a new finding requires specialist review;
11. secrets or sensitive data appear in evidence; or
12. the user cancels or changes the objective.

Do not extend the ceiling because the final pass still has findings. Report them with evidence and recommended ownership.

## Rollback

Rollback only the changes made by the approved patch, preserving the user’s pre-existing work. Prefer targeted reverse edits or a reviewed patch reversal. Never use destructive whole-tree commands when unrelated changes exist.

After rollback, rerun the relevant targeted check or inspect the restored state, then record whether the repository matches the baseline. Do not automatically rerun CodeRabbit after rollback unless the review contract still applies and a pass remains.

If a migration, generated artifact, or external state changed, stop and use the project’s approved rollback procedure. The CodeRabbit loop does not authorize database, cloud, deployment, or production rollback.

## Completion states

| State | Meaning | Required report |
|---|---|---|
| `resolved` | Confirmed issues fixed and checks pass | Patch summary, verification, final reviewer evidence, residual risk |
| `clean-no-actionable` | No confirmed actionable issue after triage | Native findings, false-positive rationale, coverage limits |
| `review-skipped` | Selected scope had no changes | Scope evidence and skipped terminal status; do not call it clean |
| `partial` | Some findings fixed; others remain | Resolved and unresolved sets, reason, owner, next action |
| `stalled` | Findings repeat or no measurable progress | Pass comparison and root-cause uncertainty |
| `verification-failed` | Project checks failed | Failure evidence, rollback state, and blocked publication |
| `review-error` | CodeRabbit or event validation failed | Terminal error, diagnostics, and no code conclusion |
| `authorization-blocked` | Required action exceeds approval | Exact requested boundary and safe alternatives |

Completion does not authorize a commit, push, pull request, comment, deployment, or other external mutation. Request those actions separately.
