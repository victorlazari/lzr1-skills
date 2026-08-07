---
name: wikijs
description: Advanced administration, API automation, and content management for Wiki.js enterprise deployments. Triggers on requests to configure Git sync, manage content via GraphQL, or verify Wiki.js versions.
---

# Wiki.js Specialist Skill

This skill provides operational procedures for managing Wiki.js enterprise deployments, focusing on Git synchronization, GraphQL API automation, and rendering pipeline configuration.

## Scope and Triggers
- **Triggers:** User requests to configure Wiki.js Git storage, execute GraphQL mutations/queries, customize rendering (KaTeX, Mermaid), or verify instance versions.
- **Scope:** Wiki.js 2.x (specifically 2.5.314) administration and automation.
- **Non-goals:** General server administration, database tuning, or network routing outside of Wiki.js configuration.

## Preconditions
- Verify the target Wiki.js instance URL and authentication credentials (API token or admin login).
- Ensure the instance is running a supported version (2.5.314 is the current stable release).

## Source Freshness
- **Verified against upstream:** 2026-08-07
- **Primary Source:** Official Wiki.js documentation (docs.requarks.io).
- **Volatile Facts:** Current stable version is 2.5.314. Always verify the installed version before applying changes.

## Workflow
1. **Discover:** Query the Wiki.js GraphQL API or use `scripts/check-version.sh` to determine the current version and configuration.
2. **Validate:** Check the discovered version against the known stable release (2.5.314) and verify Git sync connectivity using `scripts/validate-git-sync.sh`.
3. **Plan:** Formulate the required GraphQL mutations or configuration changes based on the user's request. Consult `references/graphql-api.md` or `references/git-sync.md`.
4. **Confirm:** Present the planned changes to the user for approval, especially for destructive or bulk operations.
5. **Execute:** Apply the changes via the API or configuration files.
6. **Verify:** Query the API again to confirm the changes were applied successfully and check for any Git sync conflicts.
7. **Stop:** Terminate the workflow when the desired state is achieved and verified.

## Safety
- **Read-only first:** Always perform read-only discovery (e.g., querying versions or current config) before attempting mutations.
- **Confirmation required:** Explicit user confirmation is required before executing any GraphQL mutations that modify or delete pages, or before changing storage backend configurations.

## Validation
- Use `scripts/validate-git-sync.sh` to verify Git connectivity.
- Use `scripts/check-version.sh` to verify the instance version.

## Failure Handling
- If Git sync fails, check SSH keys and repository permissions.
- If GraphQL mutations fail, verify the API token permissions and query syntax.
- Do not repeat failed actions without modifying the approach based on error messages.

## Output Contract
- Provide a summary of actions taken, including the verified version, applied configurations, and any validation results.
- Include actionable next steps if errors occurred.

## Resources
- [Git Sync Reference](references/git-sync.md): Operational guide for Git storage synchronization.
- [GraphQL API Reference](references/graphql-api.md): Guide for authenticating and executing GraphQL operations.
- [Rendering Pipeline Reference](references/rendering-pipeline.md): Guide for customizing KaTeX, MathJax, Mermaid, etc.
- [Validate Git Sync Script](scripts/validate-git-sync.sh): Script to verify Git connectivity.
- [Check Version Script](scripts/check-version.sh): Script to verify the Wiki.js version.

## Cross-Skill Routing
- Route to `automation-and-scheduling` when the user requests recurring backups, scheduled syncs, or event-triggered Wiki.js updates.
- Route to `security-review` when the user requests a comprehensive security audit of the Wiki.js deployment infrastructure.
