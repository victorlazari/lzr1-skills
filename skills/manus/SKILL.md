---
name: manus
description: Mastering Manus Autonomous Agent Platform, Sandbox Environments, Browser Automation, Web Development Scaffolds, MCP Integration, File Management, and Scheduling
---

# Manus Specialist Skill

## When to Use

Use this skill when you need to architect, scale, secure, or troubleshoot complex solutions using the Manus autonomous agent platform. This includes:
- Orchestrating complex agent pipelines and parallel clusters.
- Configuring and troubleshooting sandboxed execution environments.
- Managing robust browser automation at scale.
- Building and extending web development scaffolds (frontend and backend).
- Integrating with the Manus Control Plane (MCP) for scheduling and state management.
- Handling complex file management and synchronization patterns.
- Diagnosing and resolving agent execution, connectivity, and automation failures.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple agents in a pipeline | Pipeline Orchestrator | Parallel execution of independent pipeline stages |
| High-throughput browser automation | Browser Automation Agent | Parallel scraping or interaction across multiple URLs |
| Bulk file processing/transfer | File Management Agent | Parallel chunk uploads or delta synchronization |
| Distributed health checks | Diagnostics Agent | Parallel monitoring of MCP components and sandboxes |

### Spawning Rules
- Spawn when 3+ independent items need the same operation (e.g., scraping multiple sites, processing multiple files).
- Each sub-agent receives: context, specific target (e.g., URL, file chunk), success criteria.
- Results are aggregated and cross-referenced for conflicts or errors.
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Architecture & Orchestration**: Define the agent workflow (chained pipelines, event-driven, or parallel clusters).
2. **Sandbox Configuration**: Set up isolation mechanisms (namespaces, cgroups) and fine-grained permissions (filesystem whitelisting, network policies).
3. **Browser Automation Setup**: Implement browser pooling, session isolation, and robust waiting strategies for dynamic content.
4. **Web Scaffold Integration**: Extend frontend dashboards and backend APIs, integrating with MCP for event handling.
5. **MCP & Scheduling**: Configure cron-like schedules, dependency scheduling, and retry policies. Ensure MCP components are scaled horizontally.
6. **File Management**: Set up volume mounts, object storage integration, and secure file transfer mechanisms.
7. **Troubleshooting**: Monitor logs, metrics, and traces to diagnose execution failures, connectivity issues, or automation errors.

## Core Principles

- **Security First**: Enforce strict sandbox isolation, capability dropping, and secure credential injection.
- **Scalability**: Utilize horizontal scaling for MCP components and parallel agent clusters for high throughput.
- **Resilience**: Implement retry logic, dead letter queues, and high availability configurations to handle transient failures.
- **Efficiency**: Optimize resource utilization through browser pooling, lazy initialization, and incremental file synchronization.
- **Observability**: Maintain comprehensive logging, metrics collection, and tracing for rapid troubleshooting.

## Key References

- [Manus Platform Official Documentation](https://docs.manus-platform.io)
- [Manus GitHub Repository](https://github.com/manus-platform)
- [Puppeteer Documentation](https://pptr.dev)
- [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [PostgreSQL Clustering Best Practices](https://www.postgresql.org/docs/current/high-availability.html)
- [AWS S3 Multipart Upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html)
