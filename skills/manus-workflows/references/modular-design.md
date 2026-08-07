# Modular Workflow Design in n8n

Verified against upstream: 2026-08-07

## Sub-Workflows

n8n supports modular design through the use of sub-workflows. This allows you to break down complex processes into smaller, reusable components.

### Execute Workflow Node

Use the **Execute Workflow** node to call another workflow from within a parent workflow. This promotes reusability and simplifies maintenance.

### Benefits of Modularity

- **Reusability**: Common tasks (e.g., error handling, notifications) can be defined once and reused across multiple workflows.
- **Maintainability**: Smaller workflows are easier to understand, test, and debug.
- **Collaboration**: Different team members can work on separate sub-workflows simultaneously.

### Best Practices

- **Clear Interfaces**: Define clear inputs and outputs for sub-workflows to ensure they can be easily integrated.
- **Error Handling**: Implement robust error handling within sub-workflows to prevent failures from cascading to the parent workflow.
