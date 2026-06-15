# Advanced MongoDB Operations and Tech Support Reference

## Introduction

In the realm of modern database administration and technical support, MongoDB stands out as a highly flexible, scalable NoSQL database. However, as deployments grow from gigabytes to terabytes and beyond, the complexity of managing, optimizing, and troubleshooting MongoDB environments increases exponentially. This document serves as a comprehensive guide for technical support specialists and database administrators dealing with advanced MongoDB topics. It focuses heavily on production operations, worst-case scenarios, and practical troubleshooting techniques.

The topics covered herein include aggregation pipeline optimization, change streams, compound indexes, text search, time series collections, and the handling of massive datasets. Each section is designed to provide deep technical insights, common pitfalls, and actionable solutions for when things go wrong in a production environment.

## 1. Aggregation Pipeline Optimization

The aggregation framework is one of MongoDB's most powerful features, allowing for complex data processing and transformation. However, poorly constructed aggregation pipelines can lead to severe performance degradation, high CPU utilization, and memory exhaustion.

### 1.1 Understanding Pipeline Execution

An aggregation pipeline consists of multiple stages, where the output of one stage becomes the input for the next. The MongoDB query optimizer attempts to optimize the pipeline by reordering stages or combining them where possible. However, the optimizer has limitations, and manual optimization is often required.

### 1.2 Best Practices for Optimization

**Early Filtering:** The most critical optimization technique is to filter data as early as possible in the pipeline. Use `$match` and `$limit` stages at the very beginning to reduce the number of documents passed to subsequent stages. If a `$match` stage is placed at the beginning of the pipeline, it can utilize indexes, drastically improving performance.

**Index Utilization:** Ensure that the initial `$match` or `$sort` stages are covered by appropriate indexes. If an aggregation pipeline cannot use an index, it will perform a collection scan, which is disastrous for large datasets.

**Projection:** Use the `$project` stage early to remove unnecessary fields. This reduces the amount of data held in memory and passed between stages, lowering memory consumption and improving processing speed.

**Memory Limits:** By default, aggregation pipeline stages have a memory limit of 100 megabytes. If a stage exceeds this limit, the query will fail. To handle larger datasets, use the `allowDiskUse: true` option. However, be aware that writing to disk significantly slows down the aggregation process. It is always preferable to optimize the pipeline to stay within memory limits if possible.

### 1.3 Troubleshooting Aggregation Issues

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

## 2. Change Streams

Change streams provide a real-time stream of database changes, allowing applications to react to inserts, updates, deletes, and other events as they happen. They are built on top of the oplog (operations log) and are essential for event-driven architectures.

### 2.1 Architecture and Requirements

Change streams require a replica set or a sharded cluster because they rely on the oplog. They cannot be used on standalone MongoDB instances. When opening a change stream, you can specify a pipeline to filter or transform the events before they are sent to the application.

### 2.2 Production Considerations

**Oplog Size:** The oplog must be large enough to retain events for the duration that a change stream might be disconnected. If the oplog rolls over before a disconnected client reconnects, the client will lose events and must perform a full resync. Monitor oplog window time closely.

**Resume Tokens:** Every change stream event includes a resume token (`_id`). Applications must store this token and use it to resume the stream after a disconnect or crash. Failure to properly manage resume tokens will result in missed or duplicate events.

**Performance Impact:** While change streams are generally efficient, opening a large number of streams or using complex filtering pipelines can impact database performance. Consolidate change streams where possible and keep filtering pipelines simple.

### 2.3 Troubleshooting Change Streams

**Scenario: Application Missing Events**
If an application reports missing events, verify that it is correctly storing and using resume tokens. Check the oplog window size; if the oplog is too small, the application might be falling behind and missing events when it reconnects. Increase the oplog size if necessary.

**Scenario: High Load from Change Streams**
If change streams are causing high load, review the filtering pipelines. Ensure that the pipelines are highly selective and do not perform complex transformations. Consider whether the application truly needs real-time events or if a polling mechanism would suffice.

## 3. Compound Indexes

Compound indexes are indexes that contain multiple fields. They are crucial for optimizing queries that filter or sort on multiple criteria.

### 3.1 The ESR Rule

When designing compound indexes, follow the ESR (Equality, Sort, Range) rule:

1.  **Equality:** Fields that are queried for exact matches should come first in the index.
2.  **Sort:** Fields used for sorting should come next.
3.  **Range:** Fields used for range queries (e.g., `$gt`, `$lt`) should come last.

Following this rule ensures that the index can efficiently filter data, provide the requested sort order without an in-memory sort, and then apply range filters.

