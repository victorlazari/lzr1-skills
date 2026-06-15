# Data Engineering

## Table of Contents
1. Pipeline Architecture
2. Orchestration
3. Batch Processing
4. Stream Processing
5. Data Storage
6. Data Integration

---

## 1. Pipeline Architecture

### Data Pipeline Patterns

| Pattern | Description | Use Case |
|---|---|---|
| ETL | Extract, Transform, Load | Legacy, pre-computed transforms |
| ELT | Extract, Load, Transform | Modern cloud warehouses |
| CDC | Change Data Capture | Real-time sync, event sourcing |
| Streaming | Continuous event processing | Real-time analytics, alerting |
| Reverse ETL | Warehouse → operational systems | Activate data in tools |
| Data Mesh | Domain-owned data products | Large organizations |

### ELT Architecture (Modern Stack)

```
Sources → Ingestion (Fivetran/Airbyte) → Raw Layer (Warehouse) → Transform (dbt) → Marts → BI/Analytics
```

### Pipeline Design Principles

- **Idempotency**: Re-running produces the same result (use MERGE, not INSERT)
- **Incremental processing**: Process only new/changed data when possible
- **Schema evolution**: Handle schema changes gracefully (add columns, type changes)
- **Data contracts**: Define and enforce schemas between producers and consumers
- **Observability**: Monitor freshness, volume, schema, and quality
- **Retry and recovery**: Handle transient failures with exponential backoff
- **Partitioning**: Partition by date/key for efficient incremental processing

---

## 2. Orchestration

### Orchestration Tools

| Tool | Type | Best For |
|---|---|---|
| Apache Airflow | DAG-based, Python | Complex workflows, mature ecosystem |
| Dagster | Asset-based, Python | Software-defined assets, testing |
| Prefect | Flow-based, Python | Modern, cloud-native |
| dbt Cloud | Transform-specific | dbt-centric workflows |
| Temporal | Workflow engine | Long-running, reliable workflows |
| Mage | Notebook-style | Data engineering, ML pipelines |

### Airflow Best Practices

```python
# DAG design principles
# 1. Keep DAGs simple and focused (one purpose per DAG)
# 2. Use TaskGroups for organization
# 3. Avoid heavy processing in DAG file (parsed frequently)
# 4. Use XCom sparingly (small metadata only)
# 5. Implement proper retry and alerting
# 6. Use dynamic task mapping for variable workloads

from airflow.decorators import dag, task
from datetime import datetime, timedelta

@dag(
    schedule="0 6 * * *",  # Daily at 6 AM
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
        "on_failure_callback": alert_on_failure,
    },
)
def daily_pipeline():
    @task
    def extract(): ...
    
    @task
    def transform(data): ...
    
    @task
    def load(transformed): ...
    
    raw = extract()
    transformed = transform(raw)
    load(transformed)
```

---

## 3. Batch Processing

### Batch Processing Frameworks

| Framework | Language | Best For |
|---|---|---|
| Apache Spark | Python/Scala/Java | Large-scale distributed processing |
| dbt | SQL | Warehouse transformations |
| Apache Beam | Python/Java | Unified batch + stream |
| Polars | Python/Rust | Single-node fast processing |
| DuckDB | SQL | Analytical queries on files |
| pandas | Python | Small-medium data exploration |

### Spark Best Practices

- Partition data appropriately (avoid too many small partitions)
- Use broadcast joins for small dimension tables
- Cache intermediate results that are reused
- Avoid UDFs when native functions exist (performance penalty)
- Monitor shuffle operations (expensive, often the bottleneck)
- Use adaptive query execution (AQE) in Spark 3+
- Write output in Parquet/Delta format with proper partitioning

### Incremental Processing Patterns

| Pattern | Description | Implementation |
|---|---|---|
| Append-only | Add new records | `WHERE created_at > last_run` |
| Merge/Upsert | Update existing + add new | `MERGE INTO ... USING ...` |
| Snapshot | Full state at point in time | Type 2 SCD |
| Partition overwrite | Replace entire partition | `INSERT OVERWRITE PARTITION` |

---

## 4. Stream Processing

### Stream Processing Frameworks

