<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=lzr1-skills&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=32&desc=86%20AI%20Skills%20%C2%B7%20Parallel%20Agent%20Edition&descAlignY=55&descSize=18" width="100%"/>

<div align="center">

[![Stars](https://img.shields.io/github/stars/victorlazari/lzr1-skills?style=flat-square&color=a855f7&labelColor=1a1a2e)](https://github.com/victorlazari/lzr1-skills)
[![License](https://img.shields.io/badge/license-MIT-06b6d4?style=flat-square&labelColor=1a1a2e)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-86-ec4899?style=flat-square&labelColor=1a1a2e)](skills/)
[![CI](https://github.com/victorlazari/lzr1-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/victorlazari/lzr1-skills/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/victorlazari/lzr1-skills?style=flat-square&color=a855f7&labelColor=1a1a2e)](https://github.com/victorlazari/lzr1-skills/releases/latest)
[![macOS](https://img.shields.io/badge/macOS-✓-a855f7?style=flat-square&labelColor=1a1a2e)](install.sh)
[![Linux](https://img.shields.io/badge/Linux-✓-06b6d4?style=flat-square&labelColor=1a1a2e)](install.sh)
[![Made with Bash](https://img.shields.io/badge/made%20with-bash-ec4899?style=flat-square&labelColor=1a1a2e&logo=gnubash&logoColor=white)](install.sh)

**86 curated AI skills. One installer. Nine tools. Complete packages, not entrypoints alone.**

*Stop configuring. Start shipping — in formation.*

```bash
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash
```

</div>

---

## Table of Contents

- [What are Skills?](#what-are-skills)
- [Parallel Agent Architecture](#parallel-agent-architecture) — three multi-agent patterns, counted from the skills
- [The Arsenal](#the-arsenal) — 86 skills, organized by domain
- [Choosing between overlapping skills](#choosing-between-overlapping-skills)
- [The Armory](#the-armory) — 9 supported tools
- [Equip Up](#equip-up) — 3 ways to install
- [Command Reference](#command-reference)
- [Update & Remove](#update--remove)
- [How It Works](#how-it-works)
- [Development](#development)
- [Scope](#scope)
- [Contributing](#contributing)
- [License](#license)

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

Some skills describe an optional multi-agent execution protocol: independent work is split across sub-agents, then merged by a synthesis step. The numbers below are counted from the `SKILL.md` and `references/` files in this repository (a skill is listed when its text contains the named mechanism), not from a design document. The remaining skills are single-agent playbooks, and `coderabbit-reviewer`, `yaml-specialist` and `security-review` deliberately use bounded, evidence-first workflows where ordered verification is safer than concurrency.

---

### Pattern B — Parallel Execution Protocol
*2 skills · all agents launch at once*

`devops-infrastructure` and `legendary-readme` define a **Parallel Execution Protocol**: when several independent domains are involved, every relevant agent launches at the same time, each with the full task context and its own reference file, and a synthesis step merges the results.

```
BEFORE   Phase 1 ──▶ Phase 2 ──▶ Phase 3 ──▶ Phase N ──▶ Report

AFTER    Phase 1 Agent ─┐
         Phase 2 Agent ─┤
         Phase 3 Agent ─┼──▶ Synthesis Agent ──▶ Unified Report
         Phase N Agent ─┘
```

Other skills (for example `security-review`, `trivy-scanner`, `web-tester-supreme`, `ticket-supreme`, `oncall-master-supreme`) allow **conditional, bounded** parallel work only when branches are independent; they do not implement a launch-everything protocol.

**Affected skills:** `devops-infrastructure` · `legendary-readme`

---

### Pattern C — Multi-Specialist Spawning
*16 skills · cross-domain insight*

These skills detect every relevant domain and spawn a specialist per domain, then a **Cross-Domain Synthesizer** merges the specialists' outputs and flags contradictions between them. A task touching Go + Postgres + REST gets a Backend Specialist, a DB Specialist and an API Specialist instead of one reference.

```
BEFORE   Detect domain ──▶ Pick ONE reference ──▶ Work within it
         (other domains silently ignored)

AFTER    Detect all relevant domains
              ├──▶ Domain A Specialist ─┐
              ├──▶ Domain B Specialist ─┼──▶ Cross-Domain Synthesizer
              └──▶ Domain C Specialist ─┘    (surfaces contradictions)
```

**Affected skills:** `ai` · `content-communications` · `customer-support` · `data-analytics` · `design-ux` · `executive-leadership` · `finance` · `legal-compliance` · `marketing` · `product-management` · `quality-assurance` · `research-development` · `roles-permissions` · `sales` · `software-engineering` · `supply-chain`

---

### Pattern A — Adversarial Verification
*18 skills with a refuter panel · 20 with a consistency validator · 15 with conflict-resolving synthesis*

Skills that spawn parallel sub-agents add up to three verification steps. The counts differ because not every skill carries every step.

| Mechanism | Skills | What it does |
|:----------|:------:|:-------------|
| **3× Refuter Panel** | 18 | For each significant finding, 3 independent agents try to *refute* it. A finding is confirmed only if at least 2 refuters fail to disprove it, and a contested finding keeps the dissent. |
| **Consistency Validator** | 20 | Before synthesis, one agent reviews all parallel outputs for contradictions and missing prerequisites. |
| **Conflict-resolving synthesis** | 15 | The synthesis step resolves contradictions, orders the plan by prerequisites and calibrates confidence instead of concatenating results. |

**Affected skills:** `bot` · `claude` · `devops` · `frontend-menu-design` · `go` · `k8s-eks` · `mongodb` · `otel-collector` · `playwright` · `prompt` · `prompt-master` · `rabbitmq-documentdb` · `rag` · `redis-valkey` · `sql-partitioning` · `tech-support-ops` · `ticket-reports` · `vitest`

The skills above carry the refuter panel. The consistency validator is additionally present in `seaweedfs` and `speedtest`.

---

## The Arsenal

### 🤖 AI & Agents

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `ai` | AI model design, training, deployment and troubleshooting: CNNs, RNNs, Transformers, LLMs, inference configuration, AI security audits | Building and running AI systems end to end |
| `ai-ml-engineering` | ML engineering, MLOps, LLM applications, NLP, computer vision, RAG pipelines and fine-tuning | ML from experiment to production |
| `masterclaw` | Combined OpenClaw gateway, NemoClaw engine and prompt-architecture playbook for tasks that span more than one, or whose runtime is unknown | Cross-runtime claw work |
| `openclaw` | Deploy, configure and troubleshoot the OpenClaw (Node.js) and ZeroClaw (Rust) agent runtimes: workspace bootstrap files, config.toml, channel failures | Operating OpenClaw or ZeroClaw |
| `nemoclaw` | NVIDIA NemoClaw deployment on DGX, WSL or Linux/macOS, guided onboarding, inference provider setup, credential handling | Operating NemoClaw |
| `bot` | Build and secure bots on the OpenClaw, NemoClaw and OpenShell ecosystems: plugins, memory, sandboxes, multi-agent routing, security audits | Bots and agents on the claw runtimes |
| `manus` | Manus v2 agent platform: agent pipelines and clusters, sandbox network policies, WebMCP browser automation, Control Plane scheduling, S3 multipart uploads | Building and operating Manus agent solutions |
| `hermes-agent` | NousResearch Hermes Agent: install and update, providers and models, tools, memory and skills, cron, gateways, MCP/ACP/API integrations, plugins, production readiness | Operating and extending Hermes Agent |
| `meeting-engineering` | Live Google Meet assistants: Playwright, PulseAudio and Xvfb audio routing, low-latency STT/LLM/TTS pipelines | Real-time meeting bots |
| `coderabbit-reviewer` | Local CodeRabbit CLI reviews of Git changes with `--agent` event evidence, finding triage and bounded remediation | Pre-push review of local changes |
| `research-development` | Innovation strategy, technical research methodology, R&D management, technology scouting, emerging technology evaluation | Evaluating what to build or adopt next |

### 🧠 Prompts & LLMs

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `prompt` | Design, harden and debug prompts and prompt systems: architecture, injection and jailbreak defence, token and cache optimization, schemas, templates | One prompt system that must work and stay safe |
| `prompt-master` | Prompting techniques (CoT, ToT, ReAct, self-consistency), RAG, GraphRAG and Agentic RAG pipelines, context and bootstrap size reduction | Choosing a technique or cutting context size |
| `claude` | Claude models and API: integration, system prompts, tool use, vision, extended thinking, prompt caching, Artifacts | Apps built on Claude |
| `openai` | OpenAI API: Responses API, Realtime API, function calling, structured outputs, tool_search | Apps built on OpenAI models |
| `rag` | RAG architecture: adaptive and agentic RAG, chunking, embeddings, vector databases, hybrid retrieval, fixing irrelevant retrieval | Grounded retrieval pipelines |

### 📊 Data & Analytics

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `data-analytics` | Data engineering, analysis, BI, visualization, data science, warehouse design, SQL and analytics engineering | Pipelines to dashboards |

### 🎨 Design & Content

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `design-ux` | UX and UI design, design systems, user research, accessibility, interaction design, information architecture | Interfaces people can use |
| `content-communications` | Content strategy, technical writing, copywriting, corporate communications, developer relations | Making complex things readable |
| `marketing` | Digital and content marketing, SEO, growth, brand strategy, marketing analytics, demand generation | Campaigns and positioning |
| `one-page` | One-page presentations and reports: executive summaries, status updates, business cases, pitches, launches | One page that has to do everything |
| `legendary-readme` | GitHub README writing and polish: banners, badges, diagrams, tables, tone, light and dark mode | Project front pages |

### 🖥️ Frontend & Web

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `frontend` | React and Next.js App Router frontends: Server Components, TypeScript, Tailwind CSS, state management, testing, rendering and bundle performance | Building and auditing modern frontends |
| `frontend-menu-design` | Navigation menu architecture: mega menus, mobile drawers, RBAC-driven visibility, animation, keyboard and WCAG behavior in React and Next.js | Menus that are usable and accessible |
| `web-presentation-creator` | Premium landing pages: cinematic scrollytelling, GSAP animation, complex media, complete HTML or ZIP packages | Showcase web pages |

### 🔧 DevOps & Infrastructure

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `devops-infrastructure` | Cross-cloud architecture, Infrastructure as Code, SRE, platform engineering, networking, AI/MLOps infrastructure, FinOps | Infrastructure design decisions |
| `devops` | Hands-on AWS, EKS, Helm, GitOps, VPC and CI/CD provisioning and troubleshooting, including Terraform and CloudFormation | Provisioning and debugging AWS delivery |
| `docker` | Run and operate containers and Compose: Buildx multi-platform builds, runtime hardening, Docker Scout, networking, storage and performance troubleshooting | Containers that run and stay healthy |
| `dockerfile` | Author and optimize Dockerfiles: multi-stage builds, layer caching, BuildKit mounts, non-root and secret handling, Hadolint and Trivy in CI | Lean, safe images |
| `k8s-eks` | Kubernetes and AWS EKS operations, incident troubleshooting, networking and cluster management | EKS incidents and cluster work |
| `lerian-helm` | Helm deployments, golang-migrate migrations and security validation for Lerian Studio charts under Restricted Pod Security Standards | Deploying Lerian Studio |
| `yaml-specialist` | YAML, JSON Schema, Helm values contracts and Kubernetes manifest authoring, linting, rendering and validation | Config files that validate |
| `cron-master` | Cron scheduling locally and in Docker: crontab, Supercronic, Ofelia, host-to-container execution | Scheduled jobs that run |
| `trivy-scanner` | Trivy scans of repositories, filesystems, images, Kubernetes and SBOMs: vulnerabilities, misconfigurations, secrets, licenses, VEX, CI, air-gapped use | Knowing what ships in your images |
| `otel-collector` | OpenTelemetry Collector configuration, OTTL, scaling, connectors (routing, spanmetrics), custom builds, OOM diagnosis | Telemetry pipelines |
| `it-administration` | Endpoint management, identity and access management, IT security, SaaS administration, IT operations | Running company IT |
| `speedtest` | Ookla Speedtest methodology and CLI, custom OoklaServer, latency and jitter analysis, network throughput troubleshooting | Network performance diagnosis |

### 🗄️ Databases & Storage

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `database` | Engine-agnostic architecture, indexing, replication, high availability and security hardening for PostgreSQL and MongoDB | Choosing and designing the data layer |
| `postgres-15` | PostgreSQL 15+ operations: autovacuum, memory, PgBouncer, locks, major upgrades, PITR and DR, RBAC, RLS, pgaudit | Running Postgres in production |
| `sql-partitioning` | Partitioning and sharding for very large SQL tables: declarative partitioning, pruning, pg_partman, zero-downtime migration | Tables too big for one heap |
| `mongodb` | MongoDB operations at scale: query optimization, sharding, backup and restore, log analysis | Running MongoDB |
| `redis-valkey` | Operate Redis or Valkey in production: latency, memory pressure, hot keys, CLI incident response, cluster operations, Lua script review | Slow or full Redis/Valkey |
| `valkey-redis` | Valkey administration: valkey.conf, hardening, Redis OSS 7.2 or earlier to Valkey migration | Configuring or migrating to Valkey |
| `rabbitmq` | RabbitMQ 4.x operations and topology design, with Quorum Queues and Streams: alarms, partitions, backlogs, dead letters, tuning | Reliable messaging |
| `rabbitmq-documentdb` | RabbitMQ with Amazon DocumentDB: event-driven service design, exchange and queue setup, schemas, indexes, CDC sync | Message-driven document persistence |
| `seaweedfs` | SeaweedFS: Master, Volume and Filer servers, Kubernetes operator and CSI driver, erasure coding, tiered storage, S3 API | Self-hosted blob storage |

### 🔐 Security

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `security-engineering` | Application and cloud security, DevSecOps, security architecture, threat modeling, compliance, incident response | Designing security in |
| `security-review` | Evidence-backed security reviews of code, config, CI/CD, dependencies, infrastructure, mobile and AI integrations, with validated findings | Deep repository audits |
| `passkeys` | FIDO2 and WebAuthn passkeys: registration, authentication, recovery, Conditional UI, synced versus device-bound credentials, IdP/SSO integration | Passwordless login |
| `roles-permissions` | Authorization with Casbin and Casdoor: RBAC, ABAC, ReBAC, multi-tenant isolation, IDOR and privilege-escalation prevention | Permission models |

### 💻 Languages & Runtimes

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `software-engineering` | Backend, frontend, fullstack, mobile, API design, systems architecture, database and performance engineering, language-specific expertise | General production code decisions |
| `bash` | Bash and shell scripting, text processing, process management, POSIX compliance | Scripts that survive |
| `go` | Go troubleshooting and scaling: performance, memory and goroutine leaks, govulncheck security audits, modernization | Fixing and hardening Go |
| `lua` | Lua for embedded systems, game engines and Redis: syntax validation, C API embedding, sandboxing | Writing and securing Lua |
| `go-lua` | Go and Lua operations: pprof profiling, GOGC/GOMEMLIMIT tuning, goroutine leaks, CGO, Redis Lua scripts, migrations | Go performance work with Lua in the mix |

### 💼 Business & Operations

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `executive-leadership` | CEO, CTO, CFO, COO, VP Engineering and Chief of Staff strategy: board management, fundraising, organizational transformation | Executive decisions |
| `finance` | FP&A, accounting, treasury, financial modeling, SaaS metrics, fundraising, investor materials | Financial planning |
| `hr-people` | Talent acquisition, people operations, organizational development, compensation and benefits, employee experience, HR analytics | People programs |
| `legal-compliance` | Corporate law, contracts, IP, GDPR/CCPA data privacy, regulatory compliance, risk management | Legal and compliance groundwork |
| `operations` | Business operations, project management, process optimization, vendor management, operational excellence | Running the business |
| `product-management` | Product strategy, roadmapping, discovery, prioritization, PRDs, growth, technical product management | Deciding what to build |
| `sales` | B2B sales, sales engineering, account management, revenue operations, go-to-market | Pipeline to close |
| `supply-chain` | Procurement, vendor management, supply chain analytics, logistics, inventory, strategic sourcing | Sourcing and logistics |

### 🎯 Support, Ticketing & On-call

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `customer-support` | Support operations, technical support, knowledge management, support metrics, escalation workflows, customer experience | Support processes |
| `tech-support-ops` | Sev-1/Sev-2 triage, root cause analysis, blameless post-mortems, SLO/SLI and error-budget tracking, MTTA/MTTR | Critical incident handling |
| `oncall-master-supreme` | On-call systems: HA/DR, ChatOps war rooms, runbooks and auto-remediation, SLOs, follow-the-sun schedules, postmortems | Running on-call |
| `jira-field-schemas` | Jira field schemes, field contexts and screen schemes, with checks against the skill's recorded 2026 limits | Jira field architecture |
| `jira-jsm-oncall` | Jira Service Management SLAs, alert routing, on-call schedules, Edge Connector, CMDB-linked incident workflows, automation rules | JSM alerting and on-call |
| `jira-status-workflows` | Jira workflow state machines: transitions, conditions, validators, post-functions, workflow properties, ScriptRunner | Jira workflows |
| `ticket-reports` | Ticket reporting: JQL, SLA and team-performance dashboards, BI loading, predictive analytics, ITIL 4 measurement | Ticket data that informs |
| `ticket-supreme` | Design and build enterprise ticketing systems: high availability, real-time communication, SLA modeling, security, omnichannel, AI/ML | Building a ticketing system |

### 🌐 Integrations & APIs

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `gcalendar` | Google Calendar via MCP tools: bulk validation, duplicate removal, timezone conversion, scheduling | Calendar cleanup |
| `google-workspace-bot-integration` | Bot commands and workflows across Gmail, Calendar, Sheets, Slides, Docs, Drive, Forms, Contacts, Tasks, Chat and Events | Workspace bots |
| `slack` | Slack apps with Bolt or Deno, Block Kit messages, events, slash commands, OAuth, Web API and CLI | Slack apps |
| `vonage-voice` | Vonage Voice API: outbound calls, NCCO actions, IVR, DTMF/ASR input, answer and event webhooks, REST call control | Programmable voice |
| `voip-oncall` | VoIP on-call services: IVR incident acknowledgment, WebRTC war rooms, voice alerting with Twilio or Vonage, SIP trunks, telecom compliance | Voice-based on-call |
| `wikijs` | Wiki.js administration: Git sync, GraphQL content automation, enterprise deployments | Wiki administration |
| `manus-workflows` | n8n workflow design on its AI agent architecture: scheduling, file handling, messaging patterns, retries and recovery | n8n automations |
| `tomate-pos80` | Tomate POS-80 thermal receipt printer (MDK-080, MDK-081, MDK-08260): raw print commands, encoding, barcodes and QR codes, receipt templates | Printing receipts |

### 🧪 Testing & Quality

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `quality-assurance` | Test strategy, test plans, automation frameworks, performance and security testing, AI testing, QA processes | Planning how to test |
| `playwright` | Playwright E2E: configuration, network mocking, visual regression, multi-browser and mobile matrices, CI, flaky tests | Playwright suites |
| `vitest` | Vitest 4.1 for Next.js 16 and React 19: mocking (Prisma, Valkey, RabbitMQ), snapshots, test tags, component and hook tests | Unit tests |
| `web-tester-supreme` | Web E2E for Next.js apps: RBAC validation, degraded-state and network-failure behavior, data visualization and observability checks | App-level web test suites |
| `accessibility-testing` | Automated accessibility testing with Axe-core and Playwright: WCAG violations, known-issue snapshots, focus, dynamic trees, contrast | Accessibility checks |

### 🌍 Language Teaching

| Skill | What it does | Best for |
|:------|:-------------|:---------|
| `french-teacher` | French CEFR level assessment, targeted A1-C2 exercises and reading passages, alignment with Council of Europe descriptors | Teaching French |
| `spanish-teacher` | Spanish A1-C2: grammar, vocabulary, exercises and quizzes, dialects, cultural competence, curriculum design | Teaching Spanish |

---

## Choosing between overlapping skills

Six groups of skills sit close together. Each skill's own description names its neighbour for the other case; this table is the short version.

| Group | Lanes |
|:------|:------|
| Redis and Valkey | `redis-valkey`: a running instance is slow, out of memory, CPU-bound, has hot keys, or a Lua script needs review. `valkey-redis`: writing or hardening the Valkey config file, or migrating from Redis OSS 7.2 or earlier. |
| DevOps | `devops`: hands-on AWS networking, EKS, Helm, GitOps or CI/CD provisioning and debugging. `devops-infrastructure`: cross-cloud architecture, IaC practice, SRE, platform engineering, FinOps. |
| Prompts | `prompt`: designing, securing or debugging one prompt system. `prompt-master`: choosing a prompting technique, building RAG pipelines, cutting context size. |
| Claw runtimes | `openclaw`: deploy or troubleshoot OpenClaw or ZeroClaw. `nemoclaw`: deploy and onboard NVIDIA NemoClaw. `bot`: build or audit bots, plugins and OpenShell sandboxes on top of them. `masterclaw`: the task spans more than one runtime, or the runtime is not yet known. |
| PostgreSQL and data design | `postgres-15`: operate, tune, upgrade or secure a PostgreSQL 15+ server. `sql-partitioning`: partition or shard very large tables. `database`: engine-agnostic architecture, replication and security across PostgreSQL and MongoDB. |
| Containers | `docker`: run, debug or harden containers and Compose stacks. `dockerfile`: write, shrink or audit a Dockerfile. |

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

### Option 1 — one-line curl installer

```bash
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash
```

This installs the **latest verified release**: the script downloads the release archive `lzr1-skills.tar.gz` and `SHA256SUMS`, checks the archive against the checksum, and only then extracts it. It falls back to the **unverified `main` snapshot only when no release exists** (it prints a warning when that happens). The command launches an interactive target menu; like every `curl | bash` pattern it executes the fetched script immediately, so use the inspect-first alternative below when your trust policy requires review.

**Pin a release** (checksum-verified; fails instead of falling back if the tag or its checksums cannot be downloaded):

```bash
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash -s -- --ref v2.1.0 --codex --yes
```

**Explicit unverified snapshot** (any ref that is not a `vX.Y.Z` tag is a branch snapshot, installed without checksum verification and with a warning):

```bash
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash -s -- --ref main --detected --yes
```

**Inspect first, then run the exact saved file:**

```bash
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh -o install.sh
less install.sh
bash install.sh --detected --dry-run
bash install.sh --detected --yes
```

**Non-interactive install to detected tools:**

```bash
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash -s -- --detected --yes
```

**Verify a release by hand** (the installer does the same comparison):

```bash
curl -fsSLO https://github.com/victorlazari/lzr1-skills/releases/latest/download/lzr1-skills.tar.gz
curl -fsSLO https://github.com/victorlazari/lzr1-skills/releases/latest/download/SHA256SUMS
shasum -a 256 -c SHA256SUMS
```

**Trust model.** The checksum protects against corruption in transit and against a mirror or proxy substituting the archive. It does not protect against a compromised repository or release: both assets come from the same place, and releases are not signed yet. Report integrity problems as described in [SECURITY.md](SECURITY.md).

### Option 2 — Clone and run

Full local control. Works offline after cloning; the clone is the source, so `--ref` does not apply.

```bash
git clone https://github.com/victorlazari/lzr1-skills.git
cd lzr1-skills
bash install.sh
```

**Or go straight to a specific loadout:**

```bash
bash install.sh --claude-code --cursor --yes  # just these two
bash install.sh --all --yes                    # all nine targets, even if undetected
bash install.sh --all --dry-run                # validate and preview without writing
```

### Option 3 — Update existing install

Revalidates the latest source and reinstalls complete packages to whichever tools are recorded in the managed state file.

```bash
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash -s -- update
```

Installer version: 2.1.0

---

## Command Reference

Generated from `bash install.sh --help`; run it for the authoritative text.

```text
bash install.sh [command] [target options] [behavior options]
```

### Subcommands

| Command | What it does |
|:--------|:-------------|
| `install` | Install the complete skill catalog (default) |
| `update` | Reinstall to explicitly selected or previously saved targets |
| `remove` | Remove only content carrying lzr1 ownership markers |
| `doctor` | Validate the source catalog and report managed target coverage and the source mode, ref and verification status |
| `help` | Show the help text |

### Tool Flags

| Flag | Target |
|:-----|:-------|
| `--claude-code` | `~/.claude/skills/` |
| `--claude-desktop` | Platform-specific Claude Desktop skills directory |
| `--codex` | `~/.codex/skills/` |
| `--opencode` | `~/.config/opencode/skill/` |
| `--factory` | `~/.factory/skills/` |
| `--cursor` | `~/.cursor/rules/` |
| `--vscode` | `~/.vscode/lzr1-skills/` |
| `--antigravity` | `~/.antigravity-ide/rules/` |
| `--agy` | `~/.gemini/antigravity-cli/skills/` |
| `--detected` | Select all currently detected tools |
| `--all` | Select all nine tools, including undetected tools |

### Behavior Flags

| Flag | What it does |
|:-----|:-------------|
| `--dry-run`, `-n` | Validate the source and preview destination changes only |
| `--verbose`, `-v` | Show per-skill activity |
| `--yes`, `-y` | Non-interactive confirmation mode; does not select targets |
| `--force` | Back up and replace unowned name collisions |
| `--ref <value>` | Archive source when run via curl (env: `LZR1_REF`). Default: latest published release, checksum-verified. A tag such as `v2.1.0` pins a verified release. Any other value is a branch snapshot (unverified). Allowed characters: `A-Z a-z 0-9 . _ / -`; an empty value is rejected |
| `--version` | Show installer version |
| `--help`, `-h` | Show the help text |

### Environment Variables

| Variable | Effect |
|:---------|:-------|
| `LZR1_AUTO=1` | Automation shorthand: select detected tools without the interactive menu |
| `LZRI_AUTO=1` | Backward-compatible alias for `LZR1_AUTO` |
| `LZR1_REF` | Same as `--ref`; the flag wins when both are given |
| `LZR1_SOURCE_DIR` | Install from this local directory instead of a clone or download (source mode `override`) |

---

## Update & Remove

**Update** validates a fresh source snapshot and reinstalls all 86 complete packages to the targets recorded in `~/.lzr1-skills-state`. Explicit target flags update only those targets while preserving the other recorded selections.

```bash
# Via curl (no clone needed)
curl -fsSL https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/install.sh | bash -s -- update

# From a local clone
bash install.sh update
```

**Remove** deletes only packages that carry this repository’s ownership markers. Same-name files or directories without those markers are left untouched.

```bash
bash install.sh remove --claude-code --yes  # remove one managed target
bash install.sh remove --all --yes           # remove managed content from all targets
```

If installation finds an unowned same-name path, it fails before writing that target. `--force` is explicit opt-in: the existing content is moved under that target’s `.lzr1-backups/<run-id>/` directory before replacement.

**Health check:**

```bash
bash install.sh doctor
```

---

## How It Works

The installer chooses its source mode and then applies the same fail-closed catalog validation in every mode. The success line reads `Validated N skills from <mode> source (ref: X), verified: yes|no`, and `doctor` reports `Source: <mode>, ref <r>, verified <yes|no>`.

**Source modes** — `override` (`LZR1_SOURCE_DIR`), `local` (running from a clone), `release` (checksum-verified release archive) and `branch` (unverified snapshot of a ref).

**Manifest validation** — the source is accepted only when `skills-list.txt` is bytewise sorted, contains exactly 86 unique safe names, and exactly matches `skills/*/SKILL.md`. Every complete package directory is copied, so bundled references, scripts, templates, tests, and fixtures remain available. Unsafe archive paths and symbolic links are rejected. There is no hardcoded-list fallback.

**Checksum verification and fallback** — with no `--ref`, the installer downloads `SHA256SUMS` and `lzr1-skills.tar.gz` from the latest release and refuses to extract on a mismatch. If no `SHA256SUMS` can be downloaded it falls back to the unverified `main` snapshot with a warning. An explicit `vX.Y.Z` tag never falls back: a missing release exits non-zero. Any other ref is an unverified snapshot, with a warning. A missing `sha256sum`/`shasum` tool is an error for verified modes.

**Destination layouts** — package-native tools receive `skills/<name>/` directories. Flat-rule tools receive `<name>.md` plus a hidden `.lzr1-skill-resources/<name>/` package mirror; entrypoint links are rewritten to that mirror so referenced materials continue to resolve.

**Ownership markers and backups** — each installed package carries a `.lzr1-managed` ownership marker, and each target has a managed index. Updates stage a complete replacement before swapping it into place. Unowned collisions fail closed unless `--force` is explicit, in which case the prior content is moved to `.lzr1-backups/<run-id>/` inside that target rather than deleted.

**State and locking** — successful target selections are merged into the state file `~/.lzr1-skills-state`; subset removals delete only those records. A per-user lock directory, `~/.lzr1-skills-lock`, prevents overlapping write operations. `--dry-run` performs source validation and target preflight without writing installer state or target content.

**Tool detection** — the installer checks each tool's current config directory at startup. Detected tools are labeled in the interactive menu; undetected targets can still be selected explicitly and their directories will be created safely.

---

## Development

Run everything from the repository root. Python tooling runs isolated with `-I`.

```bash
python3 -I scripts/lint_catalog.py    # catalog linter: manifest, frontmatter, links, counts, stale refs, script registry
bash tests/test-catalog.sh            # negative fixtures for the linter
bash tests/test-scripts.sh            # smoke tests for the scripts registered in tests/script-coverage.tsv
bash tests/test-installer.sh          # installer behavior in a sandboxed HOME
bash tests/test-installer-download.sh # offline tests of the verified download path (fake curl)
bash tests/test-adversarial-remediations.sh
bash tests/test-release.sh            # offline test of scripts/build-release.sh
```

**Script-coverage registry** — `tests/script-coverage.tsv` lists every script under `skills/*/scripts/` with a level: `behavior` (a test exercises it), `help` (its `--help` is run in an isolated environment) or `static` (syntax and mode checks only, with a written reason). The linter fails when a script has no row.

**CI** (`.github/workflows/ci.yml`, on pushes to `main` and on pull requests):

| Job | Runs on | Steps |
|:----|:--------|:------|
| `test` | ubuntu and macOS | linter, `test-catalog.sh`, `test-scripts.sh`, `test-installer.sh`, `test-installer-download.sh`, `test-adversarial-remediations.sh` |
| `test` (Linux leg only) | ubuntu | ruff (`E9,F`) over `skills/`, `compileall` of skill Python |
| `shellcheck` | ubuntu | shellcheck at warning severity over `install.sh`, `tests/*.sh` and skill shell scripts |

`tests/test-release.sh` is not part of CI; run it locally when you change `scripts/build-release.sh`. Pushing a `v*` tag runs `.github/workflows/release.yml`, which builds `lzr1-skills.tar.gz` and `SHA256SUMS` with `scripts/build-release.sh`.

More: [CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md) · [CHANGELOG.md](CHANGELOG.md) · [LICENSE](LICENSE) · [docs/decisions/](docs/decisions/)

---

## Scope

This public, MIT-licensed repository does not add Lerian-specific skills; those belong in the ring plugin, and non-public Lerian material must not be submitted here. The existing `lerian-helm` skill was audited and contains no non-public material. See [docs/decisions/0001-lerian-skill-scope.md](docs/decisions/0001-lerian-skill-scope.md).

---

## Contributing

Found a skill that belongs here? Have a better version of an existing one? PRs are open. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full authoring contract.

```bash
git clone https://github.com/victorlazari/lzr1-skills.git
cd lzr1-skills

# Add your skill under skills/<your-skill-name>/SKILL.md
# Add the name to skills-list.txt
# Send a PR
```

**Skill format** — frontmatter with `name` and `description`, followed by markdown. Reference files go in `references/`, scripts in `scripts/`, templates in `templates/`.

**Execution protocols** — use parallel specialists only when work branches are genuinely independent. Ordered, stateful workflows such as `coderabbit-reviewer` and `yaml-specialist` should instead use bounded loops, explicit approval gates, deterministic evidence, and stop conditions. Choose the protocol that fits the risk and dependency structure rather than adding concurrency mechanically.

---

## License

MIT — use it, fork it, ship it. See [LICENSE](LICENSE).

---

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

<div align="center">
<sub><a href="LICENSE">License</a> · <a href="CONTRIBUTING.md">Contributing</a> · <a href="SECURITY.md">Security</a> · <a href="CHANGELOG.md">Changelog</a><br/>Built by <a href="https://github.com/victorlazari">Victor Lazari</a> · <a href="https://github.com/victorlazari/lzr1-skills/issues">Report an issue</a></sub>
</div>
