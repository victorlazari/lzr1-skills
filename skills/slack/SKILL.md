---
name: slack
description: Comprehensive mastery of the Slack platform, including Block Kit composition, API integration, CLI usage, and advanced app architecture.
---

# Slack Master Specialist

This skill provides comprehensive mastery of the Slack platform, enabling the creation of production-grade Slack applications, advanced Block Kit UIs, robust API integrations, and complex workflows.

## When to Use

Use this skill when you need to:
- Build or update Slack applications (Bolt for Python/JS, Deno next-gen platform)
- Design and implement complex Block Kit interfaces (modals, App Home, rich messages)
- Integrate with Slack Web APIs (chat, conversations, users, views, files)
- Handle Slack events, interactions, and slash commands
- Implement advanced patterns like rate limiting, state management, and progressive updates
- Configure Slack app manifests and OAuth flows

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple channels to audit | Channel Auditor | Parallel analysis of channel history or membership |
| Multiple Block Kit views to design | UI Designer | Parallel creation of distinct modal or message layouts |
| Multiple API endpoints to integrate | API Integrator | Parallel implementation of different Slack API methods |
| Bulk user data processing | Data Processor | Parallel processing of user profiles or presence data |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Requirements Analysis**: Determine the type of Slack integration needed (bot, webhook, slash command, shortcut).
2. **Architecture Design**: Choose the appropriate framework (Bolt, Deno) and connection method (Socket Mode, Events API).
3. **UI/UX Design**: Design the Block Kit interfaces (messages, modals, App Home) using the appropriate block types and interactive elements.
4. **Implementation**:
   - Configure the app manifest (`manifest.yaml` or `manifest.ts`).
   - Implement event listeners, command handlers, and interaction handlers.
   - Integrate with external APIs or databases as needed.
5. **Testing & Validation**: Test the app locally using `slack run` or ngrok, ensuring all interactions and edge cases are handled.
6. **Deployment**: Deploy the app to production infrastructure and configure OAuth or token management.

## Core Principles

- **Acknowledge Quickly**: Always acknowledge interactions (`ack()`) within 3 seconds to prevent timeouts.
- **Progressive Disclosure**: Use modals and multi-step workflows to gather information without overwhelming the user.
- **State Management**: Use `private_metadata` in views or a dedicated database to maintain state across interactions.
- **Rate Limiting**: Respect Slack's tier-based rate limits to avoid being throttled.
- **Security**: Validate request signatures and use the principle of least privilege when requesting OAuth scopes.
- **Graceful Degradation**: Provide fallback text for messages with blocks to support older clients and notifications.

## Key References

- `references/complete-reference.md`: Comprehensive guide covering advanced patterns, CLI/API reference, configuration schemas, and deep dive architecture.
- `references/reading-list.md`: Curated list of books and articles for mastering Slack development.
