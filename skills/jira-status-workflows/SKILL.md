---
name: jira-status-workflows
description: Advanced Jira workflow configuration, complex state management, ITSM integration, and troubleshooting.
---

# Jira Status & Workflows

## Scope and Triggers
Use this skill when you need to:
- Design or audit complex Jira workflow state machines.
- Configure workflow transitions, conditions, validators, and post-functions.
- Implement advanced workflow properties (e.g., `jira.issue.editable`).
- Integrate ScriptRunner (HAPI) or Jira Automation into workflow transitions.

**Cross-Skill Routing:**
- `jira-jql-search`: Route when the task requires querying issues rather than modifying workflow configurations.
- `jira-automation-rules`: Route when the task focuses purely on Jira Automation rules rather than core workflow state machines.
- `jira-project-admin`: Route when the task involves project-level settings (screens, fields, permissions) outside of workflow schemes.

## Preconditions
- Identify the target project type (Software vs. JSM) and required states.
- Verify user permissions, current workflow scheme, and required add-ons (e.g., ScriptRunner).

## Source Freshness
- Verify current upstream documentation for volatile facts, such as ScriptRunner API changes or Jira Cloud workflow properties, before applying destructive or production-impacting actions.
- See `references/complete-reference.md` for authoritative sources.

## Workflow
1. **Analyze requirements:** Identify the target project type (Software vs. JSM) and required states.
2. **Verify preconditions:** Check user permissions, current workflow scheme, and required add-ons (e.g., ScriptRunner).
3. **Design state machine:** Map statuses, categories, and transitions (local, global, loop).
4. **Configure rules:** Define conditions, validators, post-functions, and workflow properties (e.g., `jira.issue.editable`).
5. **Implement scripting:** Use ScriptRunner (HAPI) or Jira Automation for complex logic, ensuring dry-runs are tested.
6. **Validate configuration:** Run `scripts/validate-workflow-schema.py` to check schema integrity.
7. **Deploy and monitor:** Apply the workflow scheme, capture evidence of successful transitions, and halt if errors occur.

## Safety
- Require explicit user confirmation before deploying workflow scheme changes or executing mutating scripts.
- Use dry-run modes for all custom scripts and automation rules.
- Validate workflow JSON/XML schemas locally before uploading.
- Verify user permissions and separation of duties (SoD) constraints prior to transitions.
- Capture pre- and post-transition states for rollback purposes.
- Log all script execution errors and halt on failure.

## Validation
- Run `scripts/validate-workflow-schema.py` to check schema integrity.
- Verify user permissions and separation of duties (SoD) constraints prior to transitions.
- Capture pre- and post-transition states for rollback purposes.

## Failure Handling
- Log all script execution errors and halt on failure.
- If a transition fails, capture the error message and current state.
- Do not repeat a failed action unchanged.

## Output Contract
- A clear summary of the workflow changes made.
- Evidence of successful transitions or schema validation.
- Any errors encountered and the resulting state.

## Resources
- `references/complete-reference.md`: Detailed technical reference on workflow properties and ScriptRunner HAPI.
- `scripts/validate-workflow-schema.py`: Deterministic script to validate Jira workflow JSON/XML schemas against known structures.
- `templates/workflow-audit-report.md`: Reusable template for documenting workflow audit findings, including contradictions and confidence levels.
