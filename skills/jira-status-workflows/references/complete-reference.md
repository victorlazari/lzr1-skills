# Complete Reference: Jira Status & Workflows

## Authoritative Sources
- [Atlassian Jira Cloud Workflow Documentation](https://support.atlassian.com/jira-cloud-administration/docs/work-with-issue-workflows/) (Verified against upstream: 2026-08-07)
- [ScriptRunner for Jira Cloud HAPI Documentation](https://docs.adaptavist.com/sr4jc/latest/features/scriptrunner-hapi) (Verified against upstream: 2026-08-07)
- [Jira Service Management Workflows](https://support.atlassian.com/jira-service-management-cloud/docs/configure-request-types-and-workflows/) (Verified against upstream: 2026-08-07)

## Workflow Properties
Workflow properties allow you to control the behavior of issues in specific statuses.

- `jira.issue.editable`: Set to `false` to prevent users from editing issues in a specific status (e.g., "Closed" or "Done").
- `jira.permission.comment.denied`: Set to `true` to prevent users from commenting on issues in a specific status.

## Development Tool Triggers
Development tool triggers allow you to automatically transition issues based on events in connected development tools (e.g., Bitbucket, GitHub, GitLab).

- **Branch created:** Transition an issue when a branch is created.
- **Commit created:** Transition an issue when a commit is created.
- **Pull request created:** Transition an issue when a pull request is created.
- **Pull request merged:** Transition an issue when a pull request is merged.
- **Pull request declined:** Transition an issue when a pull request is declined.

## ScriptRunner HAPI
ScriptRunner for Jira Cloud provides a simplified Groovy scripting API called HAPI.

**Example: Transition an issue**
```groovy
import com.adaptavist.hapi.jira.issues.Issues

def issue = Issues.getByKey("PROJ-123")
issue.transition("In Progress")
```

**Example: Update a custom field**
```groovy
import com.adaptavist.hapi.jira.issues.Issues

def issue = Issues.getByKey("PROJ-123")
issue.update {
    setCustomFieldValue("My Custom Field", "New Value")
}
```
