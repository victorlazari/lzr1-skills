# Data Analysis

## Table of Contents
1. SQL Mastery
2. Exploratory Data Analysis
3. Statistical Methods
4. Experimentation (A/B Testing)
5. Python for Analysis

---

## 1. SQL Mastery

### Advanced SQL Patterns

```sql
-- Window functions for running totals and rankings
SELECT 
    date,
    revenue,
    SUM(revenue) OVER (ORDER BY date) AS cumulative_revenue,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rank_in_category,
    LAG(revenue, 1) OVER (ORDER BY date) AS previous_day_revenue,
    revenue - LAG(revenue, 1) OVER (ORDER BY date) AS day_over_day_change
FROM daily_metrics;

-- Cohort analysis
WITH cohorts AS (
    SELECT 
        user_id,
        DATE_TRUNC('month', first_purchase_date) AS cohort_month,
        DATE_TRUNC('month', purchase_date) AS activity_month
    FROM purchases
)
SELECT 
    cohort_month,
    activity_month,
    EXTRACT(MONTH FROM AGE(activity_month, cohort_month)) AS months_since_first,
    COUNT(DISTINCT user_id) AS active_users
FROM cohorts
GROUP BY 1, 2, 3;

-- Funnel analysis
WITH funnel AS (
    SELECT 
        user_id,
        MAX(CASE WHEN event = 'page_view' THEN 1 END) AS viewed,
        MAX(CASE WHEN event = 'add_to_cart' THEN 1 END) AS added,
        MAX(CASE WHEN event = 'checkout' THEN 1 END) AS checked_out,
        MAX(CASE WHEN event = 'purchase' THEN 1 END) AS purchased
    FROM events
    WHERE event_date = CURRENT_DATE
    GROUP BY user_id
)
SELECT 
    COUNT(*) AS total_users,
    SUM(viewed) AS viewers,
    SUM(added) AS adders,
    SUM(checked_out) AS checkers,
    SUM(purchased) AS purchasers,
    ROUND(100.0 * SUM(purchased) / NULLIF(SUM(viewed), 0), 2) AS conversion_rate
FROM funnel;
```

### SQL Performance Tips

| Technique | When to Use | Impact |
|---|---|---|
| CTEs over subqueries | Readability, reuse | Clarity (sometimes perf) |
| EXISTS over IN | Large subquery results | Faster short-circuit |
| UNION ALL over UNION | No dedup needed | Avoids sort |
| Approximate functions | Large datasets, dashboards | 10-100x faster |
| Materialized views | Repeated expensive queries | Pre-computed results |
| Partitioning | Large tables, date-based queries | Scan less data |

---

## 2. Exploratory Data Analysis

### EDA Checklist

| Step | Questions | Actions |
|---|---|---|
| Shape | How many rows/columns? | `df.shape`, `COUNT(*)` |
| Types | What are the data types? | `df.dtypes`, schema inspection |
| Missing | What's null/missing? | `df.isnull().sum()`, `NULL` counts |
| Distribution | How is data distributed? | Histograms, percentiles, skewness |
| Outliers | Are there extreme values? | Box plots, IQR method, z-scores |
| Relationships | How do variables relate? | Correlation matrix, scatter plots |
| Temporal | How does data change over time? | Time series plots, seasonality |
| Cardinality | How many unique values? | `COUNT(DISTINCT)`, value counts |

### Descriptive Statistics

| Metric | Purpose | Sensitivity |
|---|---|---|
| Mean | Central tendency | Sensitive to outliers |
| Median | Central tendency (robust) | Robust to outliers |
| Mode | Most common value | Categorical data |
| Standard deviation | Spread | Sensitive to outliers |
| IQR | Spread (robust) | Robust to outliers |
| Skewness | Distribution asymmetry | Tail direction |
| Kurtosis | Distribution tail weight | Outlier frequency |

---

## 3. Statistical Methods

### Hypothesis Testing

| Test | Use Case | Assumptions |
|---|---|---|
| t-test (independent) | Compare two group means | Normal distribution, equal variance |
| t-test (paired) | Before/after comparison | Normal differences |
| Chi-square | Categorical variable association | Expected count ≥ 5 |
| Mann-Whitney U | Compare two groups (non-parametric) | Ordinal or continuous |
| ANOVA | Compare 3+ group means | Normal, equal variance |
| Kruskal-Wallis | Compare 3+ groups (non-parametric) | Ordinal or continuous |

### Correlation Methods

| Method | Data Type | Range | Interpretation |
|---|---|---|---|
| Pearson | Continuous, linear | -1 to 1 | Linear relationship strength |
| Spearman | Ordinal/non-linear | -1 to 1 | Monotonic relationship |
| Kendall | Ordinal, small samples | -1 to 1 | Concordance |
| Point-biserial | Binary + continuous | -1 to 1 | Binary-continuous relationship |

### Regression Analysis

| Type | Use Case | Output |
|---|---|---|
| Linear | Continuous outcome, linear relationship | Coefficients, R² |
| Logistic | Binary outcome | Probabilities, odds ratios |
| Poisson | Count data | Rate ratios |
| Time series (ARIMA) | Temporal forecasting | Forecasts, confidence intervals |

---

## 4. Experimentation (A/B Testing)

### Experiment Design

```
1. Define hypothesis: "Feature X will increase metric Y by Z%"
2. Calculate sample size: Based on MDE, significance, power
3. Randomize: Assign users to control/treatment
4. Run experiment: Collect data for required duration
5. Analyze results: Statistical test + practical significance
6. Make decision: Ship, iterate, or kill
```

### Sample Size Calculation

| Parameter | Description | Typical Value |
|---|---|---|
| Significance level (α) | False positive rate | 0.05 (5%) |
| Power (1-β) | True positive rate | 0.80 (80%) |
| MDE | Minimum detectable effect | Business-defined |
| Baseline rate | Current metric value | From historical data |

### Common Pitfalls

| Pitfall | Problem | Solution |
|---|---|---|
| Peeking | Inflated false positive rate | Pre-commit to duration or use sequential testing |
| Multiple comparisons | Inflated false positive rate | Bonferroni correction, FDR |
| Simpson's paradox | Aggregate hides segment effects | Segment analysis |
| Novelty effect | Short-term behavior change | Run longer experiments |
| Selection bias | Non-random assignment | Proper randomization |
| Survivorship bias | Only analyzing completers | Intent-to-treat analysis |

---

## 5. Python for Analysis

### Essential Libraries

| Library | Purpose | Use Case |
|---|---|---|
| pandas | Data manipulation | DataFrames, cleaning, aggregation |
| polars | Fast data manipulation | Large datasets, performance |
| numpy | Numerical computing | Arrays, math operations |
| scipy | Statistical functions | Hypothesis tests, distributions |
| statsmodels | Statistical modeling | Regression, time series |
| scikit-learn | Machine learning | Classification, clustering |
| matplotlib | Basic plotting | Publication-quality figures |
| seaborn | Statistical visualization | Distribution, relationship plots |
| plotly | Interactive visualization | Dashboards, exploration |

### pandas Best Practices

```python
# Method chaining for readable transformations
result = (
    df
    .query("status == 'active' and revenue > 0")
    .assign(
        revenue_per_user=lambda x: x['revenue'] / x['users'],
        month=lambda x: x['date'].dt.to_period('M')
    )
    .groupby('month')
    .agg(
        total_revenue=('revenue', 'sum'),
        avg_revenue_per_user=('revenue_per_user', 'mean'),
        user_count=('users', 'sum')
    )
    .sort_index()
)
```
