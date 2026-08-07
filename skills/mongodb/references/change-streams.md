# Change Streams

**Verified against upstream:** 2026-08-07
**Primary Source:** [MongoDB Change Streams Documentation](https://www.mongodb.com/docs/manual/changeStreams/)

Change streams provide a real-time stream of database changes, allowing applications to react to inserts, updates, deletes, and other events as they happen. They are built on top of the oplog (operations log) and are essential for event-driven architectures.

## 1. Architecture and Requirements

Change streams require a replica set or a sharded cluster because they rely on the oplog. They cannot be used on standalone MongoDB instances. When opening a change stream, you can specify a pipeline to filter or transform the events before they are sent to the application.

## 2. Production Considerations

**Oplog Size:** The oplog must be large enough to retain events for the duration that a change stream might be disconnected. If the oplog rolls over before a disconnected client reconnects, the client will lose events and must perform a full resync. Monitor oplog window time closely.

**Resume Tokens:** Every change stream event includes a resume token (`_id`). Applications must store this token and use it to resume the stream after a disconnect or crash. Failure to properly manage resume tokens will result in missed or duplicate events.

**Performance Impact:** While change streams are generally efficient, opening a large number of streams or using complex filtering pipelines can impact database performance. Consolidate change streams where possible and keep filtering pipelines simple.

## 3. Troubleshooting Change Streams

**Scenario: Application Missing Events**
If an application reports missing events, verify that it is correctly storing and using resume tokens. Check the oplog window size; if the oplog is too small, the application might be falling behind and missing events when it reconnects. Increase the oplog size if necessary.

**Scenario: High Load from Change Streams**
If change streams are causing high load, review the filtering pipelines. Ensure that the pipelines are highly selective and do not perform complex transformations. Consider whether the application truly needs real-time events or if a polling mechanism would suffice.
