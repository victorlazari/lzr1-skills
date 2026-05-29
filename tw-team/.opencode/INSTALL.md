# Installing lzr1 TW Team for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed
- `lzr1-default` installed — provides the `using-lzr1` bootstrap that orients agent behavior. See [../../default/.opencode/INSTALL.md](../../default/.opencode/INSTALL.md).

## Installation

Add `lzr1-tw-team` to the `plugin` array in your `opencode.json`, alongside `lzr1-default`:

```json
{
  "plugin": [
    "lzr1-default@git+https://github.com/victorlazari/lzr1-skills.git#default",
    "lzr1-tw-team@git+https://github.com/victorlazari/lzr1-skills.git#tw-team"
  ]
}
```

Restart OpenCode. The plugin registers lzr1 TW Team's skills and agents.

Verify by asking: "Which lzr1 technical writing skills are available?"

## What This Plugin Adds

- **3 specialist agents:** functional-writer, api-writer, docs-reviewer
- **6 documentation skills:** write-guide, write-api, voice-and-tone, documentation-structure, review-docs, using-tw-team

## Usage

Use OpenCode's native `skill` tool:

```
use skill tool to load lzr1:write-guide
use skill tool to load lzr1:write-api
```

## Updating

```json
{
  "plugin": ["lzr1-tw-team@git+https://github.com/victorlazari/lzr1-skills.git#v0.4.7"]
}
```

## Troubleshooting

### Skills not auto-triggelzr1

`lzr1-tw-team` relies on the `using-lzr1` bootstrap from `lzr1-default`. If skills aren't auto-triggelzr1, confirm `lzr1-default` is installed and its plugin is loading. See its [INSTALL.md](../../default/.opencode/INSTALL.md#troubleshooting).

### Skills not found

1. Use `skill` tool to list discovered skills
2. Verify plugin loading: `opencode run --print-logs "hello" 2>&1 | grep -i lzr1`
3. Confirm `lzr1-default` is also installed (required peer)

## Getting Help

- Report issues: https://github.com/victorlazari/lzr1-skills/issues
- Full documentation: https://github.com/victorlazari/lzr1-skills/tree/tw-team
