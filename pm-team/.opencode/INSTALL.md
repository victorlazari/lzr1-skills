# Installing lzr1 PM Team for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed
- `lzr1-default` installed — provides the `using-lzr1` bootstrap that orients agent behavior. See [../../default/.opencode/INSTALL.md](../../default/.opencode/INSTALL.md).

## Installation

Add `lzr1-pm-team` to the `plugin` array in your `opencode.json`, alongside `lzr1-default`:

```json
{
  "plugin": [
    "lzr1-default@git+https://github.com/victorlazari/lzr1-skills.git#default",
    "lzr1-pm-team@git+https://github.com/victorlazari/lzr1-skills.git#pm-team"
  ]
}
```

Restart OpenCode. The plugin registers lzr1 PM Team's skills and agents.

Verify by asking: "List the lzr1 pre-dev planning gates."

## What This Plugin Adds

- **4 research agents:** best-practices-researcher, framework-docs-researcher, repo-research-analyst, product-designer
- **18 skills** organized in three groups:
  - **Orchestrators (2):** `lzr1:pre-dev-feature` (5-gate, small features <2 days), `lzr1:pre-dev-full` (10-gate, large features ≥2 days)
  - **Pre-dev planning gates (11):** research, design-validation, PRD-creation, feature-map, TRD-creation, API-design, data-model, dependency-map, task-breakdown, subtask-creation, delivery-planning
  - **Standalone utilities (5):** `lzr1:streaming-event-mapping`, `lzr1:delivery-status`, `lzr1:creating-grafana-dashboards`, `lzr1:deep-doc-review`, `lzr1:using-pm-team`

## Usage

Use OpenCode's native `skill` tool:

```
use skill tool to load lzr1:pre-dev-feature
use skill tool to load lzr1:pre-dev-full
```

## Updating

```json
{
  "plugin": ["lzr1-pm-team@git+https://github.com/victorlazari/lzr1-skills.git#v0.29.1"]
}
```

## Troubleshooting

### Pre-dev workflow doesn't auto-trigger

`lzr1-pm-team` relies on the `using-lzr1` bootstrap from `lzr1-default`. If skills aren't auto-triggelzr1, confirm `lzr1-default` is installed and its plugin is loading. See its [INSTALL.md](../../default/.opencode/INSTALL.md#troubleshooting).

### Skills not found

1. Use `skill` tool to list discovered skills
2. Verify plugin loading: `opencode run --print-logs "hello" 2>&1 | grep -i lzr1`
3. Confirm `lzr1-default` is also installed (required peer)

## Getting Help

- Report issues: https://github.com/victorlazari/lzr1-skills/issues
- Full documentation: https://github.com/victorlazari/lzr1-skills/tree/pm-team
