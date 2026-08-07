# Jira Field Schemas: Complete Reference

**Verified against upstream:** 2026-08-07

## 1. Architectural Overview: Unified Field Schemes (2026 Model)

In 2026, Jira transitioned from the legacy Field Configurations and Field Configuration Schemes to a unified **Field Schemes** experience. This new model serves as the single source of truth for which work types a field can appear on within a Space (Project).

### 1.1. Core Components

| Component | Description |
|---|---|
| **Field** | The atomic data element; defined by type (text, user picker, select list, etc.), name, and description. |
| **Field Scheme** | The unified construct that defines field visibility and behavior across work types within a space. Replaces legacy configurations and schemes. |
| **Field Context** | Defines default values and available options for a field. **Crucially, contexts no longer control field visibility.** Every field has a global context that cannot be deleted. |
| **Screen** | UI construct determining which fields are displayed when creating, editing, or viewing issues. |
| **Screen Scheme** | Maps screens to operations (Create, Edit, View). |
| **Issue Type Screen Scheme** | Maps screen schemes to issue types within a project. |
| **Space (Project)** | Container for issues; associates a Field Scheme to control issue behavior. |

## 2. Field Contexts: Defaults and Options

Under the unified model, Field Contexts have a narrower, more focused role. They no longer restrict where a field can be used.

### 2.1. Default Values and Options

Field Contexts are used exclusively to set default values and define custom option sets (for fields like select lists or radio buttons). This allows a field to have different default behaviors or available choices depending on the context, without affecting its overall visibility in the space.

### 2.2. Global Context

Every field now possesses a global context that cannot be deleted. This ensures a baseline configuration is always available.

## 3. System Limits

To ensure performance and reliability, Jira enforces strict limits on the new Field Schemes architecture:

- **Fields per Space:** A maximum of **700 fields** can be associated with a single space.
- **Work Types per Scheme:** A Field Scheme can map up to **150 work types** (issue types).

Exceeding these limits will result in API errors and degraded performance. Regular auditing is required to maintain compliance.

## 4. REST API: Field Scheme Model

The Jira REST API has been updated to support the unified Field Schemes model (RFC 103, 104, 105, 121).

### 4.1. Key Endpoints

- `GET /rest/api/3/field/search`: Retrieve all fields.
- `GET /rest/api/3/fieldscheme`: Retrieve all Field Schemes.
- `POST /rest/api/3/fieldscheme`: Create a new Field Scheme.
- `PUT /rest/api/3/fieldscheme/{id}`: Update an existing Field Scheme.
- `GET /rest/api/3/project/{projectId}/fieldscheme`: Get the Field Scheme associated with a specific space.

*Note: The legacy endpoints for Field Configurations and Field Configuration Schemes are deprecated and should not be used on migrated instances.*
