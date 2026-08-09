# Hermes Agent Sources and Freshness Policy

**Verified:** 2026-08-08

**Upstream snapshot:** `3e6a081d60e8d04a03d37008464f44555bc88832`
**Coverage:** 98 unique pages from the official documentation index, plus first-party repository, policy, release, installer, metadata, example, and source-tree fallback records.[105]

## Authority model

Use the highest available tier and record conflicts instead of silently reconciling them. Runtime discovery controls commands against the user's installation; it does not override the upstream security policy.[100]

| Tier | Evidence | Use |
|---:|---|---|
| 1 | Security policy and normative project policy | Security boundary, vulnerability scope, authorization requirement |
| 2 | Versioned first-party documentation | Supported workflow, command, key, or integration at the recorded date |
| 3 | Source, tests, package metadata, installer, release, and examples | Implementation behavior and volatile facts at a named revision |
| 4 | Read-only runtime discovery | Actual local version, commands, configuration, and enabled capabilities |

> Treat search snippets, community posts, model memory, generated prose, and marketing counts as discovery aids only. Do not let them control exact commands, flags, configuration keys, tool inventories, platform inventories, or security guarantees.

## Refresh procedure

Refresh this ledger before changing commands, defaults, configuration keys, integrations, provider behavior, isolation claims, or security guidance. Fetch the official documentation index, compare its unique canonical URLs with this table, review the latest release and security policy, and record the new upstream commit. Preserve source-tree fallbacks only when the rendered page is unavailable or incomplete; mark every fallback with its immutable commit.[101] [105]

Trigger an immediate refresh when the installed `hermes version` differs from the recorded package baseline, `hermes --help` conflicts with this package, a referenced page redirects or disappears, the security policy changes, or an upstream release modifies configuration, gateways, plugins, automation, or isolation.[35] [100] [101]

## Official documentation ledger

