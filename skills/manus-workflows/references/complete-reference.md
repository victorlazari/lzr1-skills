# n8n Workflows: Complete Expert Reference

Verified against upstream: 2026-08-07

## 1. Introduction to n8n Workflows

n8n is an advanced orchestration framework designed to facilitate complex business process automation across distributed systems. It provides a robust platform for defining, executing, and monitoring workflows that span multiple services and technologies.

## 2. Architecture Overview

n8n is built on a node-based architecture, ensuring scalability and flexibility.

### Core Components
- **Workflow Engine**: The central orchestrator that interprets workflow definitions, manages state transitions, and schedules tasks.
- **Nodes**: Stateless, independently deployable units that perform specific operations (e.g., API calls, data transformation).
- **Execution Modes**:
  - **Main Mode**: Standard execution mode for single-instance deployments.
  - **Queue Mode**: Distributed execution mode using Redis for scaling across multiple workers.

## 3. Task Planning and Management

Workflows are conceptualized as Directed Acyclic Graphs (DAGs) of nodes.

### Execution Flow
- **Sequential**: Nodes execute one after another based on connections.
- **Parallel**: Independent nodes execute simultaneously.
- **Conditional**: Branching logic based on runtime data (e.g., Switch node, IF node).

## 4. Message Communication

Inter-task and inter-system communication is message-driven.

### Protocols and Patterns
- **Webhooks**: Trigger workflows via external HTTP POST requests with authentication.
- **Reliability**: Utilizes error handling nodes and retries.

## 5. File Operations and Search

### File Handling
- Supports read, write, stream, upload, and download operations via specific nodes.
- Integrates with cloud storage (AWS S3, Google Cloud Storage).

## 6. Scheduling

Automates time-based workflows.

### Features
- **Cron Expressions**: Standard syntax for recurring schedules via the Cron node.
- **Intervals**: Fixed time gaps between executions via the Interval node.

## 7. Multi-Tool Orchestration

Integrates diverse systems into cohesive workflows.

### Connectors
- Pre-built nodes for hundreds of services.
- Custom API calls via the HTTP Request node.

## 8. Configuration Schemas

Configuration is managed via environment variables.

### Key Variables
- `N8N_ENCRYPTION_KEY`: Secures credentials.
- `EXECUTIONS_MODE`: Sets main or queue mode.

## 9. Troubleshooting and Diagnostics

### Diagnostic Tools
- **Execution Logs**: View detailed logs of each node's execution in the n8n UI.
- **Error Trigger Node**: Catch and handle workflow errors gracefully.
