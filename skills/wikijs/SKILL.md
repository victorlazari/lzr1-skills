---
name: wikijs
description: Advanced administration, API automation, and content management for Wiki.js enterprise deployments.
---

# Wiki.js Specialist Skill

This skill provides comprehensive capabilities for managing, automating, and optimizing Wiki.js instances. It covers advanced configuration, GraphQL API interactions, Git synchronization, rendering pipeline customization, and performance tuning.

## When to Use

Use this skill when you need to:
- Automate page creation, updates, or migrations via the Wiki.js GraphQL API.
- Configure bidirectional Git storage synchronization for docs-as-code workflows.
- Manage user access, roles, and private namespaces.
- Customize the rendering pipeline (e.g., KaTeX, MathJax, Mermaid, PlantUML).
- Optimize Wiki.js performance (connection pooling, caching, CDN integration).
- Troubleshoot deployment issues, Git sync conflicts, or asset management problems.
- Perform bulk operations on the page tree or tag system.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Bulk page migrations across locales | Migration Agent | Parallel migration of page batches |
| Large-scale content updates | Content Updater | Parallel updates via GraphQL API |
| Multi-namespace permission audits | Security Auditor | Parallel review of namespace access controls |
| Comprehensive broken link checks | Link Checker | Parallel scanning of the page tree |

### Spawning Rules
- Spawn when 3+ independent items (pages, namespaces, locales) need the same operation.
- Each sub-agent receives: API credentials, specific target paths/IDs, and success criteria.
- Results are aggregated and cross-referenced for conflicts (e.g., Git sync collisions).
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Authentication & Setup**: Ensure valid API Bearer tokens are available for GraphQL interactions. Verify the target Wiki.js instance URL.
2. **Assessment**: Determine the scope of the operation (e.g., single page update, bulk migration, configuration change).
3. **Execution**:
   - For API tasks: Construct and execute the appropriate GraphQL mutations or queries.
   - For configuration tasks: Modify `config.yml` or use the administration panel.
   - For content tasks: Utilize the correct editor format (Markdown, WYSIWYG, etc.) and handle asset uploads if necessary.
4. **Validation**: Verify the changes via API queries or by checking the web interface. Ensure no Git sync conflicts were introduced.
5. **Optimization**: Apply performance tuning (caching, minification) if applicable to the task.

## Core Principles

- **Docs-as-Code**: Treat documentation like software. Leverage Git synchronization for version control and collaborative editing.
- **API-First**: Utilize the GraphQL API for automation and bulk operations to ensure consistency and efficiency.
- **Security by Design**: Implement granular access controls using private pages and namespaces. Secure API tokens and use SSH for Git sync.
- **Performance Optimization**: Configure connection pooling, caching, and CDNs to maintain high availability and fast response times.
- **Structured Content**: Adhere to strict page path rules and utilize the tag system for effective content organization.

## Key References

- [Complete Reference Guide](./references/complete-reference.md): In-depth documentation on advanced patterns, CLI, and API usage.
- [Reading List](./references/reading-list.md): Curated books and articles on Wiki.js, knowledge management, and related technologies.

---

## Adversarial Verification Panel

For each significant content and configuration audit finding produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong content and configuration audit findings from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Migration Agent, Content Updater, Security Auditor, Link Checker) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Security Auditor recommends restricting a namespace to private access while the Migration Agent recommends bulk-migrating public pages into that same namespace without access control changes)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified aggregated cross-referenced report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
