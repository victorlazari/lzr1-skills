<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=lzr1-skills&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=32&desc=84%20AI%20Skills%20%C2%B7%20Parallel%20Agent%20Edition&descAlignY=55&descSize=18" width="100%"/>

<div align="center">

[![Stars](https://img.shields.io/github/stars/victorlazari/lzr1-skills?style=flat-square&color=a855f7&labelColor=1a1a2e)](https://github.com/victorlazari/lzr1-skills/stargazers)
[![License](https://img.shields.io/badge/license-MIT-06b6d4?style=flat-square&labelColor=1a1a2e)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-84-ec4899?style=flat-square&labelColor=1a1a2e)](skills/)
[![macOS](https://img.shields.io/badge/macOS-✓-a855f7?style=flat-square&labelColor=1a1a2e)](install.sh)
[![Linux](https://img.shields.io/badge/Linux-✓-06b6d4?style=flat-square&labelColor=1a1a2e)](install.sh)
[![Made with Bash](https://img.shields.io/badge/made%20with-bash-ec4899?style=flat-square&labelColor=1a1a2e&logo=gnubash&logoColor=white)](install.sh)

**84 curated AI skills. One installer. Nine tools. Now with parallel execution.**

*Stop configuring. Start shipping — in formation.*

```bash
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash
```

</div>

---

## Table of Contents

- [What are Skills?](#what-are-skills)
- [Parallel Agent Architecture](#parallel-agent-architecture) — the June 2026 upgrade across all 84 skills
- [The Arsenal](#the-arsenal) — 84 skills, organized by domain
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

## Parallel Agent Architecture

Every skill in this arsenal ships with a **parallel execution protocol** added in June 2026. Instead of sequential analysis, skills now fan out into specialized agents that work simultaneously, then synthesize findings that no single agent could surface alone.

Three upgrade patterns cover all 84 skills:

---

### Pattern B — Sequential → Parallel Fan-out
*8 skills · highest analysis quality gain*

Skills with multiple independent analysis phases now launch all of them simultaneously. A secrets scanner doesn't wait for a data-flow tracer. An audio/transport agent doesn't wait for a transcript pipeline agent. Each gets the full context window and a clean slate — no anchoring bias from prior phases.

```
BEFORE   Phase 1 ──▶ Phase 2 ──▶ Phase 3 ──▶ Phase N ──▶ Report

AFTER    Phase 1 Agent ─┐
         Phase 2 Agent ─┤
         Phase 3 Agent ─┼──▶ Synthesis Agent ──▶ Unified Report
         Phase N Agent ─┘    (cross-references all phases for
                               interaction effects none could see alone)
```

**Affected skills:** `security-review` · `trivy-scanner` · `meeting-engineering` · `legendary-readme` · `devops-infrastructure` · `web-tester-supreme` · `oncall-master-supreme` · `ticket-supreme`

---

### Pattern C — Reference-Selector → Multi-Specialist
*22 skills · cross-domain insight*

Skills that used to pick *one* reference domain now detect *all* relevant domains and spawn a specialist per domain in parallel. A task touching Go + Postgres + REST gets a Backend Specialist, a DB Specialist, and an API Specialist running simultaneously — then a Cross-Domain Synthesizer resolves contradictions between them before you write a line of code.

```
BEFORE   Detect domain ──▶ Pick ONE reference ──▶ Work within it
         (other domains silently ignored)

AFTER    Detect all relevant domains
              ├──▶ Domain A Specialist ─┐
              ├──▶ Domain B Specialist ─┼──▶ Cross-Domain Synthesizer
              └──▶ Domain C Specialist ─┘    (surfaces contradictions
                                              before you ship them)
```

**Affected skills:** `software-engineering` · `data-analytics` · `quality-assurance` · `security-engineering` · `ai-ml-engineering` · `executive-leadership` · `finance` · `design-ux` · `product-management` · `operations` · `sales` · `marketing` · `hr-people` · `legal-compliance` · `content-communications` · `research-development` · `customer-support` · `supply-chain` · `accessibility-testing` · `it-administration` · `roles-permissions` · `ai`

---

### Pattern A — Adversarial Verification + Upgraded Synthesis
*54 skills · already spawning, now hardened*

Skills that already spawned parallel agents received three additive upgrades:

| Addition | What it does |
|:---------|:-------------|
| **3× Refuter Panel** | For each significant finding, 3 independent agents are tasked to *refute* it. A finding is confirmed only if ≥2 refuters fail to disprove it. Eliminates plausible-but-wrong output before it reaches you. |
| **Consistency Validator** | Before synthesis, one agent reviews all parallel outputs for contradictions and flags prerequisite sequencing — so you don't get two agents recommending incompatible approaches for the same component. |
| **Upgraded Synthesis** | The synthesis step now actively resolves conflicts — picks a winner, annotates the reasoning, preserves the dissent as a footnote — instead of silently concatenating results. |

**Affected skills:** all remaining 54 including `masterclaw` · `bash` · `nemoclaw` · `openclaw` · `prompt-master` · `rag` · `k8s-eks` · `otel-collector` · `manus` · and 45 more.

---

## The Arsenal

### 🤖 AI & Agents

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `ai` | Advanced AI architectures (CNNs, Transformers, LLMs), training pipelines, deployment, and production AI security | Building and deploying AI systems end-to-end |
| `ai-ml-engineering` | ML engineering, MLOps, LLM apps, RAG pipelines, NLP, computer vision, prompt engineering | ML from experimentation to production |
| `masterclaw` | OpenClaw, NemoClaw & Enterprise Prompt Engineering — multi-agent systems, distributed stream-processing, production ops & incident response | Full-lifecycle expert for the MasterClaw platform |
| `openclaw` | OpenClaw agent runtime — session management, 3-layer memory, channel workers, WhatsApp/Signal/Telegram, multi-agent orchestration | Building and operating OpenClaw deployments |
| `nemoclaw` | NemoClaw distributed engine — LSM-tree storage, Raft consensus, stream processing, active-active CRDT replication | Operating NemoClaw clusters at scale |
| `manus` | Manus AI agent framework — task automation, multi-step workflows, tool orchestration, autonomous agents | Building Manus-powered automation |
| `manus-workflows` | Manus workflow design patterns — parallel execution, state management, agent coordination, error recovery | Designing complex Manus workflow graphs |
| `hermes-agent` | Hermes agent patterns — message routing, async communication, event-driven architecture, agent-to-agent protocols | Building reliable agent communication layers |
| `meeting-engineering` | Live virtual meeting assistants with voice — Playwright automation, audio pipelines, STT/LLM/TTS, Docker | Building real-time meeting bots |
| `software-engineering` | Backend, frontend, fullstack, APIs, systems architecture, performance, Go/Rust and more | Any production code decision |
| `quality-assurance` | Test strategy, automation frameworks, performance testing, API testing, QA processes | Shipping with confidence |
| `research-development` | Innovation strategy, tech scouting, R&D management, emerging tech evaluation | Staying ahead of the curve |

### 🧠 Prompts & LLMs

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `prompt-master` | Prompt engineering (CoT, ToT, ReAct, DSPy), RAG pipelines, model-specific tuning for Claude & GPT | Squeezing every token of performance |
| `prompt` | Core prompt design, optimization, and structuring best practices | Getting cleaner, more reliable AI outputs |
| `claude` | Claude API/SDK integration — tool use, multi-turn, streaming, MCP, caching, computer use | Building Claude-powered applications |
| `openai` | OpenAI API integration — function calling, Assistants API, fine-tuning, vision | Building OpenAI-powered applications |
| `rag` | RAG architectures — chunking strategies, embedding models, retrieval patterns, reranking, evaluation | Knowledge-grounded AI applications |

### 📊 Data & Analytics

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `data-analytics` | Data engineering, analysis, BI, data visualization, data science, analytics engineering | Pipelines to dashboards |

### 🎨 Design & Content

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `design-ux` | UX/UI design, design systems, user research, accessibility, interaction design, prototyping | Building interfaces people actually enjoy |
| `content-communications` | Content strategy, technical writing, copywriting, developer relations, corporate comms | Making complex things readable |
| `marketing` | Digital marketing, SEO, growth, brand strategy, demand gen, analytics | Campaigns that convert |
| `web-presentation-creator` | Cinematic landing pages with GSAP animations, scrollytelling, video embeds, full HTML packages | Premium web experiences |
| `one-page` | One-pagers, executive summaries, status updates, business cases | When one page has to do everything |
| `legendary-readme` | README files that are both technically excellent and genuinely entertaining | First impressions that stick |
| `frontend` | React, Next.js, TypeScript, state management, server components, accessibility | Building modern frontend applications |
| `frontend-menu-design` | Navigation UX, dropdown patterns, mobile menus, mega menus, keyboard accessibility | Menus that don't frustrate people |

### 🔧 DevOps & Infrastructure

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `devops-infrastructure` | AWS/GCP/Azure, Kubernetes, CI/CD, Terraform, SRE, networking, database ops | Infra that doesn't page you at 3am |
| `devops` | CI/CD pipelines, deployment automation, GitOps, infrastructure as code | Streamlining the path from commit to production |
| `docker` | Docker containerization — images, Compose, networking, volumes, multi-arch | Containers that actually work in prod |
| `dockerfile` | Dockerfile authoring — multi-stage builds, layer optimization, hardening, best practices | Lean, secure, reproducible images |
| `k8s-eks` | Kubernetes on AWS EKS — workloads, networking, IAM, autoscaling, node groups | Running K8s without the PhD |
| `lerian-helm` | Lerian platform Helm chart engineering with strict Lerian conventions and security patterns | Lerian-compliant Helm deployments |
| `cron-master` | Cron across local and Docker environments — Supercronic, Ofelia, host-to-container patterns | Scheduled tasks that actually run |
| `trivy-scanner` | Trivy security scanning — vulnerabilities, misconfigs, secrets, SBOM, compliance, reports | Knowing what's lurking in your images |
| `it-administration` | Endpoint management, IAM, IT security, SaaS administration, IT ops | Running the machine that runs the machines |
| `otel-collector` | OpenTelemetry Collector — pipeline config, processors, exporters, sampling, Alloy | Telemetry that reaches its destination |

### 🗄️ Databases & Storage

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `database` | Database design, SQL, indexing, query optimization, migrations, normalization | Getting the schema right the first time |
| `postgres-15` | PostgreSQL 15 expert — advanced queries, partitioning, tuning, replication, logical decoding | High-performance Postgres at scale |
| `mongodb` | MongoDB — schema design, aggregation pipelines, indexing, Atlas, transactions | Document-model application data |
| `redis-valkey` | Redis/Valkey — data structures, caching, pub/sub, Lua scripting, Sentinel, clustering | Fast data that lives at the edge of your stack |
| `valkey-redis` | Valkey/Redis open-source fork patterns — migration, compatibility, extended commands | Moving from Redis to Valkey |
| `rabbitmq` | RabbitMQ — exchanges, queues, routing, dead letters, shovel, clustering | Reliable async message delivery |
| `rabbitmq-documentdb` | RabbitMQ + DocumentDB integration — event-sourcing patterns, consumer groups, idempotency | Message-driven document persistence |
| `sql-partitioning` | PostgreSQL table partitioning — range, list, hash, declarative, constraint exclusion | Tables that don't grind to a halt at 100M rows |
| `seaweedfs` | SeaweedFS distributed storage — volumes, topology, S3 API, tiered storage, erasure coding | Cheap, scalable blob storage on your own infra |

### 🔐 Security

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `security-engineering` | AppSec, cloud security, DevSecOps, threat modeling, incident response, IAM | Secure by design, not by accident |
| `security-review` | Exhaustive line-by-line code security review — OWASP, CWE, credentials, PII leaks, supply chain | The review that catches what others miss |
| `passkeys` | WebAuthn/Passkey implementation — FIDO2, authenticator types, credential management, UX | Passwordless auth that actually ships |
| `roles-permissions` | RBAC/ABAC/ReBAC with Casbin, Casdoor, multi-tenant authorization, IDOR prevention | Authorization models that don't explode in production |

### 💻 Languages & Runtimes

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `bash` | Advanced Bash/shell scripting, text processing, POSIX compliance, process management | Automation scripts that survive the next developer |
| `go` | Go expert — concurrency patterns, stdlib, testing, performance, idiomatic Go | Writing Go that senior Go engineers won't rewrite |
| `lua` | Lua scripting — embedding, coroutines, metatables, OOP patterns, Luarocks | Lightweight, embeddable scripting |
| `go-lua` | Go + Lua integration — embedding scripts, sandboxing, extension systems, gopher-lua | Building scriptable Go applications |
| `speedtest` | Network speed testing, latency measurement, bandwidth diagnostics, jitter analysis | Understanding what your network is actually doing |

### 💼 Business & Operations

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `executive-leadership` | CEO/CTO/CFO strategy, board management, fundraising, org transformation | C-suite decisions with data |
| `finance` | FP&A, financial modeling, SaaS metrics, fundraising, cash flow, investor materials | Numbers that tell the right story |
| `hr-people` | Talent acquisition, people ops, org development, compensation, employee experience | Building teams, not just orgs |
| `legal-compliance` | Corporate law, contracts, IP, GDPR/CCPA, regulatory compliance, risk management | Staying out of trouble |
| `operations` | Business ops, project management, process optimization, vendor management, excellence | The unsexy work that makes everything work |
| `product-management` | Product strategy, roadmapping, discovery, prioritization, PRDs, growth | Shipping the right thing |
| `sales` | B2B sales, sales engineering, account management, RevOps, GTM strategy | Pipeline to close |
| `customer-support` | Support ops, technical support, knowledge management, escalation workflows, CX | Support that actually helps |
| `supply-chain` | Procurement, vendor management, supply chain analytics, logistics, strategic sourcing | Getting things from A to B |
| `accessibility-testing` | WCAG 2.1 AA, ARIA, keyboard navigation, screen reader compatibility, remediation | Accessible by default, not by lawsuit |

### 🎯 Support, Ticketing & On-call

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `jira-field-schemas` | Jira custom field configuration, schemas, screen layouts, field contexts | Jira that works the way your team thinks |
| `jira-jsm-oncall` | Jira Service Management on-call setup — schedules, escalations, SLA policies | On-call that respects sleep schedules |
| `jira-status-workflows` | Jira workflow design — status transitions, validators, post-functions, automation | Workflows people actually follow |
| `ticket-reports` | Advanced ticket reporting, JQL queries, BI integration, predictive analytics, executive dashboards | Ticket data that drives decisions |
| `ticket-supreme` | Ticket specification and sprint-ready acceptance criteria — scope, estimation, risk, dependencies | Tickets that don't come back as surprises |
| `oncall-master-supreme` | Incident management, on-call runbooks, blast radius analysis, postmortems | Incidents resolved, not just closed |
| `tech-support-ops` | Technical support operations — tooling, escalation paths, SLA management, knowledge workflows | Support at scale without chaos |

### 🌐 Integrations & APIs

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `gcalendar` | Bulk Google Calendar event validation, duplicate removal, timezone conversion, MCP workflows | Calendar chaos → order |
| `google-workspace-bot-integration` | Bot commands and workflows across Gmail, Calendar, Sheets, Docs, Drive, Forms, Contacts | Full Workspace automation |
| `slack` | Slack bot development — Block Kit, webhooks, Bolt framework, slash commands, modals | Slack bots that don't feel like bots |
| `vonage-voice` | Vonage Voice API — outbound calls, IVR, NCCO, DTMF/ASR, webhooks, call control | Programmable voice, done right |
| `voip-oncall` | VoIP-based on-call systems — SIP, call routing, escalation trees, failover | On-call that reaches a human |
| `wikijs` | Wiki.js knowledge management — pages, navigation, API, permissions, theming | Company knowledge that people actually find |
| `playwright` | Playwright automation — browser testing, E2E workflows, scraping, network interception | Tests that survive a redesign |
| `vitest` | Vitest unit testing — fast, ESM-native, coverage, mocking, snapshot testing | Unit tests that run before you lose patience |
| `tomate-pos80` | Tomate POS-80 thermal printer — raw ESC/POS commands, encoding, barcodes, receipt templates | Your AI can now print receipts |
| `bot` | Bot development patterns — webhooks, state machines, conversational flows, NLP integration | Bots that have a real conversation |

### 🧪 Testing & Quality

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `web-tester-supreme` | Comprehensive web testing — functional, visual regression, a11y, performance, client-side security | The test suite that catches everything |

### 🌍 Language Teaching

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `french-teacher` | French language instruction — grammar, vocabulary, conversation, DELF/DALF preparation | Learning French with a patient, knowledgeable teacher |
| `spanish-teacher` | Spanish language instruction — grammar, vocabulary, conversation, DELE preparation | Learning Spanish without the textbook grind |

---

## The Armory

The installer detects these tools automatically and installs skills to their config directories.

| Tool | Skills land at | Auto-detected? |
|:-----|:---------------|:---------------|
| **Claude Code** | `~/.claude/skills/` | ✓ checks `~/.claude/` |
| **Claude Desktop** | `~/Library/Application Support/Claude/skills/` (macOS)<br>`~/.config/claude/skills/` (Linux) | ✓ |
| **Codex** | `~/.codex/skills/` | ✓ checks `~/.codex/` |
| **OpenCode** | `~/.config/opencode/skill/` | ✓ |
| **Factory** | `~/.factory/skills/` | ✓ checks `~/.factory/` |
| **Cursor** | `~/.cursor/rules/` | ✓ checks `~/.cursor/` |
| **VS Code** | `~/.vscode/lzr1-skills/` | ✓ checks `~/.vscode/` |
| **Antigravity** | `~/.antigravity-ide/rules/` | ✓ checks `~/.antigravity-ide/` |
| **Antigravity AGY** | `~/.gemini/antigravity-cli/skills/` | ✓ checks `~/.gemini/antigravity-cli/` |

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

**Parallel protocols** — new skills should include a `## Parallel Execution Protocol`, `## Multi-Specialist Protocol`, or `## Adversarial Verification Panel` section depending on the skill's workflow shape. See any existing skill for the pattern that fits.

---

## License

MIT — use it, fork it, ship it.

---

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

<div align="center">
<sub>Built by <a href="https://github.com/victorlazari">Victor Lazari</a> · <a href="https://github.com/victorlazari/lzr1-skills/issues">Report an issue</a></sub>
</div>
