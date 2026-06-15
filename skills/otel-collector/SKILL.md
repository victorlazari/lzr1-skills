---
name: otel-collector
description: "Expertise in OpenTelemetry Collector advanced patterns, OTTL, scaling, connector patterns, and custom builds."
---

# OpenTelemetry Collector Skill

## When to Use

Use this skill when you need to:
- Configure, deploy, or troubleshoot the OpenTelemetry (OTel) Collector in production environments.
- Write or debug OpenTelemetry Transformation Language (OTTL) statements for processors and connectors.
- Design scaling architectures for the Collector (Stateless, Scrapers, Stateful).
- Implement connector patterns (Routing, Spanmetrics, Servicegraph, Count, Failover).
- Build custom Collector binaries using the OpenTelemetry Collector Builder (OCB).
- Manage memory, diagnose OOM kills, and configure internal telemetry (zPages, pprof).
- Deploy the Collector on Kubernetes using Helm or the OpenTelemetry Operator.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple pipelines to configure | Pipeline Architect | Parallel design and configuration of traces, metrics, and logs pipelines |
| Multiple OTTL transformations to write | OTTL Specialist | Parallel creation and testing of OTTL statements for different contexts |
| Multiple environments to deploy | Deployment Engineer | Parallel deployment of the Collector across dev, staging, and prod |
| Bulk troubleshooting of dropped data | Diagnostics Agent | Parallel investigation of exporter queues, backpressure, and memory limits |

### Spawning Rules
- Spawn when 3+ independent items need the same operation (e.g., 3+ pipelines, 3+ environments).
- Each sub-agent receives: context (e.g., overall architecture), specific target (e.g., traces pipeline), success criteria (e.g., valid YAML config).
- Results are aggregated and cross-referenced for conflicts (e.g., port conflicts, resource limits).
- Maximum concurrent sub-agents: 10

## Workflow

1.  **Requirement Analysis**: Determine the telemetry signals (traces, metrics, logs) to collect, process, and export. Identify the source and destination backends.
2.  **Architecture Design**: Choose the appropriate scaling pattern (Stateless, Scrapers, Stateful) based on the processing requirements (e.g., tail sampling requires stateful).
3.  **Configuration Development**:
    - Define receivers to ingest data.
    - Configure processors (always start with `memory_limiter` and `batch`).
    - Write OTTL statements for `transform` or `filter` processors if data manipulation is needed.
    - Define exporters to send data to backends.
    - Use connectors to bridge pipelines if necessary.
4.  **Custom Build (Optional)**: If specific components are needed or to reduce binary size, create a `builder-config.yaml` and use OCB to build a custom binary.
5.  **Deployment**: Deploy the Collector using Docker, systemd, Helm, or the OpenTelemetry Operator. Ensure proper memory limits (`GOMEMLIMIT`) and resource requests/limits are set.
6.  **Validation and Troubleshooting**: Use `otelcol validate`, `telemetrygen`, and internal telemetry (zPages, pprof, debug exporter) to verify the pipeline and troubleshoot issues like OOM kills or dropped data.

## Core Principles

-   **Memory Management is Critical**: Always use the `memory_limiter` processor as the first processor in every pipeline. Set the `GOMEMLIMIT` environment variable to ~80% of the container's hard memory limit.
-   **Batching for Performance**: Always use the `batch` processor to group telemetry data before exporting. This reduces network overhead and improves backend performance.
-   **Order Matters**: The order of processors in a pipeline is significant. For example, `memory_limiter` must come before `batch`.
-   **Stateful Processing Requires Consistent Hashing**: Operations like tail sampling or span-to-metrics generation require all data for a specific trace to be processed by the same Collector instance. Use a two-tier architecture with a `loadbalancing` exporter.
-   **Security First**: Never run the Collector as root. Use encrypted connections (TLS) for receivers and exporters. Do not expose internal endpoints (health, pprof, zpages) externally.

## Key References

-   `references/complete-reference.md`: Comprehensive guide on OTTL, scaling, connectors, OCB, CLI commands, configuration schemas, and deep-dive architecture.
-   `references/reading-list.md`: Curated list of books and articles for further learning on OpenTelemetry and observability.
