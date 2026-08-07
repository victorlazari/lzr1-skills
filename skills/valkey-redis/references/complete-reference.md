# Valkey Complete Reference

This document provides an expert-level reference for Valkey, an open-source, high-performance key-value data store that originated as a fork of Redis OSS 7.2.4.

*Verified against upstream: 2026-08-07*

## 1. Introduction to Valkey

Valkey maintains compatibility with Redis OSS 7.2 and earlier versions, supporting the RESP wire protocol (RESP2 and RESP3). It supports both standalone and cluster deployments, offering features like multi-master replication, dynamic slot sharding, and enhanced failover.

**Key Features:**
- **Compatibility:** Drop-in replacement for Redis OSS 7.2.
- **High Availability:** Multi-master replication and consensus-based failovers.
- **Performance:** Built-in support for TLS and experimental support for RDMA.
- **Persistence:** RDB snapshots and AOF (Append Only File).

## 2. Architecture Overview

Valkey's architecture is designed for enterprise-scale applications, providing high availability, fault tolerance, and data consistency.

- **Data Nodes:** Primary storage units handling read and write operations.
- **Replication:** Master-replica model for data redundancy.
- **Cluster Mode:** Horizontal scaling with automatic sharding and failover.

## 3. Configuration Schemas

The primary configuration file is typically located at `/etc/valkey/valkey.conf`.

### General Settings
- `daemonize`: Set to `yes` for production environments.
- `pidfile`: Path to store the process ID (e.g., `/var/run/valkey/valkey-server.pid`).
- `loglevel`: `notice` for general use, `debug` for troubleshooting.
- `logfile`: Path to the log file.

### Network Settings
- `bind`: `0.0.0.0` for remote access (ensure firewall settings).
- `port`: Default is `6379`.
- `tls-port`: Port for TLS connections (if enabled).

### Persistence Settings
- `save`: Conditions for RDB snapshots (e.g., `save 900 1`).
- `appendonly`: Enable AOF (`yes`) for better durability.
- `appendfsync`: `everysec` balances performance and data safety.

### Security Settings
- `requirepass`: Set a strong password.
- `rename-command`: Rename dangerous commands like `FLUSHALL`.

## 4. CLI Command Reference

The `valkey-cli` is the primary tool for managing instances. It is highly compatible with `redis-cli`.

### Basic Commands
- `PING`: Test connection.
- `INFO`: Server statistics (look for `valkey_version`).
- `CONFIG GET/SET`: Manage configuration dynamically.

### Key Management
- `SET key "value"`: Assign a value.
- `GET key`: Retrieve a value.
- `DEL key`: Remove a key.

## 5. Migration Strategies (Redis to Valkey)

Migrating from Redis OSS to Valkey is straightforward due to high compatibility.

### Approach 1: Physical Migration (Downtime Required)
1. Stop the Redis server.
2. Copy the `dump.rdb` and/or `appendonly.aof` files to the Valkey data directory.
3. Update `valkey.conf` to point to these files.
4. Start the Valkey server.

### Approach 2: Replication (Minimal Downtime)
1. Configure the Valkey instance as a replica of the existing Redis master using `REPLICAOF <redis-master-ip> <redis-master-port>`.
2. Wait for the initial synchronization to complete (`INFO replication`).
3. Stop writes to the Redis master.
4. Promote the Valkey replica to master using `REPLICAOF NO ONE`.
5. Update client connection strings to point to the new Valkey master.

## 6. Experimental Features

- **RDMA Support:** Valkey includes experimental support for RDMA (Remote Direct Memory Access) to improve network performance. Consult the official documentation for configuration details.