| # | Source | Topic | Rendered access | Research confidence |
|---:|---|---|---:|---:|
| 1 | [Adding a Platform Adapter][1] | `platform-adapters` | yes | 0.95 |
| 2 | [Adding Providers][2] | `adding-providers` | yes | 0.95 |
| 3 | [Adding Tools][3] | `adding-tools` | yes | 0.95 |
| 4 | [Agent Loop Internals][4] | `agent-loop-internals` | yes | 0.95 |
| 5 | [Architecture][5] | `architecture` | yes | 0.95 |
| 6 | [Context Compression and Caching][6] | `context-compression-and-caching` | yes | 0.95 |
| 7 | [Contributing][7] | `contributing-guidelines` | yes | 0.95 |
| 8 | [Creating Skills][8] | `creating-skills` | yes | 0.95 |
| 9 | [Extending the CLI][9] | `extending-the-cli` | yes | 0.95 |
| 10 | [Gateway Internals][10] | `gateway-internals` | yes | 0.95 |
| 11 | [Prompt Assembly][11] | `prompt-assembly` | yes | 0.95 |
| 12 | [Provider Runtime Resolution][12] | `provider-runtime` | yes | 0.95 |
| 13 | [Session Storage][13] | `session-storage` | yes | 0.95 |
| 14 | [Installation][14] | `installation` | yes | 0.95 |
| 15 | [Learning Path][15] | `learning-path` | yes | 0.95 |
| 16 | [Nix & NixOS Setup][16] | `nix-setup` | yes | 0.95 |
| 17 | [Quickstart][17] | `getting-started-quickstart` | yes | 0.95 |
| 18 | [Hermes on Android with Termux][18] | `termux-android-setup` | yes | 0.95 |
| 19 | [Updating & Uninstalling][19] | `updating-and-uninstalling` | yes | 0.95 |
| 20 | [Automate Anything with Cron][20] | `automate-with-cron` | yes | 0.95 |
| 21 | [Build a Hermes Plugin][21] | `build-a-hermes-plugin` | yes | 0.95 |
| 22 | [Tutorial: Build a Daily Briefing Bot][22] | `daily-briefing-bot` | yes | 0.95 |
| 23 | [Delegation & Parallel Work][23] | `delegation-patterns` | yes | 0.95 |
| 24 | [Tutorial: Build a GitHub PR Review Agent][24] | `github-pr-review-agent` | yes | 0.95 |
| 25 | [Run Local LLMs on Mac][25] | `local-llm-on-mac` | yes | 0.95 |
| 26 | [Using Hermes as a Python Library][26] | `python-library` | yes | 0.95 |
| 27 | [Tutorial: Team Telegram Assistant][27] | `telegram-gateway` | yes | 0.95 |
| 28 | [Tips & Best Practices][28] | `tips-and-best-practices` | yes | 0.95 |
| 29 | [Use MCP with Hermes][29] | `mcp-integration` | yes | 0.95 |
| 30 | [Use SOUL.md with Hermes][30] | `soul-md-configuration` | yes | 0.95 |
| 31 | [Use Voice Mode with Hermes][31] | `voice-mode` | yes | 0.95 |
| 32 | [Working with Skills][32] | `working-with-skills` | yes | 0.95 |
| 33 | [404 File not found][33] | `integrations-index` | no | 1.00 |
| 34 | [AI Providers][34] | `ai-providers` | yes | 0.95 |
| 35 | [CLI Commands Reference][35] | `cli-commands` | yes | 0.95 |
| 36 | [Environment Variables][36] | `environment-variables` | yes | 0.95 |
| 37 | [FAQ & Troubleshooting][37] | `faq-and-troubleshooting` | yes | 0.95 |
| 38 | [MCP Config Reference][38] | `mcp-config` | yes | 0.95 |
| 39 | [Model Catalog][39] | `model-catalog` | yes | 0.95 |
| 40 | [Optional Skills Catalog][40] | `optional-skills-catalog` | yes | 0.95 |
| 41 | [Profile Commands Reference][41] | `profile-commands` | yes | 0.95 |
| 42 | [Bundled Skills Catalog][42] | `skills-catalog` | yes | 0.95 |
| 43 | [Slash Commands Reference][43] | `slash-commands` | yes | 0.95 |
| 44 | [Tools & Skills Reference][44] | `tools-reference` | no | 0.80 |
| 45 | [Toolsets Reference][45] | `toolsets-reference` | yes | 0.95 |
| 46 | [Checkpoints and `/rollback`][46] | `checkpoints-and-rollback` | yes | 0.95 |
| 47 | [CLI Interface][47] | `cli-interface` | yes | 0.95 |
| 48 | [Configuration][48] | `configuration` | yes | 0.95 |
| 49 | [Configuring Models][49] | `configuring-models` | yes | 0.95 |
| 50 | [Hermes Agent — Docker][50] | `docker-deployment` | no | 0.90 |
| 51 | [ACP Host Integration][51] | `acp-host-integration` | yes | 0.95 |
| 52 | [API Server][52] | `api-server` | yes | 0.95 |
| 53 | [Batch Processing][53] | `batch-processing` | yes | 0.95 |
| 54 | [Browser Automation][54] | `browser-automation` | yes | 0.95 |
| 55 | [Built-in Plugins][55] | `built-in-plugins` | yes | 0.95 |
| 56 | [Code Execution][56] | `code-execution` | yes | 0.95 |
| 57 | [Context Files][57] | `context-files` | yes | 1.00 |
| 58 | [Context References][58] | `context-references` | yes | 0.95 |
| 59 | [Credential Pools][59] | `credential-pools` | yes | 0.95 |
| 60 | [Scheduled Tasks (Cron)][60] | `cron-management` | yes | 0.95 |
| 61 | [Curator][61] | `curator-maintenance` | yes | 0.95 |
| 62 | [Subagent Delegation][62] | `subagent-delegation` | yes | 0.95 |
| 63 | [Fallback Providers][63] | `fallback-providers` | yes | 0.95 |
| 64 | [Persistent Goals][64] | `persistent-goals` | yes | 0.95 |
| 65 | [Honcho Memory][65] | `honcho-memory` | no | 0.90 |
| 66 | [Event Hooks][66] | `hooks` | yes | 0.95 |
| 67 | [Image Generation][67] | `image-generation` | yes | 0.95 |
| 68 | [Kanban (Multi-Agent Board)][68] | `kanban-multi-agent-board` | yes | 0.95 |
| 69 | [Kanban tutorial][69] | `kanban-tutorial` | yes | 0.95 |
| 70 | [MCP (Model Context Protocol)][70] | `mcp-integration` | yes | 0.95 |
| 71 | [Persistent Memory][71] | `persistent-memory` | yes | 0.95 |
| 72 | [Memory Providers][72] | `memory-providers` | yes | 0.95 |
| 73 | [Features Overview][73] | `features-overview` | yes | 0.95 |
| 74 | [Personality & SOUL.md][74] | `personality-and-identity` | yes | 0.95 |
| 75 | [Plugins][75] | `plugins` | yes | 0.95 |
| 76 | [Provider Routing][76] | `provider-routing` | yes | 0.95 |
| 77 | [Skills System][77] | `skills-system` | yes | 0.95 |
| 78 | [Tools & Toolsets][78] | `tools-and-toolsets` | yes | 0.95 |
| 79 | [Voice & TTS][79] | `voice-and-tts` | yes | 0.95 |
| 80 | [Vision & Image Paste][80] | `vision-and-image-paste` | yes | 0.95 |
| 81 | [Voice Mode][81] | `voice-mode` | yes | 0.95 |
| 82 | [Git Worktrees][82] | `git-worktrees` | yes | 0.95 |
| 83 | [Discord][83] | `messaging-discord` | yes | 0.95 |
| 84 | [Email][84] | `email-gateway` | yes | 0.95 |
| 85 | [Home Assistant][85] | `home-assistant-integration` | yes | 0.95 |
| 86 | [Messaging Gateway][86] | `messaging-gateway` | yes | 0.95 |
| 87 | [Matrix Setup][87] | `messaging-matrix` | yes | 0.95 |
| 88 | [Mattermost Setup][88] | `messaging-mattermost` | yes | 0.95 |
| 89 | [Signal][89] | `messaging-signal` | yes | 0.95 |
| 90 | [Slack Setup][90] | `messaging-slack` | yes | 0.95 |
| 91 | [SMS Setup (Twilio)][91] | `messaging-sms` | yes | 0.95 |
| 92 | [Telegram][92] | `messaging-telegram` | yes | 0.95 |
| 93 | [Webhooks][93] | `messaging-webhooks` | yes | 0.95 |
| 94 | [WhatsApp Setup][94] | `whatsapp-integration` | yes | 0.95 |
| 95 | [Profiles: Running Multiple Agents][95] | `profile-management` | yes | 0.95 |
| 96 | [Security][96] | `security-model` | yes | 0.95 |
| 97 | [Sessions][97] | `session-management` | yes | 0.95 |
| 98 | [TUI][98] | `tui` | yes | 0.95 |

