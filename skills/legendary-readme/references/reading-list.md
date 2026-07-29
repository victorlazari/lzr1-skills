# Reading List: Audience & Purpose Research

> "A README that speaks to everyone speaks clearly to no one for the first 30 seconds."

This is the grounding material for the **Audience Researcher** agent in the Parallel Execution
Protocol. Its dimension: who uses this repo, what they need to know first, common onboarding
friction. Output feeds the Synthesis Agent, which reconciles it against the other discovery
agents' findings before the Writer Agent drafts a single section order.

The job here is not "guess a persona and write for them." It's: identify which personas actually
show up for *this* repo, in what proportion, and what the highest-friction gap is for the one
most likely to bounce. A CLI tool's README optimizes for a different reader than a library's, and
a library used mostly as an internal dependency optimizes for a different reader than one with
2,000 GitHub stars and a Discord.

---

## 1. Who Reads a README (Persona Map)

Five personas cover nearly all README traffic. Any given repo gets some mix of these — the
research task is figuring out the mix, not picking one.

| Persona | Arrives via | What they decide in 30s | Hits first | Bounces if | Stays if |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **The Evaluator** | Search, "awesome-X" list, a coworker's Slack link | Is this worth adopting as a dependency? | Title + tagline + first paragraph | No clear "what problem does this solve," no comparison signal, looks unmaintained | Sees the problem stated in one sentence and a credible reason to pick this over the obvious alternative |
| **The New Contributor** | CONTRIBUTING.md link, "good first issue" label, a maintainer's invite | Can I get this running and land a PR? | Install/Setup, then CONTRIBUTING | Setup fails on the first command, no contribution norms stated, tests won't run locally | Setup works in one pass and there's a visible path from "cloned" to "PR opened" |
| **The Existing User Debugging** | Google search landing mid-doc, an error message, a Stack Overflow link | Does this README answer my specific error? | Troubleshooting/FAQ, or Ctrl+F for their error string | Pitch/badges/demo GIF stand between them and the answer, no FAQ or Troubleshooting section exists at all | Their exact symptom or error text appears verbatim, with a fix, within one scroll |
| **The Maintainer's Future Self** | Their own repo, six months after last touching it | What did I build, how is it configured, how do the pieces fit? | Architecture, Configuration, or a table of env vars/flags | Config options are undocumented and only exist as inline code comments they now have to re-read | Every config surface (flags, env vars, file formats) is enumerated with defaults, not just examples |
| **The Curious Browser** | Trending list, a tweet, a "cool projects" newsletter | Is this fun/impressive enough to star or try? | Banner, tagline, demo GIF, badges | Wall of text, no visual, reads like a spec sheet before it reads like a pitch | A demo (GIF, one-liner, screenshot) lands before the reader has to parse a single paragraph |

Notes for the research writeup:
- These are not mutually exclusive across time — the same person is a Curious Browser today and
  a Debugging User in six months after they've adopted the tool.
- A README that nails all five in one linear document is rare and usually not the goal; the goal
  is picking a **primary** and **secondary** persona and ordering sections so the primary's need
  is satisfiable without reading past their bounce point (see Section 5, Handoff Format).
- The Evaluator and the Curious Browser are both "first 30 seconds, pre-install" personas but want
  opposite tones — spec-like credibility vs. demo-like delight. Confusing which one dominates for
  a given repo is the most common miscalibration in this research step.

---

## 2. Signals That Reveal the Real Audience

Don't ask "who is this for" in the abstract — check the repo and its surrounding artifacts for
evidence. Each signal below narrows the persona mix; none is conclusive alone, so triangulate at
least two before committing to a primary persona.

| Signal to check | How to check it | What it implies |
| :--- | :--- | :--- |
| `CONTRIBUTING.md` exists, and its depth | `ls` repo root and `.github/`; skim length and specificity (does it name a test command, a branch strategy, a CLA?) | Present + detailed → expects the New Contributor persona in volume, open-source-facing. Absent → likely internal-only or a solo/small-team project not soliciting outside PRs |
| Issue/PR templates | Check `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md` | Present → external contributor and bug-report traffic is expected and structured; the README should point at Troubleshooting/FAQ before "open an issue" |
| Package registry presence | Search npm, PyPI, crates.io, pkg.go.dev, RubyGems for the package name | Listed → audience skews toward "install and use as a dependency" (Evaluator, Debugging User) over "clone and read the source." Unlisted → audience skews toward direct-clone users (CLI tool, internal service, template repo) |
| Org type | Check if the repo lives under a personal account, a company org, or a foundation (e.g. CNCF, Apache) | Personal → lower expected polish, more forgiving Evaluator. Company org → Evaluator expects a support/SLA signal. Foundation → Evaluator expects governance docs (SECURITY.md, GOVERNANCE.md) to exist |
| Stars/forks/badge presence | Check the repo header and any CI/coverage/version badges | A rough popularity proxy only — use cautiously. High stars with a thin README suggests the project succeeded on word-of-mouth despite the docs, not because of them; don't assume current traffic mix matches what got it there |
| Existing issue volume and labels | Skim open issue count and labels (`bug`, `question`, `help wanted`) | High `question`-labeled volume on a recurring topic → that topic is a top candidate for a dedicated README section (see Section 4) |
| Recency of commits/releases | Last commit date, last tagged release | Stale (>6-12 months, project-dependent) → an Evaluator will read this as a maintenance risk before reading anything else the README says |
| CI badge status | Passing/failing build badge in the header | Broken CI badge visible on the README is a specific, concrete Evaluator bounce point — worse than no badge at all |

If these signals conflict (e.g., npm-listed package with no CONTRIBUTING.md and no issue
templates), report the conflict explicitly to Synthesis rather than resolving it silently — it
usually means the maintainer wants usage but not contribution traffic, which changes which
sections get emphasis.

