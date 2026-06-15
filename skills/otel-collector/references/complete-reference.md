# OpenTelemetry Collector: The Complete Reference

The OpenTelemetry (OTel) Collector is a vendor-agnostic proxy that receives, processes, and exports telemetry data (traces, metrics, logs). It removes the need to run, operate, and maintain multiple agents/collectors. This comprehensive reference consolidates advanced patterns, configuration schemas, CLI usage, and deep-dive architecture for production environments.

## 1. Architecture Internals

The OpenTelemetry Collector is written in Go and operates as a pipeline for telemetry data.

### 1.1 Service Startup and Pipeline Construction

When the Collector starts, it initializes components and constructs the telemetry pipeline:

1.  **Configuration Resolution**: Reads configuration from sources (file, env, HTTP) using the `confmap` package (Providers, Converters, Resolver).
2.  **Component Initialization**: Initializes extensions, receivers, processors, exporters, and connectors.
3.  **Pipeline Graph Construction**: Constructs a Directed Acyclic Graph (DAG) representing the pipelines.
4.  **Component Lifecycle**: Starts components in order: Extensions -> Exporters -> Processors -> Receivers.

### 1.2 Data Flow (pdata types)

Telemetry data flows through pipelines using internal `pdata` structures:
-   `pcommon`: Common structures (attributes, resources).
-   `ptrace`: Trace data (spans, events).
-   `pmetric`: Metric data (data points).
-   `plog`: Log data (records).

### 1.3 Memory Management

Proper memory management is crucial to prevent Out-Of-Memory (OOM) kills:
-   **`GOMEMLIMIT`**: Set this environment variable to ~80% of the container's hard memory limit.
-   **`memory_limiter` Processor**: MUST be the first processor in every pipeline. It drops data when memory limits are approached.

## 2. OpenTelemetry Transformation Language (OTTL)

OTTL is a domain-specific language for transforming telemetry data within the Collector (used in `transform`, `filter`, `tailsampling` processors, and `routing` connector).

### 2.1 OTTL Contexts

| Context | Description | Available Fields |
| :--- | :--- | :--- |
| `resource` | Operates on Resource attributes. | `attributes`, `dropped_attributes_count` |
| `scope` | Operates on Instrumentation Scope. | `name`, `version`, `attributes` |
| `span` | Operates on individual Spans. | `trace_id`, `span_id`, `name`, `attributes`, `status` |
| `spanevent` | Operates on Span Events. | `time_unix_nano`, `name`, `attributes` |
| `metric` | Operates on Metrics (metadata). | `name`, `description`, `unit`, `type` |
| `datapoint` | Operates on Metric Data Points. | `attributes`, `value_double`, `value_int` |
| `log` | Operates on Log Records. | `severity_text`, `body`, `attributes`, `trace_id` |

### 2.2 Key OTTL Functions

-   **Modification**: `set(target, value)`, `delete_key(target, key)`, `keep_keys(target, keys[])`, `replace_pattern(target, regex, replacement)`, `merge_maps(target, source, strategy)`.
-   **Hashing**: `fnv(target)`, `sha256(target)`.
-   **Evaluation**: `IsMatch(target, regex)`, `Int(target)`, `String(target)`.
-   **String**: `Concat(values[], separator)`, `Split(target, separator)`, `Substring(target, start, length)`.
-   **Parsing**: `ParseJSON(target)`, `ExtractPatterns(target, regex)`.

## 3. Scaling Patterns

### 3.1 Stateless Scaling

Applies when the Collector performs stateless operations (filtering, transformation, batching).
-   **Architecture**: Multiple replicas behind a load balancer.
-   **Load Balancing**: L7 load balancer (Envoy, HAProxy) is REQUIRED for gRPC to balance streams.
-   **Trigger**: Scale when `otelcol_exporter_queue_size` reaches 60-70% capacity.

### 3.2 Scrapers (Target Allocator)

Used for scraping Prometheus metrics at scale.
-   **Architecture**: OpenTelemetry Operator with Target Allocator.
-   **How it works**: Target Allocator discovers targets and shards them across a StatefulSet of Collectors.

