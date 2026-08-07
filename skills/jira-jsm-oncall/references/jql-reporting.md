# JQL Reporting Guide

**Verified against upstream:** 2026-08-07

## Overview

Jira Query Language (JQL) is an essential tool for extracting actionable insights from Jira Service Management. Advanced reporting leverages complex JQL queries, custom dashboards, and gadgets to deliver real-time operational metrics.

## Complex JQL Queries

JQL supports a rich syntax to filter issues by attributes such as status, priority, SLA status, linked assets, and custom fields. For incident management, useful advanced queries include:

- Filtering by SLA breach status and elapsed time:

```jql
project = "ITSM" AND "Time to Resolution" = breached() AND priority in (Critical, High)
```

- Querying incidents linked to specific assets or CIs:

```jql
issue.property[com.atlassian.jira.service.management.asset].assetId = "server-12345"
```

- Identifying tickets assigned to on-call engineers during specific periods:

```jql
assignee in membersOf("OnCallTeam") AND created >= -7d
```

- Combining multiple conditions with nested logic:

```jql
project = "ITSM" AND status in ("In Progress", "Waiting for Support") AND (priority = Critical OR "Customer Impact" = High)
```

These queries can be saved as filters and incorporated into dashboards or automation rules.

## Custom Reports and Dashboards

Building advanced reports involves integrating multiple gadgets and filters to provide a comprehensive view of incident management performance. Common dashboard components include:

- **SLA Compliance Reports:** Visualizing SLA attainment by priority or service.
- **Incident Volume Trends:** Time-series charts showing ticket creation and resolution rates.
- **On-Call Engineer Workload:** Reports highlighting ticket assignments and escalations per engineer.
- **Asset Impact Reports:** Correlating incidents with affected assets to identify recurring issues.

Data can be exported or linked to external BI tools for deeper analytics. Utilizing JQL filters as data sources ensures reports reflect the latest operational state.

## Authoritative Sources

- [Advanced JQL Functions](https://support.atlassian.com/jira-software-cloud/docs/advanced-search-reference-jql-functions/)
