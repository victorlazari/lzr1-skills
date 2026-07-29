# Complete Reference: Codebase Discovery

> "The README lies eventually. The codebase never does."

This is the shared grounding material for the **Parallel Execution Protocol** — the four
discovery agents that run before a README gets written: **Structure Agent**, **Stack Detector**,
**Docs Auditor**, and **Workflow Analyst**. Each agent reads only its own section below, does its
pass over the target codebase, and hands findings to the **Synthesis Agent**. Jump to your
section and stay there — cross-referencing another agent's territory produces duplicate,
conflicting findings instead of coverage.

Every dimension below ends with a completion checklist. An agent is not done until every box on
its own checklist is checked with a concrete answer, not a guess.

---

## 1. Codebase Structure Discovery

Your job: map the codebase's shape well enough that the Writer Agent can describe "where things
live" without opening a single extra file. You are not detecting languages or frameworks (that's
Stack Detector) — you are detecting **layout and architecture style**.

### Entry point conventions by layout

| Ecosystem / layout | Entry point signal | What it tells you |
| :--- | :--- | :--- |
| Go, flat | `main.go` at repo root | Single binary, no multi-command layout |
| Go, multi-binary | `cmd/<name>/main.go` per subdirectory | Multiple binaries/services from one module |
| Node.js, library | `src/index.ts` / `src/index.js` (+ `main`/`exports` in `package.json`) | Published package, entry is the public API surface |
| Node.js, app | `src/server.ts`, `src/app.ts`, or a `bin/` script referenced in `package.json`'s `bin` field | Runnable service or CLI |
| Next.js (App Router) | `app/layout.tsx` + `app/page.tsx` | Routes are folders under `app/`, not files |
| Next.js (Pages Router) | `pages/_app.tsx` + `pages/index.tsx` | Routes are files under `pages/` |
| Python, script/service | `__main__.py` or a `if __name__ == "__main__":` block | Direct-run script or module |
| Python, Django | `manage.py` at root | Django project; apps live in sibling directories with their own `models.py`/`views.py` |
| Python, package | `pyproject.toml` `[project.scripts]` or `setup.py` `entry_points` | Installable CLI, entry point named explicitly |
| Rust | `src/main.rs` (binary) or `src/lib.rs` (library) | Cargo determines binary vs. library by which file exists |
| Java/Kotlin (Maven/Gradle) | `class Main` with `public static void main`, often under `src/main/java/.../Application.java` (Spring Boot) | Framework-managed entry, look for `@SpringBootApplication` or similar annotation |
| Ruby | `config.ru` (Rack apps) or `bin/rails` (Rails) | Web app entry vs. framework CLI |
| PHP | `public/index.php` or `artisan` (Laravel) | Web-served front controller vs. framework CLI |

If more than one candidate exists (e.g. both `cmd/api/main.go` and `cmd/worker/main.go`), record
all of them — that itself is a structural finding ("multi-service repo"), not a decision to make
for the Writer Agent.

### Directory layout signals for architecture style

**Monorepo markers** — presence of any of these means "workspace of multiple packages," not a
single-package repo:

| File | Tooling implied |
| :--- | :--- |
| `turbo.json` | Turborepo |
| `nx.json` | Nx |
| `pnpm-workspace.yaml` | pnpm workspaces |
| `lerna.json` | Lerna |
| `rush.json` | Rush |
| `package.json` with a top-level `"workspaces"` array | npm/yarn workspaces (no dedicated config file) |
| `go.work` | Go workspaces (multi-module) |
| `Cargo.toml` with a `[workspace]` table | Cargo workspace |

When you find one, also record: how many packages/apps live under it (count `apps/*` and
`packages/*`, or whatever the workspace glob defines), since "monorepo with 3 packages" and
"monorepo with 40 packages" call for very different README strategies downstream.

**Layered architecture signals**:

- **Go**: `internal/` (code that cannot be imported by other modules — a strong signal of
  "this is an application, not a library") alongside `pkg/` (deliberately exported, reusable
  code) indicates a layered, dependency-conscious design. `internal/domain/`,
  `internal/adapter/`, `internal/usecase/` naming suggests clean/hexagonal architecture
  specifically.
- **Frontend, feature-folder style**: directories named after business concepts
  (`features/checkout/`, `features/auth/`, each containing its own components, hooks, and
  tests) — colocation by domain.
