# Jira Field Schemas: Complete Reference

## 1. Architectural Overview: Fields in Jira

Fields in Jira are metadata containers attached to issues (work items). Each field holds a specific piece of information—text, number, date, user, option set, or asset reference—that defines the issue's attributes. Fields are categorized as **System Fields** (built-in, immutable types like Summary, Assignee, Status) or **Custom Fields** (created by administrators to fit organizational needs).

### 1.1. Core Components of Field Architecture

| Component                   | Description                                                                                                     |
|-----------------------------|-----------------------------------------------------------------------------------------------------------------|
| **Field**                   | The atomic data element; defined by type (text, user picker, select list, etc.), name, and description.         |
| **Field Context**           | Defines scope and restrictions of a field: which projects (spaces) and issue types (work types) it applies to, along with default values and option sets. |
| **Field Configuration**     | Defines field behavior (required, optional, hidden), descriptions, and renderers (wiki vs plain text) within a context. |
| **Field Configuration Scheme** | Maps multiple field configurations to specific issue types, enabling different field behaviors per issue type in a project. |
| **Screen**                  | UI construct determining which fields are displayed when creating, editing, or viewing issues.                  |
| **Screen Scheme**           | Maps screens to operations (Create, Edit, View).                                                                |
| **Issue Type Screen Scheme** | Maps screen schemes to issue types within a project.                                                            |
| **Project (Space)**         | Container for issues; associates a set of schemes (field configuration, screen, workflow) to control issue behavior. |

## 2. Advanced Field Contexts: Controlling Scope, Defaults, and Restrictions

Field Contexts represent one of the most powerful yet underutilized mechanisms for fine-grained control over field behavior in Jira. They enable administrators to tailor fields dynamically across different projects or issue types.

### 2.1. Purpose and Mechanics of Field Contexts

Every custom field can have multiple **contexts**. Each context defines the subset of projects and issue types where the field applies. This facilitates scenarios where the same field behaves differently across projects or where it is present only in certain issue types.

### 2.2. Default Values per Context

Field contexts allow setting **default values** scoped to that context. This means that when creating a new issue in a project or issue type covered by that context, the field's value is pre-populated with the specified default, improving data consistency and reducing user input.

### 2.3. Custom Option Sets per Context

Fields with predefined options (e.g., select lists, radio buttons, checkboxes) can have **option sets customized per context**. This allows the same field to present different options depending on the project or issue type, a critical feature for global fields that must adapt to different organizational units.

### 2.4. User Picker Restrictions in Contexts

User picker fields (single or multi-select) can be restricted by context to only show users from certain **groups** or **space roles**. This prevents irrelevant or unauthorized users from being selected in certain projects or issue types.

## 3. Complex Interplay: Fields, Screens, Screen Schemes, and Issue Type Screen Schemes

Understanding the UI path of fields—how they are surfaced to users—is critical for building maintainable and scalable schemes.

### 3.1. Screens and Field Presentation

A **Screen** is a collection of fields presented together during a specific operation: creating, editing, viewing, or transitioning an issue. Each screen defines which fields appear and the order of their display.

### 3.2. Screen Schemes: Mapping Screens to Operations

A **Screen Scheme** maps three operations—Create, Edit, View—to screens. For example, a screen scheme might specify that the "Incident Create Screen" is used during issue creation, "Incident Edit Screen" during editing, and "Incident View Screen" when viewing.

### 3.3. Issue Type Screen Schemes: Mapping Screen Schemes to Work Types

The **Issue Type Screen Scheme** maps screen schemes to issue types (work types). This means that different issue types in the same project can have completely different UI setups for create/edit/view operations.

### 3.4. Fields and Screens: Visibility Control

Fields only appear to users if they are included in screens. This is an important point: even if a field is configured to be visible and required in its field configuration, if it is not added to the screen(s) used by the project and issue type, it will not be seen or editable.

## 4. Designing Enterprise-Grade Field Schemas at Scale

