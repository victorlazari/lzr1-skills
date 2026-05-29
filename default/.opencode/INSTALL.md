# Installing lzr1 Default for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed

## Installation

Add `lzr1-default` to the `plugin` array in your `opencode.json` (global or project-level):

```json
{
  "plugin": ["lzr1-default@git+https://github.com/victorlazari/lzr1-skills.git#default"]
}
```

Restart OpenCode. The plugin installs through OpenCode's plugin manager and registers all lzr1 Default skills.

Verify by asking: "Tell me which lzr1 skills are available."

OpenCode uses its own plugin install. If you also use Claude Code, Codex, or another harness, install lzr1 Default separately for each one.

## Companion Plugins

`lzr1-default` provides the foundational `using-lzr1` bootstrap. The other lzr1 plugins assume it is installed:

- `lzr1-dev-team` — backend/frontend specialist agents and the 10-gate dev cycle
- `lzr1-pm-team` — pre-dev planning workflows
- `lzr1-tw-team` — technical writing specialists

Install whichever ones you need alongside `lzr1-default`:

```json
{
  "plugin": [
    "lzr1-default@git+https://github.com/victorlazari/lzr1-skills.git#default",
    "lzr1-dev-team@git+https://github.com/victorlazari/lzr1-skills.git#dev-team"
  ]
}
```

## Usage

Use OpenCode's native `skill` tool:

```
use skill tool to list skills
use skill tool to load lzr1:using-lzr1
```

## Updating

OpenCode installs lzr1 Default through a git-backed package spec. Some OpenCode and Bun versions pin the resolved git dependency in a lockfile or cache, so a restart may not pick up the newest commit. If updates do not appear, clear OpenCode's package cache or reinstall the plugin.

To pin a specific version:

```json
{
  "plugin": ["lzr1-default@git+https://github.com/victorlazari/lzr1-skills.git#v1.32.2"]
}
```

## Troubleshooting

### Plugin not loading

1. Check logs: `opencode run --print-logs "hello" 2>&1 | grep -i lzr1`
2. Verify the plugin line in your `opencode.json`
3. Make sure you're running a recent version of OpenCode

### Windows install issues

Some Windows OpenCode builds have upstream installer issues with git-backed plugin specs. If OpenCode cannot install the plugin, try installing with system npm and pointing OpenCode at the local package:

```powershell
npm install lzr1-default@git+https://github.com/victorlazari/lzr1-skills.git#default --prefix "$HOME\.config\opencode"
```

Then use the installed package path in `opencode.json`:

```json
{
  "plugin": ["~/.config/opencode/node_modules/lzr1-default"]
}
```

### Skills not found

1. Use `skill` tool to list what's discovered
2. Check that the plugin is loading (see above)
3. Verify `using-lzr1` is loadable: `use skill tool to load lzr1:using-lzr1`

### Tool mapping

When lzr1 skills reference Claude Code tools, OpenCode equivalents are auto-substituted:

- `TodoWrite` → `todowrite`
- `Task` (with subagents) → OpenCode's `@mention` syntax
- `Skill` tool → OpenCode's native `skill` tool
- `Read`, `Write`, `Edit`, `Bash` → native OpenCode tools

## Getting Help

- Report issues: https://github.com/victorlazari/lzr1-skills/issues
- Full documentation: https://github.com/victorlazari/lzr1-skills/tree/default
