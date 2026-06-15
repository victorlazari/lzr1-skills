# SeaweedFS Complete Reference

## 1. Introduction and Core Philosophy

SeaweedFS is a high-performance, distributed object storage system designed to provide efficient, scalable, and fault-tolerant storage for unstructured data. Its architecture is heavily inspired by the principles outlined in the Haystack and F4 papers, which focus on optimizing disk access for large-scale photo storage and Facebook's cold storage system, respectively.

### Key Architectural Principles

- **O(1) Disk Access**: SeaweedFS uses a combination of volume files and index files, storing data in append-only volumes and maintaining in-memory indexes of file locations. This allows direct seek operations to retrieve file data without scanning large directories or index trees.
- **Lightweight Metadata Management**: Unlike traditional distributed file systems that maintain heavy metadata services, SeaweedFS’s master server keeps only essential metadata, offloading actual file metadata and directory structure management to the filer component or external metadata stores.
- **Flexible Storage Paradigms**: SeaweedFS supports multiple paradigms including raw blob storage, hierarchical file storage, object storage with S3 API compatibility, and integration with data warehouse solutions.

## 2. Core Components

### 2.1 Master Server (`weed master`)

The Master Server acts as the central coordinator of the SeaweedFS cluster. It manages the global namespace of volumes, keeps track of volume server registrations, and maintains the mapping between file IDs and their physical locations.

- **Responsibilities**: Volume management, cluster coordination, garbage collection scheduling, replication control.
- **High Availability**: Supports leader election among multiple master servers using Raft consensus.
- **Default Port**: 9333

### 2.2 Volume Server (`weed volume`)

Volume Servers are the data storage nodes responsible for persisting the actual file data. Each volume server manages a set of volumes, which are append-only data files accompanied by index files that map file IDs to file offsets.

- **Responsibilities**: Data storage, index maintenance, volume lifecycle management, replication.
- **Default Port**: 8080

### 2.3 Filer (`weed filer`)

The Filer component provides a hierarchical namespace and metadata management layer, effectively acting as a distributed file system interface on top of the flat SeaweedFS object storage.

- **Responsibilities**: Directory structures, file metadata, file to fid mapping, metadata storage backend support (LevelDB, MySQL, PostgreSQL, Cassandra, Redis, Etcd).
- **Default Port**: 8888

### 2.4 S3 API Gateway (`weed s3`)

SeaweedFS offers an S3-compatible object storage interface, enabling users to interact with their data using widely adopted Amazon S3 APIs.

- **Features**: Buckets and objects, bucket policies, Server-Side Encryption (SSE-S3), multipart uploads, versioning.
- **Default Port**: 8333

## 3. Advanced Configurations and Features

### 3.1 Cloud Drive and Tiered Storage

SeaweedFS enables seamless tiered storage architectures where "warm data" is stored cost-effectively on cloud providers (AWS S3, GCS, Azure) via the **Cloud Drive**. The volume server proxies data to a remote cloud object store while maintaining metadata locally for performance.

### 3.2 Erasure Coding

Erasure coding (EC) improves storage efficiency by encoding data into redundant fragments. SeaweedFS supports configurable EC parameters `(k, m)` and **rack-aware EC** to optimize reliability across failure domains.

### 3.3 Advanced Filer Configurations

- **Active-Active Cross-Cluster Sync**: Bidirectional replication of filer metadata for multi-region availability.
- **Change Data Capture (CDC)**: Exposes a stream of all metadata changes for audit logging or replication.
- **Filer as Key-Large-Value Store**: Using the filer to store large objects with metadata, useful for genomic data or ML feature stores.

### 3.4 Big Data Integration

- **HDFS Replacement**: SeaweedFS offers a Hadoop Compatible File System (HadoopFS) interface.
- **Spark and Trino Integration**: Supports reading/writing data stored on SeaweedFS, including Iceberg tables via the S3 Table Bucket feature.

### 3.5 Seaweed Message Queue (SMQ) and weed db

- **SMQ**: A distributed message queue system for high-throughput event streaming.
- **weed db**: A PostgreSQL-compatible server built on top of the SeaweedFS filer and volume servers.

## 4. Configuration Schemas

### 4.1 Master Server Configuration (`master.yaml`)

```yaml
master:
  ip: 127.0.0.1
  port: 9333
  peers: []
  defaultReplication: "000"
  gcInterval: 10
  metaFolder: "/var/lib/seaweedfs/master"
```

### 4.2 Volume Server Configuration (`volume.yaml`)

```yaml
volume:
  ip: 127.0.0.1
  port: 8080
  dataCenter: "dc1"
  rack: "rack1"
  publicUrl: "http://localhost:8080"
  pulseSeconds: 5
  folders: ["/data/volume"]
  max: 7
```

### 4.3 Filer Server Configuration (`filer.yaml`)

```yaml
filer:
  ip: 127.0.0.1
  port: 8888
  defaultReplicaPlacement: "001"
  dirListingLimit: 1000
  maxMB: 32
  leveldb:
    dir: "/var/lib/seaweedfs/filerldb"
```

## 5. Replication Strategies

Replication codes are three-digit numeric strings (e.g., `001`, `010`, `110`):
- **First digit**: Number of data replicas.
- **Second digit**: Number of rack replicas.
- **Third digit**: Number of data center replicas.

## 6. Troubleshooting and Diagnostics

### 6.1 "No Free Volumes Left"

- **Symptoms**: Uploads fail, `volume.list` shows all volumes full.
- **Causes**: Physical disk space exhaustion, replication constraints, deleted files not vacuumed.
- **Recovery**: Check disk space, force vacuuming (`volume.vacuum -garbageThreshold 0.1`), temporarily reduce replication.

### 6.2 Filer Metadata Inconsistencies

- **Symptoms**: Files appear in listings but return 404, `fs.verify` reports missing chunks.
- **Recovery**: Run `fs.verify`, fix missing chunks, check underlying Filer database health.

### 6.3 Master Node Election Failures

- **Symptoms**: Raft election timeouts, cannot connect to master.
- **Recovery**: Check network connectivity on port 9333, verify quorum, check NTP synchronization.

## 7. Security Audit Checklist

- **Authentication**: Validate IdPs, review MFA setup, audit credential storage.
- **Authorization**: Review RBAC/ABAC policies, validate user roles and permissions.
- **Encryption**: Ensure SSL/TLS for network communications, validate data-at-rest encryption (SSE-S3).
- **Network Security**: Review firewall rules, ensure segmentation and isolation.
- **System Hardening**: Validate system configurations against benchmarks, enable comprehensive logging.
