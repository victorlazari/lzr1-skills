# Data Visualization

## Table of Contents
1. Visualization Principles
2. Chart Selection
3. Dashboard Design
4. BI Tools
5. Storytelling with Data

---

## 1. Visualization Principles

### Core Principles

| Principle | Description | Application |
|---|---|---|
| Data-ink ratio | Maximize data, minimize decoration | Remove gridlines, borders, 3D effects |
| Pre-attentive attributes | Use color, size, position for emphasis | Highlight key data points |
| Cognitive load | Reduce mental effort to understand | Clear labels, logical layout |
| Consistency | Same encoding across charts | Consistent colors, scales, formats |
| Accessibility | Readable by all users | Color-blind safe palettes, alt text |
| Context | Provide reference points | Benchmarks, targets, comparisons |

### Color Best Practices

| Use Case | Palette Type | Example |
|---|---|---|
| Categories (≤7) | Qualitative | Distinct hues |
| Sequential values | Sequential | Light to dark single hue |
| Diverging values | Diverging | Two hues with neutral midpoint |
| Highlighting | Accent | Gray + one accent color |
| Status | Semantic | Red/yellow/green (with shapes) |

---

## 2. Chart Selection

### Chart Type Decision Guide

| Data Relationship | Chart Type | When to Use |
|---|---|---|
| Comparison | Bar chart (vertical/horizontal) | Compare categories |
| Trend over time | Line chart | Show change over time |
| Part of whole | Stacked bar, donut (≤5 parts) | Show composition |
| Distribution | Histogram, box plot, violin | Show data spread |
| Correlation | Scatter plot | Show relationship between two variables |
| Geographic | Choropleth, bubble map | Location-based data |
| Flow/Process | Sankey, funnel | Show progression or flow |
| Ranking | Horizontal bar (sorted) | Show ordered comparison |
| KPI/Metric | Big number, sparkline | Single metric with context |

### Charts to Avoid

| Chart | Problem | Better Alternative |
|---|---|---|
| Pie chart (>5 slices) | Hard to compare angles | Horizontal bar chart |
| 3D charts | Distorts perception | 2D equivalent |
| Dual-axis | Misleading correlations | Separate charts or indexed |
| Stacked area (many) | Hard to read middle layers | Small multiples |
| Radar/spider | Hard to compare | Grouped bar chart |

---

## 3. Dashboard Design

### Dashboard Layout Principles

```
┌─────────────────────────────────────────────┐
│  Title + Date Range + Filters               │  ← Context
├─────────────┬─────────────┬─────────────────┤
│  KPI 1      │  KPI 2      │  KPI 3          │  ← Key metrics
├─────────────┴─────────────┴─────────────────┤
│  Primary visualization (trend/comparison)    │  ← Main insight
├─────────────────────┬───────────────────────┤
│  Supporting chart 1 │  Supporting chart 2    │  ← Detail
├─────────────────────┴───────────────────────┤
│  Table / Detail view                         │  ← Drill-down
└─────────────────────────────────────────────┘
```

### Dashboard Types

| Type | Audience | Update Frequency | Purpose |
|---|---|---|---|
| Strategic | Executives | Weekly/Monthly | High-level KPIs, trends |
| Operational | Managers | Real-time/Daily | Monitor operations |
| Analytical | Analysts | On-demand | Explore and investigate |
| Tactical | Teams | Daily | Track progress, actions |

### Dashboard Best Practices

- Start with the most important metric (top-left)
- Limit to 5-7 visualizations per dashboard
- Use consistent time ranges across all charts
- Provide context (targets, benchmarks, prior period)
- Enable drill-down from summary to detail
- Use filters sparingly (max 3-4 global filters)
- Mobile-responsive design for executive dashboards
- Include data freshness indicator

---

## 4. BI Tools

### BI Tool Comparison

| Tool | Type | Best For |
|---|---|---|
| Looker | Enterprise, semantic layer | Data governance, LookML |
| Tableau | Enterprise, visual analytics | Complex visualizations |
| Power BI | Enterprise, Microsoft ecosystem | Office 365 integration |
| Metabase | Open-source, self-service | Quick setup, SQL-friendly |
| Superset | Open-source, enterprise | Large-scale, customizable |
| Sigma | Cloud-native, spreadsheet-like | Business user self-service |
| Hex | Notebook + dashboard | Data teams, Python + SQL |
| Evidence | Code-based BI | Version-controlled reports |

### Semantic Layer / Metrics Layer

```yaml
# dbt metrics layer example
metrics:
  - name: monthly_recurring_revenue
    label: Monthly Recurring Revenue (MRR)
    type: sum
    sql: mrr_amount
    timestamp: date_month
    time_grains: [month, quarter, year]
    dimensions:
      - plan_type
      - region
    filters:
      - field: status
        operator: '='
        value: "'active'"
```

---

## 5. Storytelling with Data

### Narrative Structure

1. **Context**: Set the scene (what's the situation?)
2. **Conflict**: Identify the problem or opportunity
3. **Resolution**: Present the insight and recommendation
4. **Action**: Clear next steps with owners and timelines

### Annotation Best Practices

| Element | Purpose | Example |
|---|---|---|
| Title | State the insight (not the chart type) | "Revenue grew 23% after price change" |
| Subtitle | Provide context | "Q1 2025 vs Q1 2024, US market only" |
| Annotations | Call out key data points | Arrow pointing to inflection point |
| Source | Build trust | "Source: Internal analytics, as of Jan 15" |
| Footnotes | Clarify methodology | "Excludes free trial users" |

### Presentation Formats

| Format | Audience | Detail Level |
|---|---|---|
| Executive summary | C-suite | 1 page, key metrics + recommendation |
| Analysis report | Stakeholders | 3-5 pages, findings + methodology |
| Deep dive | Data team | Full analysis, code, assumptions |
| Self-service dashboard | Business users | Interactive, filterable |
