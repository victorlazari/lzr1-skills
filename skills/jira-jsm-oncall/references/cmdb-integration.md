# CMDB Integration Guide

**Verified against upstream:** 2026-08-07

## Overview

Modern IT Service Management relies heavily on Configuration Management Databases (CMDBs) to provide contextual information about assets and their relationships. Jira Service Management’s integration with asset management tools enhances incident management by enabling impact analysis, root cause identification, and informed decision-making.

## Linking Assets to Incidents

Integration begins with linking assets to Jira issues. JSM supports native asset management via **Jira Assets** (formerly Insight), or through connectors to external CMDBs such as ServiceNow, BMC Remedy, or Device42.

When an incident is created, the affected asset or configuration item (CI) can be associated with the ticket, either manually or automatically via discovery tools or monitoring integrations. This linkage provides service desk agents with immediate visibility into asset attributes, ownership, and criticality.

This integration is critical for incident prioritization and routing. For example, an incident affecting a high-value database server might be escalated automatically due to the asset's criticality.

## Automated Impact Analysis

Advanced CMDB integrations facilitate automated impact analysis, where the relationships and dependencies between assets are used to assess the scope of an incident. For instance, if a network switch fails, the system can identify all dependent services and users potentially impacted.

Jira automation rules or external orchestration engines can then update incident fields or notify affected teams accordingly. This proactive approach reduces resolution times and improves communication.

The integration also supports change management by correlating incidents with configuration changes, further enhancing root cause analysis and compliance.

## Authoritative Sources

- [Jira Service Management Documentation](https://confluence.atlassian.com/servicedeskcloud)