| Framework | Latency | Complexity | Best For |
|---|---|---|---|
| Apache Kafka Streams | Low | Medium | Kafka-native processing |
| Apache Flink | Very low | High | Complex event processing |
| Spark Structured Streaming | Medium | Medium | Batch + stream unified |
| Materialize | Very low | Low | Streaming SQL |
| ksqlDB | Low | Low | Kafka SQL interface |

### Streaming Concepts

| Concept | Description | Example |
|---|---|---|
| Event time vs Processing time | When event occurred vs when processed | Late-arriving data handling |
| Watermarks | Track event time progress | Allow for late data |
| Windows | Group events by time | Tumbling, sliding, session |
| Exactly-once | Process each event exactly once | Idempotent consumers + dedup |
| Backpressure | Handle producer faster than consumer | Buffer, drop, or slow producer |

### Kafka Architecture

```
Producers → Topics (partitioned) → Consumer Groups → Consumers
                    ↓
            Partition 0: [msg1, msg2, msg3, ...]
            Partition 1: [msg4, msg5, msg6, ...]
            Partition 2: [msg7, msg8, msg9, ...]
```

---

## 5. Data Storage

### Storage Layer Comparison

| Storage | Type | Best For |
|---|---|---|
| Snowflake | Cloud warehouse | Analytics, multi-cloud |
| BigQuery | Cloud warehouse | GCP-native, serverless |
| Redshift | Cloud warehouse | AWS-native |
| Databricks | Lakehouse | Unified analytics + ML |
| Delta Lake | Table format | ACID on data lake |
| Apache Iceberg | Table format | Open table format, time travel |
| Apache Hudi | Table format | Incremental processing |

### Data Lake vs Data Warehouse vs Lakehouse

| Aspect | Data Lake | Data Warehouse | Lakehouse |
|---|---|---|---|
| Storage | Object storage (cheap) | Proprietary (expensive) | Object storage (cheap) |
| Format | Any (raw files) | Structured (tables) | Open table formats |
| Schema | Schema-on-read | Schema-on-write | Both |
| ACID | No | Yes | Yes (Delta/Iceberg) |
| Performance | Variable | Optimized | Optimized |
| Cost | Low storage | High compute + storage | Low storage, pay-per-query |
| Use case | Raw data, ML | BI, reporting | Unified analytics |

### File Formats

| Format | Type | Best For |
|---|---|---|
| Parquet | Columnar, compressed | Analytics, data warehouse |
| ORC | Columnar, compressed | Hive ecosystem |
| Avro | Row-based, schema evolution | Streaming, Kafka |
| JSON/JSONL | Semi-structured | APIs, logs, flexibility |
| CSV | Row-based, universal | Data exchange, simple |
| Delta/Iceberg | Table format (Parquet+metadata) | ACID, time travel |

---

## 6. Data Integration

### Ingestion Tools

| Tool | Type | Best For |
|---|---|---|
| Fivetran | Managed EL | SaaS connectors, low maintenance |
| Airbyte | Open-source EL | Self-hosted, custom connectors |
| Stitch | Managed EL | Simple, affordable |
| Debezium | CDC | Database change capture |
| Apache NiFi | Data flow | Complex routing, enterprise |
| Singer | Open-source EL | Tap/target ecosystem |

### CDC (Change Data Capture)

```
Database → WAL/Binlog → Debezium → Kafka → Stream Processing → Target
```

**Benefits**: Real-time sync, minimal source impact, complete change history.

**Implementation**:
- PostgreSQL: Logical replication slots + Debezium
- MySQL: Binlog + Debezium
- MongoDB: Change Streams
- DynamoDB: DynamoDB Streams

### Data Contracts

```yaml
# data_contract.yaml
name: orders
version: 2.1.0
owner: commerce-team
description: Order events from the e-commerce platform
schema:
  fields:
    - name: order_id
      type: string
      required: true
      description: Unique order identifier
    - name: total_amount
      type: decimal
      required: true
      constraints:
        minimum: 0
    - name: created_at
      type: timestamp
      required: true
quality:
  freshness: 1 hour
  completeness: 99.5%
  uniqueness: order_id
```
