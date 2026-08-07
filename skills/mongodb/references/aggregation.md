# Aggregation Pipeline Optimization

**Verified against upstream:** 2026-08-07
**Primary Source:** [MongoDB Aggregation Documentation](https://www.mongodb.com/docs/manual/aggregation/)

The aggregation framework is one of MongoDB's most powerful features, allowing for complex data processing and transformation. However, poorly constructed aggregation pipelines can lead to severe performance degradation, high CPU utilization, and memory exhaustion.

## 1. Understanding Pipeline Execution

An aggregation pipeline consists of multiple stages, where the output of one stage becomes the input for the next. The MongoDB query optimizer attempts to optimize the pipeline by reordering stages or combining them where possible. However, the optimizer has limitations, and manual optimization is often required.

## 2. Best Practices for Optimization

**Early Filtering:** The most critical optimization technique is to filter data as early as possible in the pipeline. Use `$match` and `$limit` stages at the very beginning to reduce the number of documents passed to subsequent stages. If a `$match` stage is placed at the beginning of the pipeline, it can utilize indexes, drastically improving performance.

**Index Utilization:** Ensure that the initial `$match` or `$sort` stages are covered by appropriate indexes. If an aggregation pipeline cannot use an index, it will perform a collection scan, which is disastrous for large datasets.

**Projection:** Use the `$project` stage early to remove unnecessary fields. This reduces the amount of data held in memory and passed between stages, lowering memory consumption and improving processing speed.

**Memory Limits:** By default, aggregation pipeline stages have a memory limit of 100 megabytes. If a stage exceeds this limit, the query will fail. To handle larger datasets, use the `allowDiskUse: true` option. However, be aware that writing to disk significantly slows down the aggregation process. It is always preferable to optimize the pipeline to stay within memory limits if possible.

**MongoDB 8.0 Operators:** Leverage new aggregation operators introduced in MongoDB 8.0 for more efficient data processing. Refer to the [MongoDB 8.0 Release Notes](https://www.mongodb.com/docs/manual/release-notes/8.0/) for the latest operators and performance improvements.

## 3. Troubleshooting Aggregation Issues

**Scenario: High CPU and Slow Queries**
When an aggregation query causes high CPU usage and takes a long time to execute, the first step is to analyze the query execution plan using the `explain()` method.

```javascript
db.collection.explain("executionStats").aggregate([
  { $match: { status: "active" } },
  { $group: { _id: "$category", total: { $sum: "$amount" } } }
])
```

Look for the `winningPlan` and check if an index was used (`IXSCAN`) or if a collection scan occurred (`COLLSCAN`). If a collection scan is present, create an appropriate index for the `$match` stage.

**Scenario: Memory Limit Exceeded**
If an aggregation fails with a memory limit error, evaluate whether `allowDiskUse: true` is an acceptable workaround. If performance is critical, review the pipeline to see if data can be filtered earlier or if the `$group` or `$sort` stages can be optimized. Consider pre-aggregating data using materialized views or scheduled background jobs if the aggregation is run frequently.