Entries 33, 44, 50, and 65 were unavailable or incomplete through rendered extraction at research time. Use the immutable first-party source fallbacks [106] [107] [108] [109] and re-test the canonical pages during refresh.

## Additional first-party controls

| # | Source | Role |
|---:|---|---|
| 99 | [Upstream repository][99] | project source |
| 100 | [Security policy][100] | normative security boundary |
| 101 | [Release v2026.8.3][101] | release metadata |
| 102 | [Package metadata at research snapshot][102] | version and dependencies |
| 103 | [Installer at research snapshot][103] | installation behavior |
| 104 | [Configuration example at research snapshot][104] | configuration examples |
| 105 | [Official documentation index][105] | canonical documentation inventory |
| 106 | [Integrations index source fallback][106] | rendered page unavailable |
| 107 | [Tools reference source fallback][107] | rendered page incomplete |
| 108 | [Docker guide source fallback][108] | rendered page unavailable |
| 109 | [Honcho guide source fallback][109] | rendered page unavailable |

## References

[1]: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters "Adding a Platform Adapter"
[2]: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-providers "Adding Providers"
[3]: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-tools "Adding Tools"
[4]: https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop "Agent Loop Internals"
[5]: https://hermes-agent.nousresearch.com/docs/developer-guide/architecture "Architecture"
[6]: https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching "Context Compression and Caching"
[7]: https://hermes-agent.nousresearch.com/docs/developer-guide/contributing "Contributing"
[8]: https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills "Creating Skills"
[9]: https://hermes-agent.nousresearch.com/docs/developer-guide/extending-the-cli "Extending the CLI"
[10]: https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-internals "Gateway Internals"
[11]: https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly "Prompt Assembly"
[12]: https://hermes-agent.nousresearch.com/docs/developer-guide/provider-runtime "Provider Runtime Resolution"
[13]: https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage "Session Storage"
[14]: https://hermes-agent.nousresearch.com/docs/getting-started/installation "Installation"
[15]: https://hermes-agent.nousresearch.com/docs/getting-started/learning-path "Learning Path"
[16]: https://hermes-agent.nousresearch.com/docs/getting-started/nix-setup "Nix & NixOS Setup"
[17]: https://hermes-agent.nousresearch.com/docs/getting-started/quickstart "Quickstart"
[18]: https://hermes-agent.nousresearch.com/docs/getting-started/termux "Hermes on Android with Termux"
[19]: https://hermes-agent.nousresearch.com/docs/getting-started/updating "Updating & Uninstalling"
[20]: https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron "Automate Anything with Cron"
[21]: https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin "Build a Hermes Plugin"
[22]: https://hermes-agent.nousresearch.com/docs/guides/daily-briefing-bot "Tutorial: Build a Daily Briefing Bot"
[23]: https://hermes-agent.nousresearch.com/docs/guides/delegation-patterns "Delegation & Parallel Work"
[24]: https://hermes-agent.nousresearch.com/docs/guides/github-pr-review-agent "Tutorial: Build a GitHub PR Review Agent"
[25]: https://hermes-agent.nousresearch.com/docs/guides/local-llm-on-mac "Run Local LLMs on Mac"
[26]: https://hermes-agent.nousresearch.com/docs/guides/python-library "Using Hermes as a Python Library"
[27]: https://hermes-agent.nousresearch.com/docs/guides/team-telegram-assistant "Tutorial: Team Telegram Assistant"
[28]: https://hermes-agent.nousresearch.com/docs/guides/tips "Tips & Best Practices"
[29]: https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes "Use MCP with Hermes"
[30]: https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes "Use SOUL.md with Hermes"
[31]: https://hermes-agent.nousresearch.com/docs/guides/use-voice-mode-with-hermes "Use Voice Mode with Hermes"
[32]: https://hermes-agent.nousresearch.com/docs/guides/work-with-skills "Working with Skills"
[33]: https://hermes-agent.nousresearch.com/docs/integrations/index "404 File not found"
[34]: https://hermes-agent.nousresearch.com/docs/integrations/providers "AI Providers"
[35]: https://hermes-agent.nousresearch.com/docs/reference/cli-commands "CLI Commands Reference"
[36]: https://hermes-agent.nousresearch.com/docs/reference/environment-variables "Environment Variables"
[37]: https://hermes-agent.nousresearch.com/docs/reference/faq "FAQ & Troubleshooting"
[38]: https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference "MCP Config Reference"
[39]: https://hermes-agent.nousresearch.com/docs/reference/model-catalog "Model Catalog"
[40]: https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog "Optional Skills Catalog"
[41]: https://hermes-agent.nousresearch.com/docs/reference/profile-commands "Profile Commands Reference"
[42]: https://hermes-agent.nousresearch.com/docs/reference/skills-catalog "Bundled Skills Catalog"
[43]: https://hermes-agent.nousresearch.com/docs/reference/slash-commands "Slash Commands Reference"
[44]: https://hermes-agent.nousresearch.com/docs/reference/tools-reference "Tools & Skills Reference"
[45]: https://hermes-agent.nousresearch.com/docs/reference/toolsets-reference "Toolsets Reference"
[46]: https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback "Checkpoints and `/rollback`"
[47]: https://hermes-agent.nousresearch.com/docs/user-guide/cli "CLI Interface"
[48]: https://hermes-agent.nousresearch.com/docs/user-guide/configuration "Configuration"
[49]: https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models "Configuring Models"
[50]: https://hermes-agent.nousresearch.com/docs/user-guide/docker "Hermes Agent — Docker"
[51]: https://hermes-agent.nousresearch.com/docs/user-guide/features/acp "ACP Host Integration"
[52]: https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server "API Server"
[53]: https://hermes-agent.nousresearch.com/docs/user-guide/features/batch-processing "Batch Processing"
[54]: https://hermes-agent.nousresearch.com/docs/user-guide/features/browser "Browser Automation"
[55]: https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins "Built-in Plugins"
[56]: https://hermes-agent.nousresearch.com/docs/user-guide/features/code-execution "Code Execution"
[57]: https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files "Context Files"
[58]: https://hermes-agent.nousresearch.com/docs/user-guide/features/context-references "Context References"
[59]: https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-pools "Credential Pools"
[60]: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron "Scheduled Tasks (Cron)"
[61]: https://hermes-agent.nousresearch.com/docs/user-guide/features/curator "Curator"
[62]: https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation "Subagent Delegation"
[63]: https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers "Fallback Providers"
[64]: https://hermes-agent.nousresearch.com/docs/user-guide/features/goals "Persistent Goals"
[65]: https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho "Honcho Memory"
[66]: https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks "Event Hooks"
[67]: https://hermes-agent.nousresearch.com/docs/user-guide/features/image-generation "Image Generation"
[68]: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban "Kanban (Multi-Agent Board)"
[69]: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial "Kanban tutorial"
[70]: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp "MCP (Model Context Protocol)"
[71]: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory "Persistent Memory"
[72]: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers "Memory Providers"
[73]: https://hermes-agent.nousresearch.com/docs/user-guide/features/overview "Features Overview"
[74]: https://hermes-agent.nousresearch.com/docs/user-guide/features/personality "Personality & SOUL.md"
[75]: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins "Plugins"
[76]: https://hermes-agent.nousresearch.com/docs/user-guide/features/provider-routing "Provider Routing"
[77]: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills "Skills System"
[78]: https://hermes-agent.nousresearch.com/docs/user-guide/features/tools "Tools & Toolsets"
[79]: https://hermes-agent.nousresearch.com/docs/user-guide/features/tts "Voice & TTS"
[80]: https://hermes-agent.nousresearch.com/docs/user-guide/features/vision "Vision & Image Paste"
[81]: https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode "Voice Mode"
[82]: https://hermes-agent.nousresearch.com/docs/user-guide/git-worktrees "Git Worktrees"
[83]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord "Discord"
[84]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/email "Email"
[85]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant "Home Assistant"
[86]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/index "Messaging Gateway"
[87]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/matrix "Matrix Setup"
[88]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/mattermost "Mattermost Setup"
[89]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/signal "Signal"
[90]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/slack "Slack Setup"
[91]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/sms "SMS Setup (Twilio)"
[92]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram "Telegram"
[93]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks "Webhooks"
[94]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp "WhatsApp Setup"
[95]: https://hermes-agent.nousresearch.com/docs/user-guide/profiles "Profiles: Running Multiple Agents"
[96]: https://hermes-agent.nousresearch.com/docs/user-guide/security "Security"
[97]: https://hermes-agent.nousresearch.com/docs/user-guide/sessions "Sessions"
[98]: https://hermes-agent.nousresearch.com/docs/user-guide/tui "TUI"
[99]: https://github.com/NousResearch/hermes-agent "Upstream repository"
[100]: https://github.com/NousResearch/hermes-agent/blob/main/SECURITY.md "Security policy"
[101]: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.3 "Release v2026.8.3"
[102]: https://github.com/NousResearch/hermes-agent/blob/3e6a081d60e8d04a03d37008464f44555bc88832/pyproject.toml "Package metadata at research snapshot"
[103]: https://github.com/NousResearch/hermes-agent/blob/3e6a081d60e8d04a03d37008464f44555bc88832/install.sh "Installer at research snapshot"
[104]: https://github.com/NousResearch/hermes-agent/blob/3e6a081d60e8d04a03d37008464f44555bc88832/cli-config.yaml.example "Configuration example at research snapshot"
[105]: https://hermes-agent.nousresearch.com/docs/llms.txt "Official documentation index"
[106]: https://github.com/NousResearch/hermes-agent/blob/3e6a081d60e8d04a03d37008464f44555bc88832/website/docs/integrations/index.md "Integrations index source fallback"
[107]: https://github.com/NousResearch/hermes-agent/blob/3e6a081d60e8d04a03d37008464f44555bc88832/website/docs/reference/tools-reference.md "Tools reference source fallback"
[108]: https://github.com/NousResearch/hermes-agent/blob/3e6a081d60e8d04a03d37008464f44555bc88832/website/docs/user-guide/docker.md "Docker guide source fallback"
[109]: https://github.com/NousResearch/hermes-agent/blob/3e6a081d60e8d04a03d37008464f44555bc88832/website/docs/user-guide/features/honcho.md "Honcho guide source fallback"