### 3.2 Index Intersection vs. Compound Indexes

MongoDB can sometimes use multiple single-field indexes to satisfy a query (index intersection). However, a well-designed compound index is almost always more efficient than index intersection. Do not rely on index intersection for critical queries; create compound indexes instead.

### 3.3 Troubleshooting Index Issues

**Scenario: Query Not Using Expected Index**
If a query is not using the expected compound index, use `explain()` to analyze the query planner's decision. Check if the query predicates match the index prefix. An index on `{ a: 1, b: 1, c: 1 }` can support queries on `{ a: 1 }` and `{ a: 1, b: 1 }`, but not on `{ b: 1 }` or `{ c: 1 }` alone.

**Scenario: In-Memory Sorts**
If `explain()` shows a `SORT` stage instead of using the index for sorting, verify that the sort fields follow the equality fields in the index definition and that the sort direction matches the index direction (or is the exact inverse). In-memory sorts are limited to 32 megabytes; exceeding this limit will cause the query to fail unless `allowDiskUse` is specified.

## 4. Text Search

MongoDB provides text indexes to support text search queries on string content. While powerful, text search has specific limitations and performance characteristics.

### 4.1 Text Index Creation

A collection can have at most one text index. The text index can cover multiple string fields, and you can assign weights to different fields to influence the relevance score of search results.

```javascript
db.articles.createIndex(
  { title: "text", content: "text" },
  { weights: { title: 10, content: 1 } }
)
```

### 4.2 Performance and Limitations

Text indexes can be large and resource-intensive to build and maintain. They are not suitable for real-time, highly concurrent write workloads. Text search queries can also be CPU-intensive, especially when searching across large datasets or using complex search terms.

### 4.3 Troubleshooting Text Search

**Scenario: Slow Text Search Queries**
If text search queries are slow, consider whether MongoDB's built-in text search is the right tool for the job. For advanced text search requirements, such as fuzzy matching, stemming, or complex relevance tuning, a dedicated search engine like Elasticsearch or Apache Solr integrated with MongoDB (e.g., via MongoDB Atlas Search) is often a better choice.

**Scenario: High Memory Usage During Index Build**
Building a text index on a large collection can consume significant memory and CPU. Build text indexes during off-peak hours or use rolling index builds in a replica set to minimize the impact on production workloads.

## 5. Time Series Collections

Introduced in MongoDB 5.0, time series collections are optimized for storing and querying time-series data, such as IoT sensor readings, financial market data, or system metrics.

### 5.1 Architecture and Benefits

Time series collections automatically organize data by time and a specified metadata field. Under the hood, MongoDB stores time-series data in a highly compressed, columnar format, significantly reducing storage space and improving query performance for time-based aggregations.

### 5.2 Creating Time Series Collections

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

### 5.3 Troubleshooting Time Series Collections

**Scenario: Poor Query Performance**
If queries on a time series collection are slow, ensure that you are filtering by the `timeField` and `metaField`. Queries that do not filter by these fields will scan the entire collection. Create secondary indexes on the `metaField` or other frequently queried fields if necessary.

**Scenario: High Storage Usage**
If a time series collection is consuming more storage than expected, verify that the `granularity` setting matches the actual data ingestion rate. If the granularity is set too fine (e.g., "seconds" for data arriving every hour), compression will be less effective.

## 6. Handling Huge Datasets

Managing datasets that exceed terabytes or petabytes requires careful planning, architecture, and operational discipline.

### 6.1 Sharding

Sharding is MongoDB's method for distributing data across multiple machines. It is essential for handling datasets that exceed the storage or processing capacity of a single replica set.

**Choosing a Shard Key:** The shard key determines how data is distributed across the cluster. Choosing the wrong shard key is the most common cause of performance issues in sharded clusters. A good shard key should have high cardinality, even distribution, and support targeted queries.

**Jumbo Chunks:** If a shard key has low cardinality, multiple documents with the same shard key value will be grouped into a single chunk. If this chunk grows beyond the maximum chunk size, it becomes a "jumbo chunk" and cannot be migrated. Avoid low-cardinality shard keys to prevent jumbo chunks.

### 6.2 Archiving and Data Lifecycle Management

Do not keep all data in the primary operational database indefinitely. Implement data lifecycle management policies to archive or delete old data.

**TTL Indexes:** Use Time-To-Live (TTL) indexes to automatically delete documents after a certain period. This is useful for log data, session data, or other transient information.

**Archiving Strategies:** For data that must be retained but is rarely accessed, move it to cheaper storage solutions, such as Amazon S3 or a dedicated archival database. MongoDB Atlas Data Lake or custom scripts can be used to query archived data when necessary.

