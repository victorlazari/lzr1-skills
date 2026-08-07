---
name: manus
description: Orchestrate Manus v2 agent pipelines, configure sandboxes, manage WebMCP browser automation, and integrate with the Manus Control Plane.
---

# Manus Specialist Skill

## Scope and Triggers

Use this skill when you need to architect, scale, secure, or troubleshoot complex solutions using the Manus autonomous agent platform. This includes:
- Orchestrating complex agent pipelines and parallel clusters using the v2 API.
- Configuring and troubleshooting sandboxed execution environments with network policies.
- Managing robust browser automation with WebMCP support.
- Integrating with the Manus Control Plane (MCP) for scheduling and state management.
- Handling complex file management, including S3 multipart uploads with CRC-64/NVME checksums.

**Cross-Skill Routing:**
- Route to `automation-and-scheduling` when the task involves automated execution, recurring execution, or background execution.
- Route to `persistent-computing` when the task requires persistent services, Docker, fixed IP, or heavy compute.

## Preconditions

Before acting, detect the target environment, required permissions, and user intent. Verify current upstream documentation for Manus v2 API and dependencies.

## Source Freshness

Volatile facts like API endpoints and supported versions are documented with a verification date (2026-08-07) in the reference file. Verify current upstream documentation before applying production-impacting actions.

## Workflow

1. Detect the target environment, required permissions, and user intent.
2. Verify current upstream documentation for Manus v2 API and dependencies.
3. Define the agent workflow (chained pipelines, event-driven, or parallel clusters) using the v2 API structure.
4. Configure the sandbox environment with appropriate isolation and network policies.
5. Set up browser automation with WebMCP support and robust waiting strategies.
6. Integrate with the Manus Control Plane (MCP) for scheduling and state management.
7. Execute the workflow, applying safety checks and requiring confirmation for destructive actions.
8. Validate the output against the expected contract and handle failures with retry logic or rollback.
9. Stop when the workflow completes successfully or a terminal error occurs.

## Safety

- Separate read-only discovery from mutations.
- Require confirmation for destructive, external, privileged, financial, legal, or production-impacting actions.
- Dry-run Kubernetes network policies.

## Validation

- Verify v2 API endpoint structures before execution.
- Validate Puppeteer scripts against version 25.5.0 compatibility.
- Ensure S3 multipart uploads specify CRC-64/NVME checksums.

## Failure Handling

Explain how to diagnose errors, choose alternatives, roll back, and avoid repeating a failed action unchanged.

## Output Contract

Specify the structure, evidence, severity/confidence, and actionable next steps expected in the result.

## Resources

- [Complete Reference](references/complete-reference.md): Detailed technical material, v2 API endpoints, WebMCP integration, and modern K8s/PostgreSQL practices.
- [Agent Pipeline Template](templates/agent-pipeline.json): Reusable, valid JSON template for chained agent pipelines using the v2 API structure.

## Orchestration

Use parallel work only for independent dimensions; define inputs, schemas, conflict handling, synthesis, and termination conditions.
