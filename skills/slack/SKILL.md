---
name: slack
description: Comprehensive mastery of the Slack platform, including Block Kit composition (Card, Alert, Carousel, Data Table, Work Object, Code), API integration, CLI usage, and advanced app architecture.
---

# Slack Master Specialist

This skill provides comprehensive mastery of the Slack platform, enabling the creation of production-grade Slack applications, advanced Block Kit UIs for agent experiences, robust API integrations, and complex workflows.

## Scope and Triggers

Use this skill when you need to:
- Build or update Slack applications (Bolt for Python/JS, Deno next-gen platform)
- Design and implement complex Block Kit interfaces, especially using new agent experience components (Card, Alert, Carousel, Data Table, Work Object, Code)
- Integrate with Slack Web APIs (chat, conversations, users, views, files)
- Handle Slack events, interactions, and slash commands
- Implement advanced patterns like rate limiting, state management, and progressive updates
- Configure Slack app manifests and OAuth flows

## Preconditions

- Detect the target Slack workspace and environment.
- Verify required permissions and OAuth scopes.
- Identify the appropriate framework (Bolt, Deno) and connection method (Socket Mode, Events API).

## Source Freshness

- Volatile facts (e.g., API rate limits, Block Kit schemas) must be verified against official current documentation.
- Check `references/block-kit-components.md` and `references/api-reference.md` for verified patterns.
- Verified against upstream: 2026-08-07.

## Workflow

1. **Requirements Analysis**: Determine the type of Slack integration needed (bot, webhook, slash command, shortcut) and required OAuth scopes.
2. **Architecture Design**: Choose the appropriate framework (Bolt, Deno) and connection method (Socket Mode, Events API).
3. **UI/UX Design**: Design the Block Kit interfaces using the latest components (Card, Alert, Carousel, Data Table, Work Object, Code) for structured, interactive agent experiences instead of static text.
4. **Validation**: Validate the Block Kit JSON design against the official schema using `scripts/validate-block-kit.sh`.
5. **Implementation**:
   - Configure the app manifest.
   - Implement event listeners, command handlers, and interaction handlers.
   - Integrate with external APIs or databases as needed.
6. **Testing & Validation**: Test the app locally using `slack run` or ngrok, verifying interactions and edge cases.
7. **Deployment**: Deploy the app, ensuring request signature validation and secure token management are in place.

## Safety

- Separate read-only discovery from mutations.
- Require confirmation before sending messages to large channels or `@channel`.
- Verify request signatures for all incoming webhooks/events.
- Use the principle of least privilege for OAuth scopes.

## Validation

- Validate all Block Kit JSON payloads against the official schema before sending.
- Run safe local syntax checks on scripts and configurations.

## Failure Handling

- Diagnose errors using `references/troubleshooting.md`.
- Choose alternatives or roll back if an action fails.
- Do not repeat a failed action unchanged.

## Output Contract

- The result must include the implemented code, configuration, or Block Kit JSON.
- Provide evidence of successful validation or testing.
- Specify actionable next steps for deployment or further integration.

## Resources

- `references/block-kit-components.md`: Detailed documentation and JSON examples for the new Block Kit components.
- `references/api-reference.md`: Focused reference for essential Slack Web API methods.
- `references/security-patterns.md`: Guidelines for request signature validation, OAuth scopes, and token management.
- `references/troubleshooting.md`: Diagnostic commands and common failure modes.
- `scripts/validate-block-kit.sh`: A script to validate Block Kit JSON payloads against the official schema.

## Orchestration

- Use parallel work only for independent dimensions (e.g., auditing multiple channels, integrating multiple API endpoints).
- Define inputs, schemas, conflict handling, synthesis, and termination conditions for parallel tasks.