- **Frontend, layer-folder style**: directories named after technical role
  (`components/`, `hooks/`, `services/`, `store/`) shared across the whole app — colocation by
  technical kind. Note which one you find; it changes how you'd describe "where to add a new
  feature."
- **Backend, layered (any language)**: parallel top-level dirs like `controllers/`,
  `services/`, `repositories/`, `models/` signal classic MVC/N-tier layering.
- **Domain-driven**: `domain/`, `application/`, `infrastructure/` naming is a DDD/hexagonal
  tell regardless of language.

### What to explicitly ignore

Never walk into, count files inside, or report on these as "meaningful directories" — they are
generated or vendored, not authored:

- `node_modules/`, `vendor/`, `bower_components/`
- `dist/`, `build/`, `out/`, `.next/`, `.nuxt/`, `.svelte-kit/`, `target/` (Rust/Java), `bin/` and
  `obj/` (.NET)
- `__pycache__/`, `.pytest_cache/`, `*.egg-info/`, `.venv/`, `venv/`
- `.git/`, `.terraform/`, `.turbo/`, `.cache/`, `coverage/`, `.nyc_output/`
- Lockfile-adjacent noise: don't enumerate `node_modules` contents even indirectly via a lockfile
  walk

If one of these directories is unusually large or has an unusual name (e.g. a committed
`vendor/` in a Go repo — normal — vs. a committed `dist/` in a source repo — unusual, possibly a
sign of a build-artifact leak worth flagging as a documentation/hygiene note, not a structural
one), that observation belongs to the Docs Auditor or is a footnote, not the structural map
itself.

### Structure discovery checklist

- [ ] I can name the entry point file(s) and which layout convention they match
- [ ] I can name the top 3-5 meaningful directories and state each one's purpose in one line
- [ ] I've determined monorepo vs. single-package repo, and if monorepo, named the workspace tool
      and approximate package count
- [ ] I've identified whether the architecture reads as layered, feature-based, DDD, or "flat/no
      clear pattern yet" — and said so plainly rather than forcing a label that doesn't fit
- [ ] I have not reported on anything inside `node_modules/`, `dist/`, `vendor/`, `.next/`,
      `target/`, `__pycache__/`, or `.git/`

---

## 2. Tech Stack Detection

Your job: name every language, framework, database, and deployment target the project actually
uses, backed by a specific file you looked at — never by guessing from the README (that's stale
until the Docs Auditor says otherwise) or from directory names alone.

### Manifest files by ecosystem

