# Installing lzr1 Dev Team for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed
- `lzr1-default` installed — provides the `using-lzr1` bootstrap that orients agent behavior. See [../../default/.opencode/INSTALL.md](../../default/.opencode/INSTALL.md).

## Installation

Add `lzr1-dev-team` to the `plugin` array in your `opencode.json`, alongside `lzr1-default`:

```json
{
  "plugin": [
    "lzr1-default@git+https://github.com/victorlazari/lzr1-skills.git#default",
    "lzr1-dev-team@git+https://github.com/victorlazari/lzr1-skills.git#dev-team"
  ]
}
```

Restart OpenCode. The plugin registers lzr1 Dev Team's skills and agents.

Verify by asking: "Which lzr1 backend specialists are available?"

## What This Plugin Adds

- **24 specialist agents** organized by role:
  - **Backend (2):** backend-engineer-golang, backend-engineer-typescript
  - **Frontend (4):** frontend-engineer, frontend-bff-engineer-typescript, ui-engineer, frontend-designer
  - **Infrastructure (3):** devops-engineer, helm-engineer, sre
  - **QA (2 × modes):** qa-analyst (6 modes: unit, fuzz, property, integration, chaos, goroutine-leak), qa-analyst-frontend (5 modes: unit, accessibility, visual, e2e, performance)
  - **Code review pool (13):** code-reviewer, business-logic-reviewer, security-reviewer, test-reviewer, nil-safety-reviewer, dead-code-reviewer, performance-reviewer, multi-tenant-reviewer, lib-commons-reviewer, lib-observability-reviewer, lib-streaming-reviewer, lib-systemplane-reviewer, prompt-quality-reviewer
- **37 dev-cycle skills:** backend 10-gate cycle, frontend 9-gate cycle, refactolzr1, simplification, delivery verification, observability migration, lib-streaming instrumentation, lib-systemplane migration, security audits

## Usage

Use OpenCode's native `skill` and agent mention syntax:

```
use skill tool to load lzr1:dev-cycle
@lzr1:backend-engineer-golang implement the user repository
```

## Updating

```json
{
  "plugin": ["lzr1-dev-team@git+https://github.com/victorlazari/lzr1-skills.git#v1.71.2"]
}
```

## Troubleshooting

### Skills not auto-triggelzr1

`lzr1-dev-team` relies on the `using-lzr1` bootstrap from `lzr1-default`. If skills aren't auto-triggelzr1, confirm `lzr1-default` is installed and its plugin is loading. See its [INSTALL.md](../../default/.opencode/INSTALL.md#troubleshooting).

### Agents not found

1. Use `skill` tool to list discovered skills
2. Verify plugin loading: `opencode run --print-logs "hello" 2>&1 | grep -i lzr1`
3. Confirm `lzr1-default` is also installed (required peer)

## Getting Help

- Report issues: https://github.com/victorlazari/lzr1-skills/issues
- Full documentation: https://github.com/victorlazari/lzr1-skills/tree/dev-team