### 3.3 Stateful Scaling (Consistent Hashing)

Required for stateful operations (Tail Sampling, Span-to-Metrics).
-   **Architecture**: Two-tier. Tier 1 (Stateless) receives traffic and uses `loadbalancing` exporter to route data to Tier 2 (Stateful) based on a consistent hash (e.g., `trace_id`).

## 4. Connector Patterns

Connectors bridge two pipelines, acting as both exporter and receiver.

-   **Routing Connector**: Routes telemetry based on OTTL conditions.
-   **Spanmetrics Connector**: Generates RED (Request, Error, Duration) metrics from spans (Stateful).
-   **Servicegraph Connector**: Generates service dependency graphs from spans (Stateful).
-   **Count Connector**: Counts telemetry items and emits a metric.
-   **Failover Connector**: Provides high availability by falling back to secondary pipelines if the primary fails.

## 5. Custom Collector Building (OCB)

The OpenTelemetry Collector Builder (OCB) generates a custom binary containing only needed components.

### 5.1 Manifest (`builder-config.yaml`)

```yaml
dist:
  name: custom-otelcol
  output_path: ./dist
  otelcol_version: 0.95.0

receivers:
  - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.95.0

processors:
  - gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.95.0
  - gomod: go.opentelemetry.io/collector/processor/memorylimiterprocessor v0.95.0

exporters:
  - gomod: go.opentelemetry.io/collector/exporter/otlpexporter v0.95.0
```

### 5.2 Building

Run `./ocb --config builder-config.yaml` to generate source code and compile the binary.

## 6. Configuration Schemas

### 6.1 Top-Level Structure

```yaml
receivers: {}   # How data gets in
processors: {}  # What happens to data
exporters: {}   # Where data goes
connectors: {}  # Bridge pipelines
extensions: {}  # Auxiliary capabilities
service:        # Ties everything together
  extensions: []
  telemetry: {}
  pipelines:
    traces: {}
    metrics: {}
    logs: {}
```

### 6.2 Essential Processors

-   **Memory Limiter**: MUST be first. `limit_percentage: 80`, `spike_limit_percentage: 20`.
-   **Batch**: Groups data. `send_batch_size: 8192`, `timeout: 1s`.

## 7. CLI Reference

-   **Start**: `otelcol --config config.yaml`
-   **Overrides**: `otelcol --config config.yaml --set "exporters::otlp::endpoint=0.0.0.0:4317"`
-   **Validate**: `otelcol validate --config config.yaml`
-   **List Components**: `otelcol components`

## 8. Troubleshooting

### 8.1 Diagnostic Tools

-   **zPages**: Extension for internal pipeline metrics and trace latency (`/debug/tracez`).
-   **pprof**: Extension for Go profiling (CPU, memory).
-   **Debug Exporter**: Exporter with `verbosity: detailed` to print payloads.

### 8.2 Common Issues

| Symptom | Root Cause | Resolution |
| :--- | :--- | :--- |
| **Data Dropped (Queue Full)** | Backend is slow/unreachable. | Check backend health. Increase `queue_size`. Scale Collector (if stateless). |
| **OOM Kills** | Memory spike exceeded limits. | Set `GOMEMLIMIT`. Ensure `memory_limiter` is first processor. |
| **Transformations Not Applied** | Incorrect OTTL or processor not in pipeline. | Verify pipeline config. Use `debug` exporter to inspect payload. |
| **Collector Fails to Start** | Invalid YAML or missing component. | Run `otelcol validate`. Check startup logs. |

## 9. Kubernetes Deployment

Deploy using the official Helm charts or the OpenTelemetry Operator.

-   **Operator CRD**: Manages `OpenTelemetryCollector` and `Instrumentation` (auto-instrumentation) resources.
-   **Sidecar Injection**: Use annotation `sidecar.opentelemetry.io/inject: "true"` on Pods.

---
*Author: Manus AI*
AI*
Date: June 2026*
