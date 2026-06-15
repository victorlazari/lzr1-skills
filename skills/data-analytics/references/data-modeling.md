# Data Modeling

## Table of Contents
1. Dimensional Modeling
2. Data Vault
3. dbt (Data Build Tool)
4. Metrics Layer
5. Schema Design Patterns

---

## 1. Dimensional Modeling

### Star Schema

```
           ┌──────────────┐
           │  dim_product  │
           └──────┬───────┘
                  │
┌──────────┐     │     ┌──────────────┐
│ dim_date │─────┼─────│ fact_sales    │
└──────────┘     │     └──────┬───────┘
                  │            │
           ┌──────┴───────┐   │
           │ dim_customer  │──┘
           └──────────────┘
```

### Fact Table Types

| Type | Description | Example |
|---|---|---|
| Transaction | One row per event | Order placed, payment received |
| Periodic snapshot | One row per period | Daily account balance |
| Accumulating snapshot | One row per lifecycle | Order: placed → shipped → delivered |
| Factless fact | Records events without measures | Student attendance, product views |

### Dimension Types (Slowly Changing Dimensions)

| Type | Strategy | Use Case |
|---|---|---|
| Type 0 | Never change | Reference data (country codes) |
| Type 1 | Overwrite | Current state only needed |
| Type 2 | Add new row (versioned) | Full history needed |
| Type 3 | Add column (previous value) | Limited history (current + previous) |
| Type 6 | Hybrid (1+2+3) | Current + history + previous |

### Naming Conventions

| Object | Convention | Example |
|---|---|---|
| Fact tables | `fct_` or `fact_` prefix | `fct_orders`, `fct_page_views` |
| Dimension tables | `dim_` prefix | `dim_customer`, `dim_product` |
| Staging models | `stg_` prefix | `stg_stripe__payments` |
| Intermediate | `int_` prefix | `int_orders_pivoted` |
| Marts | `mart_` or domain prefix | `mart_finance`, `mart_marketing` |

---

## 2. Data Vault

### Data Vault Components

| Component | Purpose | Structure |
|---|---|---|
| Hub | Business keys | Hash key, business key, load date, source |
| Link | Relationships | Hash key, hub references, load date, source |
| Satellite | Descriptive attributes | Hash key, parent key, attributes, load date |

### When to Use Data Vault

- Enterprise-scale data warehouses
- Multiple source systems with overlapping entities
- Need for full auditability and traceability
- Agile/incremental loading requirements
- Historical tracking of all changes

---

## 3. dbt (Data Build Tool)

### dbt Project Structure

```
dbt_project/
├── dbt_project.yml          # Project configuration
├── models/
│   ├── staging/             # Source-conformed models (1:1 with source)
│   │   ├── stripe/
│   │   │   ├── _stripe__models.yml
│   │   │   ├── stg_stripe__payments.sql
│   │   │   └── stg_stripe__customers.sql
│   │   └── shopify/
│   │       └── ...
│   ├── intermediate/        # Business logic transformations
│   │   └── int_orders_enriched.sql
│   └── marts/               # Business-facing models
│       ├── finance/
│       │   └── fct_revenue.sql
│       └── marketing/
│           └── dim_customers.sql
├── tests/                   # Custom data tests
├── macros/                  # Reusable SQL functions
├── seeds/                   # Static reference data (CSV)
└── snapshots/               # SCD Type 2 tracking
```

### dbt Model Patterns

```sql
-- staging model: clean and rename source data
-- stg_stripe__payments.sql
WITH source AS (
    SELECT * FROM {{ source('stripe', 'payments') }}
),
renamed AS (
    SELECT
        id AS payment_id,
        amount / 100.0 AS amount_usd,  -- cents to dollars
        status,
        created AS created_at,
        customer_id
    FROM source
    WHERE status != 'failed'  -- filter invalid records
)
SELECT * FROM renamed

-- mart model: business logic and joins
-- fct_orders.sql
WITH orders AS (
    SELECT * FROM {{ ref('stg_shopify__orders') }}
),
payments AS (
    SELECT * FROM {{ ref('stg_stripe__payments') }}
),
final AS (
    SELECT
        orders.order_id,
        orders.customer_id,
        orders.order_date,
        payments.amount_usd,
        CASE 
            WHEN payments.amount_usd > 100 THEN 'high_value'
            ELSE 'standard'
        END AS order_tier
    FROM orders
    LEFT JOIN payments ON orders.payment_id = payments.payment_id
)
SELECT * FROM final
```

### dbt Testing

```yaml
# _stripe__models.yml
models:
  - name: stg_stripe__payments
    description: Cleaned Stripe payment records
    columns:
      - name: payment_id
        description: Primary key
        tests:
          - unique
          - not_null
      - name: amount_usd
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 100000
      - name: status
        tests:
          - accepted_values:
              values: ['succeeded', 'pending', 'refunded']
```

---

## 4. Metrics Layer

### Metrics Definition

| Component | Description | Example |
|---|---|---|
| Metric | Business calculation | Monthly Recurring Revenue |
| Dimension | Grouping attribute | Plan type, region, segment |
| Time grain | Temporal granularity | Day, week, month |
| Filter | Subset condition | Active customers only |

### dbt Semantic Layer (MetricFlow)

```yaml
semantic_models:
  - name: orders
    defaults:
      agg_time_dimension: order_date
    entities:
      - name: order_id
        type: primary
      - name: customer_id
        type: foreign
    measures:
      - name: order_total
        agg: sum
        expr: amount
      - name: order_count
        agg: count
        expr: order_id
    dimensions:
      - name: order_date
        type: time
      - name: status
        type: categorical

metrics:
  - name: revenue
    type: simple
    type_params:
      measure: order_total
    filter: |
      {{ Dimension('status') }} = 'completed'
      
  - name: average_order_value
    type: derived
    type_params:
      expr: revenue / order_count
      metrics:
        - name: revenue
        - name: order_count
```

---

## 5. Schema Design Patterns

### One Big Table (OBT)

- Denormalized, wide table with all dimensions pre-joined
- Best for: BI tools, simple queries, small-medium datasets
- Trade-off: Storage cost vs query simplicity

### Activity Schema

```sql
-- All user activities in one table
CREATE TABLE activity_stream (
    activity_id BIGINT,
    entity_type VARCHAR,      -- 'user', 'order', 'product'
    entity_id VARCHAR,
    activity_type VARCHAR,    -- 'page_view', 'purchase', 'signup'
    occurred_at TIMESTAMP,
    properties JSONB          -- Flexible attributes
);
```

### Wide vs Tall Tables

| Aspect | Wide (Pivoted) | Tall (Unpivoted) |
|---|---|---|
| Structure | One column per metric | Metric name + value columns |
| Query | Simple SELECT | Requires pivot/filter |
| Flexibility | Fixed metrics | Easy to add new metrics |
| Best for | BI dashboards | Metrics stores, time series |
