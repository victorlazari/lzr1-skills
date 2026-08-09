# Hermes Agent Automation and Multi-Agent Operations

**Read this reference** before scheduling cron jobs, enabling hooks, using delegation, persistent goals, Kanban, batch processing, worktrees, background services, or any unattended Hermes workflow. **Verified:** 2026-08-08.

Commands, schemas, defaults, concurrency, recovery semantics, and platform support are volatile. Verify the installed version and relevant first-party documentation before execution.[1] [2]

> Automation converts a prompt into persistent authority. Require a scoped identity, bounded tools, explicit inputs and outputs, spend/time limits, deterministic validation, an audit trail, and a tested kill switch before unattended execution.

## Classify the automation

Record the trigger, owner, execution identity, profile/home, workspace, input source and trust, data class, provider/model, allowed tools, external destinations, persistence, concurrency, cost, stop condition, and rollback.

| Pattern | Main additional risk |
|---|---|
| Cron/scheduled task | Repeated unattended effects and stale credentials/configuration |
| Hook | Hidden execution around lifecycle events, recursion, blocking, secret exposure |
| Delegation/subagent | Authority propagation, conflicting results, unbounded parallelism |
| Persistent goal | Self-continuation, weak completion criteria, accumulated cost/state |
| Kanban board | Multi-agent races, task ownership ambiguity, shared artifacts |
| Batch processing | Dataset injection, high concurrency/spend, partial output/resume errors |
| Worktree agent | Concurrent repository mutation, branch confusion, cleanup loss |
| Gateway service | Persistent external ingress and outbound delivery |

If the operation cannot be safely repeated, reconciled after partial failure, and stopped independently, do not schedule it.

## Establish an unattended-execution contract

Use a written contract before creating automation:

1. **Owner and purpose:** human accountable for the job and exact business outcome.
2. **Trigger:** schedule/event, timezone, jitter, duplicate-trigger handling, and expiry.
3. **Identity:** dedicated OS/service/profile/provider/external-system credentials.
4. **Inputs:** canonical source, authorization, schema, size, trust, and freshness.
5. **Tools:** explicit allowlist; no unrestricted/Yolo mode.
6. **Effects:** approved files, branches, records, messages, or endpoints.
7. **Budgets:** wall-clock, turns/tool calls, tokens/cost, concurrency, output size, and retries.
8. **Quality gates:** deterministic tests, policy checks, human review threshold, and denied paths.
9. **Idempotency:** run key, duplicate prevention, reconciliation, and compensating action.
10. **Observability:** run ID, start/end, source revision, redacted logs, outputs, and alerts.
11. **Kill switch:** exact command/control plane, owner, maximum stop latency, and orphan cleanup.
12. **Rollback:** checkpoint, backup, prior revision, external compensation, and validation.

Require explicit consent for this contract and again for material scope increases.

## Schedule cron safely

Hermes documents cron management and isolated/non-isolated execution modes. Confirm current CLI, schedule syntax, storage, delivery behavior, and service dependency at runtime.[3] [4]

Prefer isolated sessions for unattended jobs unless continuity is required and explicitly approved. Use a dedicated profile and workspace. Never embed secrets in the schedule, prompt, command line, or description.

Before creation, preview the exact schedule and timezone, next runs, prompt/input, model/provider, allowed tools, destination/delivery, timeout, retry ceiling, expiry, and removal command. Avoid high-frequency schedules until one manual run passes under the same identity and environment.

Test missed-run, overlap, duplicate trigger, reboot, credential expiry, provider outage, output failure, and cancellation. A successful creation command does not prove the job will run safely.

## Design hooks defensively

Hooks can run commands around lifecycle events and may block or observe agent activity. Treat hook configuration and scripts as privileged code.[5]

Pin the script, use absolute paths, set a minimal environment, bound input/output, time out execution, prevent recursion, and fail safely. Do not pass full prompts, tool results, secrets, or session data to a hook unless necessary and approved. Avoid shell interpolation of untrusted event fields.

A blocking hook can enforce a policy only within its implemented scope. It cannot replace process isolation or user authorization. Test malformed input, slow execution, non-zero exit, missing executable, secret redaction, and reentrancy.

## Delegate with least authority

Hermes supports subagent delegation and parallel work. Delegate only tasks that are independent, bounded, and mergeable.[6] [7]

Each subtask must receive the minimum context and tools plus a structured result schema:

| Field | Required value |
|---|---|
| Task ID | Stable identifier tied to the parent run |
| Objective | One concrete outcome |
| Inputs | Approved files/URLs/data and trust classification |
| Allowed tools/effects | Explicit list; deny everything else |
| Limits | Time, turns, tokens/cost, concurrency, retries |
| Evidence | Sources, commands, tests, and uncertainty |
| Output | Typed artifact or structured fields |
| Stop | Success, blocked, failed, or cancelled condition |

The parent must validate results independently. Do not let one subagent approve another's side effects or merge untrusted code without deterministic checks. Cap fan-out and total budget; a child cannot grant itself more authority.

## Operate persistent goals

