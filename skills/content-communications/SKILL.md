---
name: content-communications
description: Comprehensive content and communications skill covering content strategy, technical writing, copywriting, corporate communications, and developer relations for technology companies. Use when creating content strategies, writing technical documentation, crafting marketing copy, managing corporate communications, or building developer advocacy programs.
---

# Content & Communications

Expert-level content and communications covering content strategy, technical writing, copywriting, corporate communications, and developer relations for technology companies.

## Scope and Triggers

- **Scope**: Creating content strategies, writing technical documentation, crafting marketing copy, managing corporate communications, and building developer relations programs.
- **Triggers**: Activates when the user requests content planning, technical guides, marketing messaging, PR announcements, or developer advocacy materials.
- **Non-goals**: Does not execute social media campaigns (route to `social-media-manager`), perform deep SEO audits (route to `seo-optimization`), or conduct comprehensive WCAG compliance checking (route to `accessibility-audit`).

## Preconditions

1. **Detect Target**: Identify the audience, channel, and communication goal.
2. **Detect Domain**: Determine which communication domain(s) apply (Content Strategy, Technical Writing, Copywriting, Corporate Communications).
3. **Verify Inputs**: Ensure sufficient context is provided (e.g., product details, target audience, key messages).

## Source Freshness

- Volatile facts such as SEO algorithms and accessibility standards change frequently.
- Always verify current WCAG 2.1 guidelines and authoritative style guides (e.g., Google Developer Documentation Style Guide, Microsoft Writing Style Guide) before finalizing content.
- See `references/source-map.md` for the active source map and verification dates.

## Workflow

1. **Understand the context** — What audience, channel, and communication goal?
2. **Detect the required communication domain(s)** from the user request.
3. **Spawn specialists** — If multiple domains are detected, spawn specialists concurrently with their respective reference files (max 4 concurrent).
   - Content strategy and planning → `references/content-strategy.md`
   - Technical writing → `references/technical-writing.md`
   - Copywriting and messaging → `references/copywriting.md`
   - Corporate communications → `references/corporate-comms.md`
4. **Apply guidelines** — Each specialist applies domain-specific guidelines, including accessibility (WCAG 2.1) and SEO standards.
5. **Run the Voice & Tone Synthesizer** — Resolve contradictions, identify gaps, and ensure brand consistency across all specialist outputs.
6. **Validate** — Validate the final output against WCAG 2.1, SEO best practices, and editorial style guides.
7. **Present** — Present the unified content recommendation to the user.

## Safety

- **Read-only discovery**: Research and planning phases are read-only.
- **Mutations**: Require explicit user confirmation before publishing content, sending external communications, or making production-impacting changes.
- **Sensitive content**: Require human review for sensitive corporate communications (e.g., crisis comms, legal announcements).

## Validation

- **Accessibility**: Verify WCAG 2.1 compliance for digital copy.
- **Style**: Validate technical writing against Google/Microsoft style guides.
- **SEO**: Ensure SEO best practices are applied to web content.
- **Syntax**: Run markdown linters or syntax checks on generated documentation.

## Failure Handling

- **Contradictions**: If the Voice & Tone Synthesizer cannot resolve a contradiction, escalate to the user with explicit trade-offs.
- **Missing context**: If inputs are insufficient, pause and request clarification from the user.
- **Rollback**: If published content contains errors, follow the crisis communication framework in `references/corporate-comms.md` to issue corrections.

## Output Contract

- **Structure**: A unified content recommendation or finalized draft.
- **Evidence**: Citations of applied guidelines (e.g., WCAG 2.1, specific style guide rules).
- **Actionable next steps**: Clear instructions for review, approval, or publication.

## Resources

- `references/content-strategy.md`: Planning, governance, and modern digital marketing trends.
- `references/technical-writing.md`: Documentation, accessibility, and inclusive language.
- `references/copywriting.md`: Marketing, messaging, SEO copywriting, and A/B testing.
- `references/corporate-comms.md`: PR, internal comms, multi-channel strategy, and feedback mechanisms.
- `references/source-map.md`: Active source map dictating when to consult specific guidelines.

## Orchestration (Multi-Specialist Protocol)

When multiple domains are detected, spawn all relevant specialists simultaneously.

### Domain Detection Table

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `content strategy`, ... | **Content Strategy** | Content Strategy Specialist | `references/content-strategy.md` |
| `copywriting`, ... | **Copywriting** | Copywriting Specialist | `references/copywriting.md` |
| `technical writing`, ... | **Technical Writing** | TechWrite Specialist | `references/technical-writing.md` |
| `PR`, ... | **Corporate Communications** | CorpComms Specialist | `references/corporate-comms.md` |

### Spawning Logic

- **Single domain detected** → Fall back to single-reference behavior.
- **Multiple domains detected** → Launch all relevant specialists simultaneously.
  - Each specialist receives: **full task context** + its dedicated reference file only.
  - No specialist waits for another — all start at the same time.
  - Maximum concurrent specialists: 4.

### Cross-Domain Synthesizer

After all specialists complete, run one **Voice & Tone Synthesizer** with all specialist outputs that:
1. **Identifies contradictions** between specialist recommendations.
2. **Identifies gaps** — requirements addressed by no specialist.
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation.
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions.