---

## 3. Common Onboarding Friction Points

A catalog of where READMEs lose readers, in roughly descending order of how early they cost a
reader. Check the repo's actual README (if one exists) and setup path against each row.

| Friction point | Symptom | Fix |
| :--- | :--- | :--- |
| No prerequisite version stated | First install/build command fails with a cryptic engine or syntax error | State exact minimum version (`Node >= 18`, `Go 1.22+`, `Python 3.10+`) directly above the first command, not buried in a `package.json`/`go.mod` the reader hasn't opened yet |
| Install command assumes a package manager the reader doesn't have | Copy-pasted command errors with "command not found" | Give the command for at least two ecosystems' common managers (npm/pnpm/yarn; pip/uv/poetry; brew/apt), or state the one assumption explicitly ("requires `pnpm`") so the reader isn't guessing why it failed |
| "Quick start" hides undocumented prior steps | Reader follows steps 1-3 exactly, hits a failure that's actually step 0 (a running database, an API key, an env var) | Enumerate every external dependency the quick start needs *before* the first command — a short "you'll need" list with a database, an API key, a `.env` file — even if it feels obvious to the maintainer |
| Jargon in the first paragraph before any example | Reader can't tell what the project does without already knowing the domain | Lead with a plain-language sentence and, ideally, a concrete before/after or input/output example ahead of any acronym or internal terminology |
| No maintenance signal | No recent commits, no version badge, no "last release" date visible | State it plainly if the project is stable-but-done ("feature-complete, in maintenance mode") — an Evaluator who can't tell active from abandoned will assume abandoned and leave, even if the code works fine |
| Demo/pitch blocks the fix | Debugging User has to scroll past marketing copy to reach Troubleshooting | Put Troubleshooting/FAQ high enough in the table of contents (or link it near the top) that it doesn't require scrolling past the full pitch |
| Config options shown only as examples, never enumerated | Maintainer's Future Self has to grep source to find what flags/env vars exist | Provide a full table of config surface (name, default, description) even if most users only ever touch two of the rows |
| No indication of scope/non-goals | Evaluator can't tell if their use case is in-scope without trial and error | One sentence on what this deliberately does *not* do saves an Evaluator a wasted install |

---

## 4. Purpose Research Questions

Answer these before handing off. Where possible, cite the actual source (issue #, commit hash,
PR title) rather than paraphrasing from memory — the Synthesis Agent needs traceable evidence,
not vibes.

- **What problem does this solve, in the maintainer's own words?** Check issue descriptions, PR
  titles, commit messages, and any design-doc/RFC in the repo — not just the README tagline,
  which is often written last and optimized for brevity over accuracy.
- **What kind of thing is this: library, CLI tool, or service?**
  - *Library* (imported/required inside other code) → Installation + API Reference + Usage
    Examples matter most; Deployment rarely applies.
  - *CLI tool* (invoked directly by a human or script) → Installation + Command Reference +
    Quick Start matter most; API Reference rarely applies.
  - *Service* (deployed and called over a network) → Deployment/Configuration + API/Endpoint
    Reference + Architecture matter most; a "quick start" needs to cover running it locally
    (Docker Compose, etc.), not just calling it.
  - Some repos are more than one (a library with a companion CLI) — note the split and which one
    is primary.
- **Is there a comparable or competing project?** Check the README's own "Why not X" section if
  one exists, check issues asking "how does this compare to Y," check if the project name or
  tagline implicitly positions against an incumbent (e.g., "X, but fast" or "a lighter Y").
  Report the comparison target even if the README currently doesn't mention it — that's a gap for
  the Writer Agent to consider filling.
- **What's the single most common question in the issue tracker that a good README section would
  preempt?** Skim issue titles/labels for a repeated theme (a specific setup error, a specific
  "does this support X" question, a specific misconfiguration). This is often the highest-leverage
  single fact this research step can produce — it points directly at a Troubleshooting/FAQ entry
  that would measurably cut support burden.
- **Who actually opens issues and PRs today?** Skim a sample of recent issue/PR authors — internal
  team members, external strangers, or dependabot/bots only. This is a stronger signal of actual
  audience than any static file check in Section 2.

---

## 5. Handoff Format

Findings go to Synthesis as a compact structured summary, not prose. The Writer Agent should be
able to prioritize sections from this without re-reading the source repo.

```
AUDIENCE RESEARCH SUMMARY
Primary persona:      <one of the five, or a named blend, with one-sentence justification>
Secondary persona:    <one of the five, with one-sentence justification>
Repo type:            <library | CLI tool | service | mixed>
Top 3 friction risks: 1. <friction point + concrete evidence>
                       2. <friction point + concrete evidence>
                       3. <friction point + concrete evidence>
Differentiation angle: <one sentence: what this is instead of, or why it beats the obvious alternative>
Maintenance signal:    <active | stale | maintenance-mode — with evidence (last commit/release date)>
Top preemptable question: <the most common issue-tracker question a README section could kill>
```

Keep each field to one sentence. If evidence conflicts (Section 2's "signals conflict" case),
note the conflict inline rather than smoothing it over — Synthesis needs to know where the
research was ambiguous, not just where it was confident.

---

## Audience research is complete when...

- [ ] I can state, in one sentence: **who this is for** (primary persona, named, with the signal
      that supports it)
- [ ] I can state, in one sentence: **what they need in the first screen** (the section or fact
      that satisfies their 30-second decision)
- [ ] I can state, in one sentence: **the one friction point most likely to lose them** (concrete,
      evidenced by an actual gap in setup/docs or an actual issue-tracker pattern, not a guess)
