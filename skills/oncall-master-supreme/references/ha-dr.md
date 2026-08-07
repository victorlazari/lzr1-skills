# High Availability and Disaster Recovery for On-Call Systems

Verified against upstream: 2026-08-07

## Overview

High Availability (HA) and Disaster Recovery (DR) are critical for on-call systems to ensure continuous operation and rapid recovery during outages.

## Key Concepts

-   **Redundancy:** Deploying multiple instances of critical components across different availability zones or regions.
-   **Failover:** Automatic switching to a standby system or network upon failure of the primary system.
-   **RTO (Recovery Time Objective):** The maximum acceptable amount of time to restore the system after an outage.
-   **RPO (Recovery Point Objective):** The maximum acceptable amount of data loss measured in time.

## Best Practices

1.  **Multi-Region Deployment:** Distribute on-call infrastructure across multiple geographic regions to mitigate regional outages.
2.  **Automated Failover:** Implement automated failover mechanisms for databases, message queues, and application servers.
3.  **Regular DR Testing:** Conduct regular disaster recovery drills to validate failover procedures and RTO/RPO targets.
4.  **Data Replication:** Ensure synchronous or near-synchronous data replication across regions for critical configuration and incident data.

## References

-   [AWS Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)
-   [Google Cloud Disaster Recovery Planning Guide](https://cloud.google.com/architecture/disaster-recovery)
