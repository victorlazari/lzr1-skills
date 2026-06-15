# Data Governance

## Table of Contents
1. Data Quality
2. Data Lineage
3. Data Catalog
4. Data Privacy
5. Governance Framework

---

## 1. Data Quality

### Data Quality Dimensions

| Dimension | Description | Measurement |
|---|---|---|
| Completeness | No missing values | % non-null for required fields |
| Accuracy | Values are correct | Comparison to source of truth |
| Consistency | Same value across systems | Cross-system reconciliation |
| Timeliness | Data is fresh enough | Lag from event to availability |
| Uniqueness | No duplicates | Duplicate rate on key fields |
| Validity | Values conform to rules | % passing validation rules |

### Data Quality Tools

| Tool | Type | Best For |
|---|---|---|
| Great Expectations | Open-source, Python | Programmable data validation |
| dbt tests | Built into dbt | Transform-time validation |
| Soda | Open-source + cloud | SQL-based checks, monitoring |
| Monte Carlo | Managed | Data observability platform |
| Elementary | dbt-native | dbt data observability |
| Datafold | Managed | Data diff, regression testing |

### Data Quality Monitoring

```yaml
# Great Expectations example
expectations:
  - expect_column_values_to_not_be_null:
      column: order_id
  - expect_column_values_to_be_unique:
      column: order_id
  - expect_column_values_to_be_between:
      column: amount
      min_value: 0
      max_value: 1000000
  - expect_table_row_count_to_be_between:
      min_value: 1000    # Alert if too few rows (data loss)
      max_value: 1000000 # Alert if too many (duplication)
  - expect_column_values_to_match_regex:
      column: email
      regex: "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
```

---

## 2. Data Lineage

### Lineage Types

| Type | Scope | Purpose |
|---|---|---|
| Column-level | Individual fields | Impact analysis, debugging |
| Table-level | Table dependencies | Pipeline understanding |
| Pipeline-level | End-to-end flow | Architecture documentation |
| Business-level | Metric to source | Trust and transparency |

### Lineage Tools

| Tool | Integration | Features |
|---|---|---|
| dbt docs | dbt-native | DAG visualization, column lineage |
| OpenLineage | Standard/API | Open standard for lineage |
| DataHub | Universal | Catalog + lineage + governance |
| Atlan | Managed | Active metadata, collaboration |
| Marquez | Open-source | OpenLineage-compatible |

---

## 3. Data Catalog

### Catalog Components

| Component | Purpose | Example |
|---|---|---|
| Technical metadata | Schema, types, stats | Column names, row counts |
| Business metadata | Descriptions, owners | "This table contains..." |
| Operational metadata | Freshness, quality | Last updated, test results |
| Social metadata | Usage, popularity | Query frequency, users |
| Lineage | Dependencies | Upstream/downstream |

### Data Catalog Tools

| Tool | Type | Best For |
|---|---|---|
| DataHub | Open-source | Comprehensive, extensible |
| Atlan | Managed | Modern, collaborative |
| Alation | Enterprise | Large organizations |
| dbt docs | dbt-native | dbt project documentation |
| Amundsen | Open-source | Discovery-focused |
| OpenMetadata | Open-source | Standards-based |

---

## 4. Data Privacy

### Privacy Techniques

| Technique | Description | Use Case |
|---|---|---|
| Anonymization | Remove identifying information | Analytics on sensitive data |
| Pseudonymization | Replace identifiers with tokens | Reversible de-identification |
| Masking | Hide partial values | Display (****1234) |
| Tokenization | Replace with random token | Payment data |
| Aggregation | Group-level only | Reporting without individual data |
| Differential privacy | Add noise to query results | Statistical queries on sensitive data |

### Data Classification

| Level | Description | Handling |
|---|---|---|
| Public | No restriction | Open access |
| Internal | Business use only | Employee access |
| Confidential | Restricted access | Need-to-know, encrypted |
| Restricted | Highly sensitive (PII, financial) | Strict controls, audit trail |

---

## 5. Governance Framework

### Data Ownership Model

| Role | Responsibility | Example |
|---|---|---|
| Data Owner | Accountable for data asset | VP of Sales owns CRM data |
| Data Steward | Day-to-day quality management | Analytics engineer |
| Data Producer | Creates/maintains data | Backend team (events) |
| Data Consumer | Uses data for decisions | Marketing analyst |
| Data Platform | Infrastructure and tooling | Data engineering team |

### Governance Maturity Levels

| Level | Description | Characteristics |
|---|---|---|
| 1 - Initial | Ad hoc, tribal knowledge | No documentation, manual processes |
| 2 - Managed | Some documentation | Defined owners, basic catalog |
| 3 - Defined | Standardized processes | Quality checks, lineage, policies |
| 4 - Measured | Metrics-driven | SLAs, quality scores, compliance |
| 5 - Optimized | Continuous improvement | Automated governance, self-service |