| Language / ecosystem | Manifest file(s) | What it reveals |
| :--- | :--- | :--- |
| JavaScript/TypeScript | `package.json` + lockfile (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb`) | Dependencies, `scripts` block, `engines` (required Node version), package manager in use (inferred from which lockfile exists) |
| Go | `go.mod` + `go.sum` | Module path, Go version pin, direct + indirect dependencies |
| Python | `requirements.txt`, `pyproject.toml`, `Pipfile` (+ `Pipfile.lock`), `setup.py`/`setup.cfg` | Dependencies; `pyproject.toml` additionally reveals build backend, tool config (`[tool.poetry]`, `[tool.ruff]`, etc.), and Python version constraint |
| Rust | `Cargo.toml` + `Cargo.lock` | Crate deps, edition, workspace membership |
| Ruby | `Gemfile` + `Gemfile.lock` | Gem deps, Ruby version (`.ruby-version` or `Gemfile`'s `ruby` directive) |
| PHP | `composer.json` + `composer.lock` | Package deps, PHP version constraint, PSR autoload mapping |
| Java/Kotlin (Maven) | `pom.xml` | Deps, parent POM, Java version (`<maven.compiler.source>`) |
| Java/Kotlin (Gradle) | `build.gradle` / `build.gradle.kts` + `settings.gradle` | Deps, plugins, multi-module structure |
| .NET | `*.csproj` / `*.fsproj` + `*.sln` | Target framework (`<TargetFramework>`), package refs (`<PackageReference>`) |
| Elixir | `mix.exs` | Deps, app config, OTP application name |

Always check the lockfile alongside the manifest — the manifest states intent (`^18.0.0`), the
lockfile states reality (what's actually resolved and installed). A manifest without a lockfile
committed is itself a finding (dependency versions aren't pinned/reproducible).

### Detecting a database or external service without an explicit manifest entry

Not every dependency announces itself as a package. Triangulate from these three signal types,
in order of reliability:

1. **`docker-compose.yml` / `docker-compose.yaml` service names.** This is the most reliable
   signal in the repo — a service block literally named `postgres`, `redis`, `kafka`, or using
   image lines like `image: postgres:15`, `image: redis:7-alpine`, `image: confluentinc/cp-kafka`
   tells you the exact system and often the exact version the team develops against.
2. **Environment variable naming patterns** — check `.env.example`, `.env.sample`, or wherever
   config is loaded (`config/`, `settings.py`, `os.Getenv` calls):
   - `DATABASE_URL`, `POSTGRES_*`, `MYSQL_*` → relational DB
   - `MONGO_URI`, `MONGODB_URI` → MongoDB
   - `REDIS_URL`, `REDIS_HOST` → Redis (or Valkey — check the compose image, they share the
     protocol)
   - `KAFKA_BROKERS`, `KAFKA_BOOTSTRAP_SERVERS` → Kafka (or a Kafka-protocol-compatible broker
     like Redpanda — again, check the compose image or client library for which one)
   - `RABBITMQ_URL`, `AMQP_URL` → RabbitMQ
   - `S3_BUCKET`, `AWS_*` → S3-compatible object storage
   - `ELASTICSEARCH_URL`, `ES_URL` → Elasticsearch/OpenSearch
3. **Import/require statements for known client libraries**, when the above two are absent or you
   need to confirm which driver is actually used (e.g. `pg` vs `postgres` npm packages both talk
   to Postgres but have different APIs — matters for the Writer Agent's setup instructions):
   - Go: `database/sql` + `lib/pq`/`jackc/pgx` (Postgres), `go-redis/redis`, `segmentio/kafka-go`
   - Node: `pg`, `mysql2`, `mongoose`/`mongodb`, `ioredis`, `kafkajs`, `amqplib`
   - Python: `psycopg2`/`asyncpg`, `pymongo`, `redis`, `kafka-python`, `pika`

Cross-check all three when possible — a `REDIS_URL` env var plus a `redis:7` compose service plus
an `ioredis` import in code is a confirmed finding; any one alone is a hint worth stating with
appropriate uncertainty ("likely uses Redis, based on env var naming only — no client library or
compose service confirms this").

### Detecting runtime and deployment target

| Signal file | What it tells you |
| :--- | :--- |
| `Dockerfile` (check the `FROM` base image) | Runtime language/version (`FROM node:20-alpine`, `FROM golang:1.22`), and whether it's a multi-stage build (build vs. runtime image can differ) |
| `Procfile` | Heroku-style process types (`web:`, `worker:`) — implies Heroku or a Heroku-compatible PaaS |
| `vercel.json` | Vercel deployment, often paired with Next.js |
| `netlify.toml` | Netlify deployment, usually static/JAMstack |
| `fly.toml` | Fly.io deployment |
| `render.yaml` | Render deployment |
| Helm chart (`Chart.yaml` + `values.yaml`, usually under `charts/` or `deploy/`) | Kubernetes deployment; `values.yaml` reveals resource limits, replica counts, exposed ports, and env var wiring |
| `serverless.yml` | Serverless Framework (AWS Lambda or similar) |
| `.github/workflows/*deploy*.yml` (deploy step specifically, not just CI) | Often the most concrete evidence of where code actually ships, when no dedicated deploy config exists |
| `terraform/` or `*.tf` files | Infrastructure as code; check `provider` blocks for cloud target (AWS/GCP/Azure) |

### Stack detection checklist

- [ ] I can name every language in the repo with the manifest file that proves it
- [ ] I can name the package manager in use (proven by which lockfile exists, not assumed)
- [ ] I can name every database/queue/external service, each tagged with how it was confirmed
      (compose service / env var / import — or a combination)
- [ ] I can name the runtime/deployment target (container base image, PaaS config, or Helm/K8s)
- [ ] I have not inferred a stack element from the README or from a directory name alone — every
      claim traces to a manifest, lockfile, compose file, env var, import, or deploy config

---

## 3. Existing Documentation Audit

Your job: assess what documentation already exists, how good it is, and how stale it is — not to
rewrite it, and not to praise it. The Writer Agent needs to know what to keep, what to fix, and
what's actively misleading.

### What "good" looks like, per artifact

| Artifact | What "good" looks like |
| :--- | :--- |
| **README** | Answers **What** (one-sentence description), **Why** (problem it solves / who it's for), and **How** (install + first-run command) all within the first screen — before any scrolling. No wall of badges before the pitch. |
| **Inline comments** | Explain **why**, not **what** — a comment restating `// increment i by 1` above `i++` is noise; a comment explaining *why* a retry uses exponential backoff with a specific cap, or why a workaround exists for a specific upstream bug, is signal. Comment density should track complexity, not line count. |
| **API docs** | A reference exists **per endpoint or per public function**, and it matches the current signature — parameter names, types, and return shapes in the doc match the code, not a prior version of it. |
| **CHANGELOG** | Follows one consistent format throughout (ideally [Keep a Changelog](https://keepachangelog.com/) or auto-generated from conventional commits) — not free-form prose in some entries and structured bullets in others. Its most recent entry roughly tracks the most recent release/tag. |
| **CONTRIBUTING guide** | States concrete setup steps (not just "clone and go") and a concrete PR process (branch naming, required checks, review expectations) — a first-time contributor could follow it without asking a question in Slack first. |

### Scoring rubric

Apply this same four-level scale to every artifact you assess:

| Level | Definition |
| :--- | :--- |
| **Missing** | The artifact doesn't exist at all, or exists as an empty/placeholder stub (a README that's just a title, a CHANGELOG with no entries). |
| **Stale** | The artifact exists and was once accurate, but now contradicts the current code — wrong commands, renamed files, version mismatches, or dead links (see staleness signals below). |
| **Adequate** | The artifact is accurate and covers the basics, but is thin, unstructured, or missing a section a reader would expect (e.g. a README with What/How but no Why, or CONTRIBUTING with setup steps but no PR process). |
| **Excellent** | Accurate, complete against the "what good looks like" bar above, and actively helps a new reader/contributor with no follow-up questions needed for the basics. |

Score each of the five artifacts independently — a project can have an Excellent README and a
Missing CHANGELOG at the same time. Don't average them into one number; report per-artifact.

### Signals of documentation staleness

Actively look for these rather than assuming docs are current:

- **References to renamed or removed files/commands** — a README instructing `npm run start:dev`
  when `package.json`'s `scripts` block has no such key (only `dev`), or pointing at a file path
  that no longer exists in the tree.
- **Version numbers that don't match the manifest** — a README badge or prose claiming
  "requires Node 18" while `package.json`'s `engines.node` says `>=20`, or a doc referencing
  `v1.x` APIs when the current package version is `3.x`.
- **Dead links** — internal links to moved/deleted docs, or external links returning 404s (you
  don't need to fetch every link, but flag ones that reference clearly-renamed internal paths).
- **Screenshots or example output** that show a UI, CLI output format, or config file structure
  visibly different from what's in the current codebase.
- **A CHANGELOG or version history whose latest entry date/version is far behind the most recent
  git tag or the version in the manifest** — a strong, easy-to-check staleness signal.

### Docs audit checklist

- [ ] I've scored all five artifacts (README, inline comments, API docs, CHANGELOG, CONTRIBUTING)
      independently on the Missing/Stale/Adequate/Excellent scale
- [ ] For every artifact scored Stale, I've cited the specific contradiction (quote the doc line
      and the code/manifest line it conflicts with)
- [ ] I've checked at least one version-number cross-reference between docs and the manifest file
- [ ] I've noted whether inline comments skew toward "explains why" or "restates what," with an
      example of each if both patterns exist
- [ ] I have not silently corrected a stale doc in my findings — I report what it currently says
      and what's actually true, and let the Synthesis Agent own the reconciliation

---

## 4. Team Workflow Analysis

Your job: reconstruct how this team actually ships code day to day — CI/CD, pre-commit
enforcement, and local dev setup — so the README's "Development" section reflects real practice,
not an idealized one.

### CI/CD config by platform

| Platform | File location |
| :--- | :--- |
| GitHub Actions | `.github/workflows/*.yml` |
| GitLab CI | `.gitlab-ci.yml` |
| Jenkins | `Jenkinsfile` |
| CircleCI | `.circleci/config.yml` |
| Azure Pipelines | `azure-pipelines.yml` |
| Travis CI | `.travis.yml` |
| Bitbucket Pipelines | `bitbucket-pipelines.yml` |
| Drone CI | `.drone.yml` |

Don't just note the file exists — open it and extract: what triggers it (push/PR/tag), what
stages it runs (lint, test, build, deploy), and whether a deploy stage exists at all. A repo with
CI that only lints and tests (no deploy stage) tells you deployment is either manual or handled
by a separate system — worth flagging so the Writer Agent doesn't invent a deploy story.

### Git hooks and pre-commit tooling signals

| Signal | What it means |
| :--- | :--- |
| `.husky/` directory | Husky-managed Git hooks (Node ecosystem) — check `.husky/pre-commit`, `.husky/pre-push` for what actually runs |
| `.pre-commit-config.yaml` | Python-ecosystem `pre-commit` framework — lists the exact hooks (linters, formatters, secret scanners) enforced before every commit |
| `lint-staged` key in `package.json` (usually paired with Husky) | Runs linters/formatters only on staged files, not the whole repo, on commit |
| `.git/hooks/` containing non-sample scripts | Hooks configured directly without a framework — less common, worth noting as "manual hook setup" |
| `commitlint.config.js` / `.commitlintrc` | Enforces a commit message convention (often Conventional Commits) — implies a semantic-release or changelog-automation pipeline downstream |

The presence of enforced hooks is a strong signal for the README: it means "run the linter
before committing" isn't a suggestion in this repo, it's mechanically enforced, and the README's
contribution section should say so plainly rather than as a polite request.

### Where local dev workflow is defined

- **`Makefile`** — list every target (`make dev`, `make test`, `make build`, `make lint`). A
  Makefile with a rich target list is usually the single most reliable source of truth for "how
  do I actually work on this," often more current than the README itself.
- **`package.json` `scripts` block** — the Node-ecosystem equivalent of Makefile targets; note
  `dev`, `build`, `test`, `lint`, `start` at minimum, and any custom scripts that hint at
  non-obvious workflow steps (`predev`, `postinstall` hooks running codegen, etc.).
  Also check `Taskfile.yml` (Task) or `justfile` (Just) as Makefile alternatives.
- **`docker-compose.yml`** — reveals the full local dependency stack (see Stack Detector's use of
  this same file) and, from the `command:`/`entrypoint:` of the app's own service block, how the
  app itself is expected to run locally.
- **`devcontainer.json` / `.devcontainer/`** — signals the team standardizes on VS Code Dev
  Containers or GitHub Codespaces; check `postCreateCommand` for the exact bootstrap steps a new
  contributor's environment runs automatically.
- **`.env.example` / `.env.sample`** — enumerate every variable listed; this is the definitive
  list of what a contributor must configure to run the project locally at all. Cross-reference
  against Stack Detector's findings — an env var here for a service Stack Detector didn't
  otherwise find is a signal worth surfacing (e.g. a `SENTRY_DSN` reveals error-tracking
  integration that no manifest would show).

### Workflow analysis checklist

- [ ] I've identified every CI/CD platform in use and what each pipeline's stages actually do
      (not just that a config file exists)
- [ ] I've determined whether commits/PRs are gated by an automated hook, and named the tooling
      (Husky/pre-commit/lint-staged/commitlint) if so
- [ ] I've extracted the concrete local-dev commands (Makefile targets or npm scripts) a new
      contributor would run, in the order they'd run them (setup → run → test)
- [ ] I've listed every required environment variable from `.env.example` (or equivalent) and
      flagged any that imply a service not already surfaced by Stack Detector
- [ ] I've noted whether a devcontainer/Codespaces setup exists, since that changes the "getting
      started" instructions the Writer Agent should produce

---

## Cross-Dimension Conflicts

These four sections describe four different lenses on the same codebase, and they will sometimes
disagree — that disagreement is signal, not noise. If your finding contradicts something another
agent is likely to find (for example: Docs Auditor sees the README claim "requires Node 18" while
Stack Detector sees `package.json`'s `engines.node` require `>=20`; or Structure Agent calls the
repo single-package while Workflow Analyst finds a CI matrix building three separate deploy
artifacts), do **not** quietly pick a side and report only the version you believe. Flag it
explicitly as **CONFLICT: <the two contradictory claims, each with its source file>** in your
findings and hand both halves to the Synthesis Agent. Resolving the contradiction is the
Synthesis Agent's job, not yours — a discovery agent that silently resolves a conflict destroys
the evidence the Synthesis Agent needs to decide which source is actually authoritative.
