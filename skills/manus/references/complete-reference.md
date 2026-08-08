# Manus Complete Reference

**Verified against upstream: 2026-08-07**

## Table of Contents
1. [Manus v2 API Endpoints](#manus-v2-api-endpoints)
2. [WebMCP Integration](#webmcp-integration)
3. [Dependency Practices](#dependency-practices)
4. [Kubernetes and PostgreSQL Patterns](#kubernetes-and-postgresql-patterns)

## Manus v2 API Endpoints

The official Manus v2 API documentation is available at `https://open.manus.ai/docs/v2/introduction`.

- Base URL: `https://api.manus.ai` (API v2 is the current contract; verify endpoint paths in the linked v2 reference).
- Authentication: Bearer token in the `Authorization` header.

## WebMCP Integration

WebMCP provides robust browser automation capabilities.

- Ensure Puppeteer scripts are compatible with version 25.5.0.
- Use robust waiting strategies (e.g., waiting for specific elements or network idle) instead of fixed timeouts.

## Dependency Practices

- **AWS S3:** Ensure S3 multipart uploads specify CRC-64/NVME checksums for data integrity.

## Kubernetes and PostgreSQL Patterns

- **Kubernetes:** Apply modern network policies for sandbox isolation. Dry-run policies before applying.
- **PostgreSQL:** Implement modern replication practices for state management.
