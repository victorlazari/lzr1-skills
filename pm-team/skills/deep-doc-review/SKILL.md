---
name: lzr1:deep-doc-review
description: |
  Deep review of project documentation before entelzr1 dev-cycle.
  Finds errors, inconsistencies, gaps, missing data, and contradictions
  across PRD, TRD, API design, data model, and other pre-dev artifacts.
  Cross-references information between docs — not just reviewing one doc
  in isolation — to catch mismatches that cause implementation failures.
---

# Deep Doc Review

## When to use

- Before starting dev-cycle (validate doc quality as a pre-gate)
- After completing pre-dev workflow (lzr1:pre-dev-feature or lzr1:pre-dev-full)
- When user requests project documentation review
- After significant changes to reference docs (PRD, TRD, API design, data model)

## Skip when

- Code review needed (use lzr1:codereview instead)
- Docs do not exist yet (run pre-dev workflow first)
- Reviewing a single simple file (do it directly without the skill)

## Sequence

**Runs before:** lzr1:dev-cycle, lzr1:write-plan
**Runs after:** lzr1:pre-dev-feature, lzr1:pre-dev-full

## Related

**Complementary:** lzr1:pre-dev-prd-creation, lzr1:pre-dev-trd-creation, lzr1:pre-dev-api-design, lzr1:pre-dev-data-model, lzr1:pre-dev-task-breakdown
**Differentiation:** lzr1:codereview reviews code. lzr1:deep-doc-review reviews documentation artifacts against each other.


> Adapted from alexgarzao/optimus (optimus-deep-doc-review)

Deep cross-reference review of project documentation to catch contradictions before they become implementation bugs. Emphasis is on **inconsistencies between docs**, not just intra-doc quality.

## Phase 0: Discover and Load Docs

### Step 0.1: Identify Docs to Review

If user specified files, use those. Otherwise, auto-discover:

**Search locations:**
- `docs/pre-dev/<feature>/` (lzr1 pre-dev artifacts)
- `docs/` (general project docs)
- Root directory (README, CHANGELOG, ARCHITECTURE)

**Include:** PRD, TRD, API design, data model, task specs, subtask specs, dependency map, delivery plan, research docs, coding standards, README, CHANGELOG

**Exclude:** generated files, node_modules, build artifacts, binary files, test fixtures

Present discovered docs list to user before proceeding.

### Step 0.2: User Confirms Scope

Show doc list and ask: "Are there additional documents to include or any to exclude?"

### Step 0.3: Load All Docs

Read each document. Build a cross-reference map: entities, fields, endpoints, and decisions mentioned in each doc.

## Phase 1: Cross-Reference Analysis

For each pair of docs that share entities or concepts, check for contradictions:

| Cross-Reference | What to Check |
|----------------|---------------|
| PRD ↔ TRD | TRD covers all PRD requirements; TRD doesn't add new requirements; NFRs align |
| TRD ↔ API Design | API operations match TRD component interfaces; data shapes consistent |
| API Design ↔ Data Model | API response fields exist in data model; field names consistent; types compatible |
| Data Model ↔ Task Breakdown | All entities have creation/migration tasks; relationships implemented |
| TRD ↔ Dependency Map | All TRD components have explicit dependencies; no undeclared tech |
| PRD ↔ Tasks | All PRD features have at least one task; task deliverables match PRD goals |

## Phase 2: Intra-Document Quality

For each document:

| Check | Description |
|-------|-------------|
| Completeness | Required sections present; no "TBD" or placeholder content |
| Internal consistency | Same entity/field named the same way throughout |
| Format compliance | Gate-specific format requirements met |
| Clarity | No ambiguous language; success criteria testable |

## Phase 3: Findings Report

Classify findings:

| Severity | Criteria | Action |
|----------|----------|--------|
| **CRITICAL** | Contradiction that will cause implementation failure | MUST fix before dev-cycle |
| **HIGH** | Missing information that blocks a specific task | Should fix before dev-cycle |
| **MEDIUM** | Inconsistency that will cause confusion | Fix preferred |
| **LOW** | Style, formatting, minor clarity | Optional |

Present findings to user with:
- Finding description
- Documents affected
- Specific location (doc → section → line reference)
- Suggested correction

## Phase 4: Apply Approved Corrections

For each finding user approves:
1. Make the correction directly in the affected document
2. Mark finding as FIXED
3. Continue to next finding

## Phase 5: Summary

```markdown
# Deep Doc Review Summary

**Date:** {YYYY-MM-DD}
**Documents Reviewed:** {N}
**Cross-References Checked:** {N pairs}

## Finding Summary
| Severity | Found | Fixed | Skipped |
|----------|-------|-------|---------|
| CRITICAL | N | N | N |
| HIGH | N | N | N |
| MEDIUM | N | N | N |
| LOW | N | N | N |

## Status
✅ CLEARED — Ready for lzr1:dev-cycle
⚠️ ISSUES REMAIN — {N} unfixed critical/high findings
```

**Output:** `docs/pre-dev/{feature}/doc-review-{date}.md`