Organizations with hundreds of projects and complex issue hierarchies face unique challenges in field schema design. Scaling thoughtfully ensures performance, maintainability, and adherence to Jira Cloud’s field limits.

### 4.1. Field Limits and Upcoming 2026 Changes

Jira Cloud imposes limits on field configurations and schemes to ensure performance and reliability:

- A **Field Configuration** can include up to **700 fields**.
- A **Field Configuration Scheme** can map up to **150 issue types**.
- Projects can associate only one field configuration scheme at a time.

In **February 2026**, Atlassian will retire traditional field configurations and configuration schemes, replacing them with a unified **Field Schemes** experience.

### 4.2. Field Schema Design Principles

- **Avoid redundant fields**: Reuse fields wherever possible rather than creating new similar fields.
- **Leverage Field Contexts**: Use contexts to vary field options and defaults instead of creating separate fields per project.
- **Limit field visibility via screens**: Do not add fields to screens unnecessarily.
- **Group issue types logically**: Map similar issue types to the same field configuration to reduce the number of schemes.
- **Consolidate screens and screen schemes**: Reuse screens and schemes across projects and issue types to ease administration.
- **Document field usage**: Maintain a field dictionary to track field purposes, contexts, and associated projects.

## 5. The New Unified Field Schemes Experience (2026 Update)

Atlassian is evolving Jira’s field management model with a **unified Field Schemes** experience, retiring Field Configurations and Field Configuration Schemes.

### 5.1. Key Differences in the Unified Model

- **Field contexts will no longer restrict field visibility or options.** Instead, visibility rules are enforced via the new Field Schemes interface.
- Field schemes will combine configuration and context settings into a single construct, reducing fragmentation.
- The new model will better support dynamic changes and scaling.
- Deprecated entities (Field Configurations, Field Configuration Schemes) will be phased out, with migration tooling provided.

## 6. REST API Schema Details for Field Management

Administrators and architects can leverage Jira’s REST API to audit, create, and manage fields, contexts, and schemes programmatically.

### 6.1. Field Schema JSON Structure

Each field returned by the API includes these attributes:

| Attribute    | Description                                                                                                     |
|--------------|-----------------------------------------------------------------------------------------------------------------|
| `id`         | Unique identifier of the field                                                                                   |
| `name`       | Display name of the field                                                                                        |
| `type`       | Data type (string, number, date, datetime, option, user, group, version, etc.)                                   |
| `system`     | System field identifier if applicable (e.g., summary, assignee)                                                 |
| `custom`     | Custom field type identifier (e.g., com.atlassian.jira.plugin.system.customfieldtypes:textfield)                  |
| `customId`   | Numeric ID of the custom field                                                                                   |
| `items`      | For array types, the data type of array elements                                                                |
| `contexts`   | List of field contexts and their options (for fields with predefined options)                                    |

## 7. Jira Field Schemas CLI Reference

The `jira-field-schemas` command-line interface (CLI) serves as a powerful tool for Jira administrators and developers to interact with Jira field schemas programmatically.

### 7.1. Key Commands

- `init`: Initializes a new field schema.
- `list`: Retrieves a list of all field schemas.
- `get`: Retrieves detailed information about a specific field schema.
- `create`: Creates a new field schema.
- `update`: Modifies an existing field schema.
- `delete`: Removes an existing field schema.
- `assign`: Associates a field schema with a project or issue type.
- `unassign`: Removes the association of a field schema from a project or issue type.

## 8. Security Audit Checklist

### 8.1. Access Controls

- Verify that only authorized administrators have permission to modify field schemas.
- Review role-based access controls (RBAC) for field configuration management.

### 8.2. Field Visibility

- Ensure sensitive fields are not visible on public or unauthorized screens.
- Audit field contexts to confirm user picker restrictions are correctly applied.

### 8.3. Data Integrity

- Check for conflicting field types or names across projects.
- Validate default values and required field settings to prevent data entry errors.

### 8.4. Compliance

- Ensure field configurations comply with organizational data privacy policies (e.g., GDPR, HIPAA).
- Maintain an audit trail of schema changes for compliance reporting.
