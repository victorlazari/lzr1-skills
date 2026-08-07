# Compound Indexes, Text Search, and Time Series

**Verified against upstream:** 2026-08-07
**Primary Source:** [MongoDB Indexes Documentation](https://www.mongodb.com/docs/manual/indexes/)

## 1. Compound Indexes

Compound indexes are indexes that contain multiple fields. They are crucial for optimizing queries that filter or sort on multiple criteria.

### 1.1 The ESR Rule

When designing compound indexes, follow the ESR (Equality, Sort, Range) rule:

1.  **Equality:** Fields that are queried for exact matches should come first in the index.
2.  **Sort:** Fields used for sorting should come next.
3.  **Range:** Fields used for range queries (e.g., `$gt`, `$lt`) should come last.

Following this rule ensures that the index can efficiently filter data, provide the requested sort order without an in-memory sort, and then apply range filters.

### 1.2 Index Intersection vs. Compound Indexes

MongoDB can sometimes use multiple single-field indexes to satisfy a query (index intersection). However, a well-designed compound index is almost always more efficient than index intersection. Do not rely on index intersection for critical queries; create compound indexes instead.

### 1.3 Troubleshooting Index Issues

**Scenario: Query Not Using Expected Index**
If a query is not using the expected compound index, use `explain()` to analyze the query planner's decision. Check if the query predicates match the index prefix. An index on `{ a: 1, b: 1, c: 1 }` can support queries on `{ a: 1 }` and `{ a: 1, b: 1 }`, but not on `{ b: 1 }` or `{ c: 1 }` alone.

**Scenario: In-Memory Sorts**
If `explain()` shows a `SORT` stage instead of using the index for sorting, verify that the sort fields follow the equality fields in the index definition and that the sort direction matches the index direction (or is the exact inverse). In-memory sorts are limited to 32 megabytes; exceeding this limit will cause the query to fail unless `allowDiskUse` is specified.

## 2. Text Search

MongoDB provides text indexes to support text search queries on string content. While powerful, text search has specific limitations and performance characteristics.

### 2.1 Text Index Creation

A collection can have at most one text index. The text index can cover multiple string fields, and you can assign weights to different fields to influence the relevance score of search results.

```javascript
db.articles.createIndex(
  { title: "text", content: "text" },
  { weights: { title: 10, content: 1 } }
)
```

### 2.2 Performance and Limitations

Text indexes can be large and resource-intensive to build and maintain. They are not suitable for real-time, highly concurrent write workloads. Text search queries can also be CPU-intensive, especially when searching across large datasets or using complex search terms.

### 2.3 Troubleshooting Text Search

**Scenario: Slow Text Search Queries**
If text search queries are slow, consider whether MongoDB's built-in text search is the right tool for the job. For advanced text search requirements, such as fuzzy matching, stemming, or complex relevance tuning, a dedicated search engine like Elasticsearch or Apache Solr integrated with MongoDB (e.g., via MongoDB Atlas Search) is often a better choice.

**Scenario: High Memory Usage During Index Build**
Building a text index on a large collection can consume significant memory and CPU. Build text indexes during off-peak hours or use rolling index builds in a replica set to minimize the impact on production workloads.

## 3. Time Series Collections

Introduced in MongoDB 5.0, time series collections are optimized for storing and querying time-series data, such as IoT sensor readings, financial market data, or system metrics.

### 3.1 Architecture and Benefits

Time series collections automatically organize data by time and a specified metadata field. Under the hood, MongoDB stores time-series data in a highly compressed, columnar format, significantly reducing storage space and improving query performance for time-based aggregations.

### 3.2 Creating Time Series Collections

When creating a time series collection, you must specify the `timeField` and optionally the `metaField` and `granularity`.

```javascript
db.createCollection("sensor_data", {
  timeseries: {
    timeField: "timestamp",
    metaField: "sensorId",
    granularity: "seconds"
  }
})
```

Choosing the correct granularity (seconds, minutes, or hours) is crucial for optimal performance and compression.

### 3.3 Troubleshooting Time Series Collections

**Scenario: Poor Query Performance**
If queries on a time series collection are slow, ensure that you are filtering by the `timeField` and `metaField`. Queries that do not filter by these fields will scan the entire collection. Create secondary indexes on the `metaField` or other frequently queried fields if necessary.

**Scenario: High Storage Usage**
If a time series collection is consuming more storage than expected, verify that the `granularity` setting matches the actual data ingestion rate. If the granularity is set too fine (e.g., "seconds" for data arriving every hour), compression will be less effective.