### 6.3 Troubleshooting Huge Datasets

**Scenario: Uneven Data Distribution**
If data is unevenly distributed across shards, check the shard key. An uneven distribution indicates a poorly chosen shard key or a sudden change in data ingestion patterns. You may need to reshard the collection, which is a complex and resource-intensive operation.

**Scenario: Slow Backups and Restores**
Backing up and restoring huge datasets can take days. Use filesystem snapshots or storage-level backups instead of `mongodump` for large deployments. Ensure that your backup strategy meets your Recovery Time Objective (RTO) and Recovery Point Objective (RPO).

## 7. MongoDB CLI Reference

This section serves as a comprehensive, production-focused CLI reference for MongoDB operations. It is designed specifically for tech support engineers, database administrators, and DevOps professionals who need to manage, troubleshoot, and recover MongoDB deployments under pressure. The tools covered in this guide include `mongosh`, `mongodump`, `mongorestore`, `mongoexport`, and `mongoimport`.

### 7.1 The MongoDB Shell (`mongosh`)

The MongoDB Shell (`mongosh`) is a fully functional JavaScript and Node.js environment for interacting with MongoDB deployments.

**Connection and Authentication:**
```bash
mongosh "mongodb://localhost:27017"
mongosh "mongodb://db.example.com:27017" --tls --tlsCAFile /etc/ssl/ca.pem --tlsCertificateKeyFile /etc/ssl/client.pem
```

**Advanced Querying and Aggregation:**
```javascript
db.users.find({ status: "active" }, { email: 1, lastLogin: 1, _id: 0 }).sort({ lastLogin: -1 }).limit(100)
```

**Index Management and Optimization:**
```javascript
db.orders.find({ customerId: "CUST-123", status: "shipped" }).explain("executionStats")
db.orders.createIndex({ customerId: 1, status: 1 }, { background: true })
```

**Replica Set and Cluster Management:**
```javascript
rs.status()
rs.stepDown(120)
```

### 7.2 Data Backup with `mongodump`

`mongodump` is a utility for creating binary exports of the contents of a database.

**Full Database Backup:**
```bash
mongodump --uri="mongodb://user:password@localhost:27017/admin" --out=/backups/full_backup_$(date +%F)
```

**Archiving and Compressing on the Fly:**
```bash
mongodump --uri="mongodb://localhost:27017/mydb" --archive=/backups/mydb_$(date +%F).archive.gz --gzip
```

**Oplog Backups for Point-in-Time Recovery:**
```bash
mongodump --uri="mongodb://localhost:27017/admin" --oplog --out=/backups/oplog_backup
```

### 7.3 Data Restoration with `mongorestore`

`mongorestore` reads the binary files produced by `mongodump` and restores them to a MongoDB instance.

**Restoring a Full Backup:**
```bash
mongorestore --uri="mongodb://localhost:27017/admin" /backups/full_backup_2023-10-25
```

**Point-in-Time Recovery using the Oplog:**
```bash
mongorestore --uri="mongodb://localhost:27017/admin" --oplogReplay --oplogLimit="1698278400" /backups/oplog_backup
```

### 7.4 Data Export with `mongoexport`

`mongoexport` produces a JSON or CSV export of data stored in a MongoDB instance.

**Exporting a Collection to JSON:**
```bash
mongoexport --uri="mongodb://localhost:27017/mydb" --collection=users --out=users.json
```

**Exporting to CSV with Specific Fields:**
```bash
mongoexport --uri="mongodb://localhost:27017/mydb" --collection=orders --type=csv --fields="_id,customerId,totalAmount,status" --out=orders.csv
```

### 7.5 Data Import with `mongoimport`

`mongoimport` imports content from an Extended JSON, CSV, or TSV export created by `mongoexport`.

**Importing a JSON File:**
```bash
mongoimport --uri="mongodb://localhost:27017/mydb" --collection=users --file=users.json
```

**Upserting Data:**
```bash
mongoimport --uri="mongodb://localhost:27017/mydb" --collection=inventory --file=inventory_update.json --mode=upsert --upsertFields=sku
```

## 8. Worst-Case Scenarios and Tech Support Tactics

### 8.1 Recovering from a Dropped Collection

If a collection is accidentally dropped, and you have an oplog backup, you can recover it.

1.  **Stop all writes** to the database if possible.
2.  **Dump the oplog** from the primary or a secondary node.
3.  **Identify the drop command** in the oplog and note its timestamp.
4.  **Restore the last full backup**.
5.  **Replay the oplog** up to the timestamp just before the drop command using `mongorestore --oplogLimit`.

