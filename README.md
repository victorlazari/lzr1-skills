<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=lzr1-skills&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=32&desc=AI%20Skills%20Arsenal&descAlignY=55&descSize=18" width="100%"/>

<div align="center">

[![Stars](https://img.shields.io/github/stars/victorlazari/lzr1-skills?style=flat-square&color=a855f7&labelColor=1a1a2e)](https://github.com/victorlazari/lzr1-skills/stargazers)
[![License](https://img.shields.io/badge/license-MIT-06b6d4?style=flat-square&labelColor=1a1a2e)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-32-ec4899?style=flat-square&labelColor=1a1a2e)](skills/)
[![macOS](https://img.shields.io/badge/macOS-✓-a855f7?style=flat-square&labelColor=1a1a2e)](install.sh)
[![Linux](https://img.shields.io/badge/Linux-✓-06b6d4?style=flat-square&labelColor=1a1a2e)](install.sh)
[![Made with Bash](https://img.shields.io/badge/made%20with-bash-ec4899?style=flat-square&labelColor=1a1a2e&logo=gnubash&logoColor=white)](install.sh)

**32 curated AI skills. One installer. Nine tools.**

*Stop configuring. Start shipping.*

```bash
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash
```

</div>

---

## Table of Contents

- [What are Skills?](#what-are-skills)
- [The Arsenal](#the-arsenal) — 32 skills, organized by domain
- [The Armory](#the-armory) — 9 supported tools
- [Equip Up](#equip-up) — 3 ways to install
- [Command Reference](#command-reference)
- [Update & Remove](#update--remove)
- [How It Works](#how-it-works)
- [Contributing](#contributing)

---

## What are Skills?

Skills are **structured markdown playbooks** that give your AI assistant expert-level context for a specific domain. Instead of re-explaining your stack every session, you load a skill once — and your AI already knows the patterns, tools, and decisions that matter.

Think of them as RPG loadouts. You equip a skill, and your AI levels up.

Each skill in this arsenal is battle-tested and includes:
- A `SKILL.md` — the core playbook loaded by the AI
- `references/` — domain-specific knowledge files  
- `scripts/` — ready-to-run utilities (where applicable)
- `templates/` — copy-paste starting points

> **Supported by:** Claude Code, Claude Desktop, Cursor, Codex, OpenCode, Factory, VS Code, Antigravity, and Antigravity AGY.

---

## The Arsenal

### 🤖 AI & Engineering

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `ai-ml-engineering` | ML engineering, MLOps, LLM apps, RAG pipelines, NLP, computer vision, prompt engineering | Building AI systems end-to-end |
| `software-engineering` | Backend, frontend, fullstack, APIs, systems architecture, performance, Go/Rust/and more | Any production code decision |
| `prompt-master` | Prompt engineering (CoT, ToT, ReAct), RAG pipelines, model-specific tuning for Claude & GPT | Squeezing every token of performance |
| `meeting-engineering` | Live Google Meet virtual assistants with voice — Playwright, PulseAudio, STT/LLM/TTS, Docker | Building real-time meeting bots |
| `quality-assurance` | Test strategy, automation frameworks, performance testing, API testing, QA processes | Shipping with confidence |
| `research-development` | Innovation strategy, tech scouting, R&D management, emerging tech evaluation | Staying ahead of the curve |

### 📊 Data & Analytics

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `data-analytics` | Data engineering, analysis, BI, data visualization, data science, analytics engineering | Pipelines to dashboards |

### 🎨 Design & Content

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `design-ux` | UX/UI design, design systems, user research, accessibility, prototyping | Building interfaces people actually enjoy |
| `content-communications` | Content strategy, technical writing, copywriting, developer relations | Making complex things readable |
| `marketing` | Digital marketing, content marketing, SEO, growth, brand strategy, analytics | Campaigns that convert |
| `web-presentation-creator` | Cinematic landing pages with GSAP animations, scrollytelling, video embeds, full HTML packages | Premium web experiences |
| `one-page` | One-pagers, executive summaries, status updates, business cases | When one page has to do everything |
| `legendary-readme` | README files that are both technically excellent and genuinely entertaining | First impressions that stick |

### 🔧 DevOps & Infrastructure

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `devops-infrastructure` | AWS/GCP/Azure, Kubernetes, CI/CD, Terraform, SRE, networking, database administration | Infra that doesn't page you at 3am |
| `cron-master` | Cron across local and Docker environments — Supercronic, Ofelia, host-to-container patterns | Scheduled tasks that actually run |
| `trivy-scanner` | Trivy security scanning — vulnerabilities, misconfigs, secrets, SBOM, compliance, reports | Knowing what's lurking in your images |
| `it-administration` | Endpoint management, IAM, IT security, SaaS administration, IT ops | Running the machine that runs the machines |

### 💼 Business & Operations

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `executive-leadership` | CEO strategy, CTO leadership, CFO finance, board management, fundraising, org transformation | C-suite decisions with data |
| `finance` | FP&A, financial modeling, SaaS metrics, fundraising, cash flow, investor materials | Numbers that tell the right story |
| `hr-people` | Talent acquisition, people ops, org development, compensation, employee experience | Building teams, not just orgs |
| `legal-compliance` | Corporate law, contracts, IP, GDPR/CCPA, regulatory compliance, risk management | Staying out of trouble |
| `operations` | Business ops, project management, process optimization, vendor management, excellence | The unsexy work that makes everything work |
| `product-management` | Product strategy, roadmapping, discovery, prioritization, PRDs, growth | Shipping the right thing |
| `sales` | B2B sales, sales engineering, account management, RevOps, GTM strategy | Pipeline to close |
| `customer-support` | Support ops, technical support, knowledge management, escalation workflows, CX | Support that actually helps |
| `supply-chain` | Procurement, vendor management, supply chain analytics, logistics, strategic sourcing | Getting things from A to B |

### 🔐 Security

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `security-engineering` | AppSec, cloud security, pentesting, DevSecOps, threat modeling, incident response, IAM | Secure by design, not by accident |
| `security-review` | Line-by-line code security review — OWASP, CWE, credentials, PII leaks, supply chain | The review that catches what others miss |

### 🌐 Integrations

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `gcalendar` | Bulk Google Calendar event validation, duplicate removal, timezone conversion, MCP workflows | Calendar chaos → order |
| `google-workspace-bot-integration` | Bot commands and workflows across Gmail, Calendar, Sheets, Docs, Drive, Forms, Contacts | Full Workspace automation |
| `vonage-voice` | Vonage Voice API — outbound calls, IVR, NCCO, DTMF/ASR, webhooks, call control | Programmable voice, done right |
| `tomate-pos80` | Tomate POS-80 thermal printer — raw ESC/POS commands, encoding, barcodes, receipt templates | Your AI can now print receipts |

---

## The Armory

The installer detects these tools automatically and installs skills to their config directories.

| Tool | Skills land at | Auto-detected? |
|:-----|:---------------|:---------------|
| **Claude Code** | `~/.claude/skills/` | ✓ checks `~/.claude/` |
| **Claude Desktop** | `~/Library/Application Support/Claude/skills/` (macOS)<br>`~/.config/claude/skills/` (Linux) | ✓ |
| **Codex** | `~/.codex/skills/` | ✓ checks `~/.codex/` |
| **OpenCode** | `~/.config/opencode/skills/` | ✓ |
| **Factory** | `~/.factory/skills/` | ✓ checks `~/.factory/` |
| **Cursor** | `~/.cursor/rules/` | ✓ checks `~/.cursor/` |
| **VS Code** | `~/.vscode/lzr1-skills/` | ✓ checks `~/.vscode/` |
| **Antigravity** | `~/.antigravity/skills/` | ✓ |
| **Antigravity AGY** | `~/.agy/skills/` | ✓ |

---

## Equip Up

### Option 1 — curl (recommended)

No cloning required. The installer downloads directly from GitHub.

```bash
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash
```

This launches an interactive menu — pick your tools, choose your action, done.

**Silent install to all detected tools:**

```bash
LZRI_AUTO=1 curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash
```

### Option 2 — Clone and run

Full local control. Works offline after cloning.

```bash
git clone https://github.com/victorlazari/lzr1-skills.git
cd lzr1-skills
bash install.sh
```

**Or go straight to a specific loadout:**

```bash
bash install.sh --claude-code --cursor       # just these two
bash install.sh --all                         # arm everything
bash install.sh --all --dry-run              # preview without touching anything
```

### Option 3 — Update existing install

Re-downloads the latest skills and reinstalls to whichever tools you previously selected.

```bash
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash -s -- update
```

---

## Command Reference

### Subcommands

| Command | What it does |
|:--------|:-------------|
| `install` | Install skills (default) |
| `update` | Re-download and reinstall to previously selected tools |
| `remove` | Remove installed skills |
| `doctor` | Check installation health — verifies every skill file |

### Tool Flags

| Flag | Target |
|:-----|:-------|
| `--claude-code` | `~/.claude/skills/` |
| `--claude-desktop` | Platform-specific Claude Desktop path |
| `--codex` | `~/.codex/skills/` |
| `--opencode` | `~/.config/opencode/skills/` |
| `--factory` | `~/.factory/skills/` |
| `--cursor` | `~/.cursor/rules/` |
| `--vscode` | `~/.vscode/lzr1-skills/` |
| `--antigravity` | `~/.antigravity/skills/` |
| `--agy` | `~/.agy/skills/` |
| `--all` | All nine tools |

### Behavior Flags

| Flag | What it does |
|:-----|:-------------|
| `--dry-run`, `-n` | Preview what would be installed without writing anything |
| `--verbose`, `-v` | Show per-file output |
| `--yes`, `-y` | Skip confirmation prompts |
| `--version` | Show installer version |
| `--help`, `-h` | Full help text |

### Environment Variables

| Variable | Effect |
|:---------|:-------|
| `LZRI_AUTO=1` | Skip the interactive menu, install to all detected tools automatically |

---

## Update & Remove

**Update** re-downloads the latest version of all skills and reinstalls them to whatever tools you picked last time. Your previous selection is saved to `~/.lzr1-skills-state`.

```bash
# Via curl (no clone needed)
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash -s -- update

# From a local clone
bash install.sh update
```

**Remove** deletes skill files from the target tool directories.

```bash
bash install.sh remove --claude-code    # remove from one tool
bash install.sh remove --all            # clean everything
```

**Health check:**

```bash
bash install.sh doctor
```

---

## How It Works

The installer has two modes, chosen automatically:

**Local mode** (when you clone the repo) — skills are read directly from `./skills/*/SKILL.md` and copied to target directories. No network required after cloning.

**Curl mode** (when piped from the internet) — the installer detects that no local `skills/` directory exists, fetches the skill manifest from `skills-list.txt`, then downloads each `SKILL.md` individually from GitHub raw URLs. Falls back to a hardcoded list if the manifest is unreachable.

**State file** — after each install, the selected tools are written to `~/.lzr1-skills-state`. The `update` and `remove` subcommands read this file so you don't have to re-specify your tools every time.

**Tool detection** — the installer checks for each tool's config directory at startup. Detected tools show `✓` in the interactive menu; undetected ones show `○` but can still be installed (the directory will be created).

---

## Contributing

Found a skill that belongs here? Have a better version of an existing one? PRs are open.

```bash
git clone https://github.com/victorlazari/lzr1-skills.git
cd lzr1-skills

# Add your skill under skills/<your-skill-name>/SKILL.md
# Add the name to skills-list.txt
# Send a PR
```

**Skill format** — frontmatter with `name` and `description`, followed by markdown. Reference files go in `references/`, scripts in `scripts/`, templates in `templates/`.

---

## License

MIT — use it, fork it, ship it.

---

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

<div align="center">
<sub>Built by <a href="https://github.com/victorlazari">Victor Lazari</a> · <a href="https://github.com/victorlazari/lzr1-skills/issues">Report an issue</a></sub>
</div>