Persistent goals can continue work over time. Define a measurable completion predicate, maximum duration/runs/cost, allowed tools, review cadence, pause/kill control, and expiry before enabling.[8]

Do not use open-ended goals such as “keep improving” against production systems or external accounts. Split them into reviewable milestones. Require human approval before crossing from analysis to mutation, expanding targets, installing dependencies, messaging users, or spending money.

At each resume, revalidate version, credentials, target state, input trust, and prior partial effects. Do not assume yesterday's authorization remains valid after scope or environment changes.

## Coordinate Kanban/multi-agent boards

Kanban workflows can distribute tasks across agents and maintain shared board state. Define board ownership, authenticated access, task schema, claim/lease semantics, dependency rules, artifact paths, branch strategy, conflict policy, and close criteria.[9] [10]

Use one writer or transactional/lease controls for shared fields. Separate research, implementation, review, and approval roles. Prevent agents from marking work complete based only on self-report; require tests and artifact evidence.

Test agent crash, duplicate claim, lease expiry, stale task, conflicting writes, blocked dependency, board corruption, and recovery from a known snapshot.

## Process batches safely

Batch mode can process many inputs concurrently and resume partial work. Validate the dataset schema, source authorization, row identity, prompt-injection risk, output directory, overwrite behavior, concurrency, timeout, provider limits, spend ceiling, and resume semantics.[11]

Use immutable input snapshots and per-item identifiers. Write outputs atomically, preserve item-level status, and distinguish retryable provider failures from invalid data or committed side effects. Never retry ambiguous external writes automatically.

Pilot a representative sample, including malformed and adversarial records, before full execution. Verify the final count against the immutable input and account for every failed/skipped item.

## Use worktrees for repository concurrency

Git worktrees isolate working directories, not credentials, repository object storage, remote permissions, service state, or external side effects.[12]

Assign one branch/worktree per task, prevent overlapping ownership, pin the base revision, and define merge order. Run repository-specific tests in each worktree. Do not allow agents to force-push, alter protected branches, delete another worktree, or merge without explicit authorization.

Before cleanup, preserve uncommitted changes, test artifacts, review notes, and recovery references. Verify no process still uses the worktree.

## Gate external effects

Unattended workflows must not post messages, open/merge pull requests, modify tickets, deploy, purchase, delete, or change accounts solely because a model decided to. Use a two-phase pattern:

1. Generate a preview artifact with exact destination and payload.
2. Apply deterministic policy and quality checks.
3. Obtain required human or separately authorized approval.
4. Execute through a narrow, idempotent tool.
5. Reconcile the external state and record evidence.

Keep read/research identities separate from write identities where practical.

## Validate, monitor, and stop

A pre-production test must cover success, denied action, malformed input, duplicate trigger, retry, provider failure, timeout, cancellation, restart, partial output, credential expiry, budget exhaustion, and rollback.

Monitor run age, queue depth, concurrency, error class, retry count, provider/cost, output delivery, orphan processes, and authorization denials. Alerts must not include secrets or sensitive prompt content.

Test the kill switch before launch. Stopping the scheduler is insufficient if child processes, remote sandboxes, provider requests, gateway deliveries, or external mutations continue. Reconcile each layer.

## Failure handling

| Failure | Safe response |
|---|---|
| Overlapping runs | Stop new starts; lease/lock; reconcile both run IDs |
| Budget exceeded | Cancel children and remote work; preserve partial artifacts |
| Retry storm | Disable schedule/queue; classify first failure; do not replay writes |
| Output delivered twice | Stop delivery; use idempotency key and reconcile recipients |
| Agent expands scope | Deny; require a new plan and consent |
| Hook blocks service | Disable through approved rollback; preserve event/log evidence |
| Board/task conflict | Freeze writers; restore/repair from a known snapshot |
| Worktree conflict | Stop merge; preserve branches; rebase/resolve under human review |
| Kill switch incomplete | Escalate incident; revoke credentials and isolate network if needed |

## Required report

Report the automation contract, owner, schedule/trigger, identity, scopes, tools, budgets, deterministic gates, dry run, negative tests, kill-switch test, run evidence, external effects, residual risks, and rollback. Never call automation “autonomous and safe”; state the bounded authority and tested failure modes.

## References

[1]: https://hermes-agent.nousresearch.com/docs/reference/cli-commands "CLI commands reference"
[2]: https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop "Agent loop internals"
[3]: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron "Scheduled tasks"
[4]: https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron "Automate with cron"
[5]: https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks "Event hooks"
[6]: https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation "Subagent delegation"
[7]: https://hermes-agent.nousresearch.com/docs/guides/delegation-patterns "Delegation and parallel work"
[8]: https://hermes-agent.nousresearch.com/docs/user-guide/features/goals "Persistent goals"
[9]: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban "Kanban multi-agent board"
[10]: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial "Kanban tutorial"
[11]: https://hermes-agent.nousresearch.com/docs/user-guide/features/batch-processing "Batch processing"
[12]: https://hermes-agent.nousresearch.com/docs/user-guide/git-worktrees "Git worktrees"