### 8.2 Handling High CPU or Memory Usage

When a MongoDB node is unresponsive due to high resource usage:

1.  **Connect via `mongosh`** (you may need to connect locally if remote connections are timing out).
2.  **Check current operations:** `db.currentOp({ "active": true, "secs_running": { "$gt": 3 } })`
3.  **Kill long-running queries:** `db.killOp(<opid>)`
4.  **Analyze the logs** to identify the source of the queries.
5.  **Add missing indexes** or optimize the application code.

### 8.3 Repairing a Corrupted Database

If the MongoDB process crashes and the data files become corrupted (rare with WiredTiger, but possible):

1.  **Stop the `mongod` process.**
2.  **Run the repair command:** `mongod --repair --dbpath /var/lib/mongodb`
3.  **Check the logs** for any unrecoverable errors.
4.  **Restart the `mongod` process.**
5.  **Run `db.collection.validate({full: true})`** on critical collections to ensure data integrity.

## 9. Advanced One-Liners for Daily Operations

**Find the top 5 largest collections in a database:**
```bash
mongosh mydb --quiet --eval 'db.getCollectionNames().map(c => ({name: c, size: db[c].stats().size})).sort((a, b) => b.size - a.size).slice(0, 5)'
```

**Kill all queries running longer than 60 seconds:**
```bash
mongosh admin --quiet --eval 'db.currentOp({ "active": true, "secs_running": { "$gt": 60 } }).inprog.forEach(op => db.killOp(op.opid))'
```

**Export all user emails to a text file:**
```bash
mongoexport --uri="mongodb://localhost:27017/mydb" --collection=users --fields=email --type=csv | tail -n +2 > emails.txt
```

**Monitor replication lag in real-time (run in a loop):**
```bash
watch -n 2 'mongosh admin --quiet --eval "rs.printSlaveReplicationInfo()"'
```

## 10. Performance Tuning and Diagnostics

### 10.1 Profiling Slow Queries

MongoDB includes a built-in database profiler that logs detailed information about database operations.

**Enabling the Profiler:**
```javascript
// Enable profiling for queries slower than 100ms
db.setProfilingLevel(1, { slowms: 100 })
```

**Analyzing Profiler Data:**
```javascript
// Find the top 10 slowest queries in the last hour
db.system.profile.find({
  ts: { $gt: new ISODate(Date.now() - 1000 * 60 * 60) }
}).sort({ millis: -1 }).limit(10)
```

### 10.2 Analyzing the WiredTiger Storage Engine

WiredTiger is the default storage engine for MongoDB. Understanding its internal state can help diagnose I/O bottlenecks and memory pressure.

**Viewing WiredTiger Statistics:**
```javascript
// Get detailed statistics for the WiredTiger storage engine
db.serverStatus().wiredTiger
```

**Key Metrics to Monitor:**
*   `cache.bytes currently in the cache`: Indicates how much memory WiredTiger is using.
*   `cache.maximum bytes configured`: The maximum memory WiredTiger is allowed to use.
*   `cache.tracked dirty bytes in the cache`: The amount of modified data that has not yet been written to disk. High values can indicate I/O bottlenecks.

### 10.3 Network Diagnostics

Network latency and bandwidth limitations can also impact MongoDB performance.

**Checking Network Statistics:**
```javascript
// View network connection statistics
db.serverStatus().connections
```

**Identifying Connection Spikes:**
A sudden increase in connections can overwhelm the database. Monitor the `current` and `created` connection metrics to detect anomalies.

## 11. Troubleshooting Common Errors

### 11.1 "Connection Refused"

**Symptoms:** The application or CLI tool cannot connect to the MongoDB instance.
**Causes:**
*   The `mongod` process is not running.
*   A firewall is blocking the connection.
*   The `bindIp` configuration is restricting access.
**Resolution:**
1.  Check the status of the `mongod` service (`systemctl status mongod`).
2.  Verify firewall rules.
3.  Check the `net.bindIp` setting in `mongod.conf`.

## Conclusion

Managing advanced MongoDB deployments requires a deep understanding of the database's internal mechanics and a proactive approach to monitoring and optimization. By mastering aggregation pipelines, change streams, compound indexes, text search, time series collections, and sharding, technical support specialists and database administrators can ensure that their MongoDB environments remain performant, scalable, and resilient in the face of massive data volumes and complex workloads. Always rely on empirical data from `explain()` plans and monitoring tools to guide your optimization efforts, and never underestimate the importance of a well-designed schema and indexing strategy.
