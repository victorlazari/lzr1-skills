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
