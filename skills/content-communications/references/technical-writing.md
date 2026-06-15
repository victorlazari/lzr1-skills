# Technical Writing

## Table of Contents
1. Documentation Types
2. Writing Standards
3. API Documentation
4. Developer Experience
5. Documentation Architecture

---

## 1. Documentation Types

### Documentation Quadrant (Divio System)

| Type | Purpose | Analogy | Example |
|---|---|---|---|
| Tutorials | Learning-oriented | Teaching a child to cook | "Getting Started with X" |
| How-to guides | Problem-oriented | Recipe in a cookbook | "How to deploy to production" |
| Explanation | Understanding-oriented | Article on culinary history | "How authentication works" |
| Reference | Information-oriented | Encyclopedia entry | "API endpoint reference" |

### Documentation Hierarchy

```
docs/
├── getting-started/
│   ├── quickstart.md
│   ├── installation.md
│   └── first-project.md
├── guides/
│   ├── authentication.md
│   ├── deployment.md
│   └── migration.md
├── concepts/
│   ├── architecture.md
│   ├── data-model.md
│   └── security.md
├── reference/
│   ├── api/
│   ├── cli/
│   ├── configuration.md
│   └── errors.md
├── tutorials/
│   ├── build-a-todo-app.md
│   └── integrate-with-slack.md
└── changelog.md
```

---

## 2. Writing Standards

### Style Principles

| Principle | Description | Example |
|---|---|---|
| Active voice | Subject performs the action | "Click the button" not "The button should be clicked" |
| Present tense | Describe current state | "The API returns" not "The API will return" |
| Second person | Address the reader directly | "You can configure" not "Users can configure" |
| Concise | Remove unnecessary words | "To start" not "In order to start" |
| Specific | Concrete over abstract | "Enter your API key" not "Enter the required credentials" |
| Consistent | Same terms throughout | Pick "click" or "select" and stick with it |

### Formatting Standards

| Element | Standard |
|---|---|
| Headings | Sentence case, descriptive |
| Code | Inline for short, blocks for multi-line |
| Lists | Parallel structure, consistent punctuation |
| Links | Descriptive text, not "click here" |
| Images | Alt text, captions, annotated screenshots |
| Callouts | Note, Warning, Tip, Important |
| Tables | For comparing options or listing parameters |

---

## 3. API Documentation

### API Reference Structure

```markdown
## Endpoint Name

Brief description of what this endpoint does.

### Request

`POST /api/v1/resource`

#### Headers

| Header | Required | Description |
|---|---|---|
| Authorization | Yes | Bearer token |
| Content-Type | Yes | application/json |

#### Body Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| name | string | Yes | Resource name (max 255 chars) |
| type | enum | Yes | One of: "a", "b", "c" |
| metadata | object | No | Additional key-value pairs |

#### Example Request

```json
{
  "name": "My Resource",
  "type": "a",
  "metadata": {"key": "value"}
}
```

### Response

#### Success (201 Created)

```json
{
  "id": "res_abc123",
  "name": "My Resource",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Errors

| Code | Description |
|---|---|
| 400 | Invalid request body |
| 401 | Authentication required |
| 409 | Resource already exists |
```

---

## 4. Developer Experience

### Developer Journey

| Stage | Content Needed | Goal |
|---|---|---|
| Discover | Landing page, overview | Understand value proposition |
| Evaluate | Quickstart, pricing, comparison | Decide to try |
| Learn | Tutorials, getting started | First success in <5 min |
| Build | Guides, reference, examples | Productive development |
| Scale | Architecture, best practices | Production readiness |
| Troubleshoot | Error reference, FAQ, support | Unblock quickly |

### Code Examples Best Practices

| Practice | Description |
|---|---|
| Complete | Runnable without modification |
| Commented | Explain non-obvious parts |
| Realistic | Use real-world scenarios |
| Multi-language | Show in popular languages |
| Copy-friendly | Easy to copy and paste |
| Tested | Verified to work with current version |
| Progressive | Simple first, then advanced |

---

## 5. Documentation Architecture

### Docs-as-Code Workflow

```
Write (Markdown) → Review (PR) → Build (SSG) → Deploy (CI/CD) → Measure (Analytics)

Tools:
- Writing: VS Code, any text editor
- Source: Git (GitHub/GitLab)
- Build: Docusaurus, MkDocs, GitBook, Nextra
- Review: Pull requests, technical review
- Deploy: Vercel, Netlify, GitHub Pages
- Measure: Google Analytics, Plausible
```

### Documentation Platforms

| Platform | Best For | Features |
|---|---|---|
| Docusaurus | Open source, developer docs | React, versioning, search |
| GitBook | Team docs, internal wikis | WYSIWYG, collaboration |
| MkDocs (Material) | Python projects | Markdown, themes, plugins |
| Readme.com | API documentation | Interactive API explorer |
| Notion | Internal docs | Collaboration, databases |
| Confluence | Enterprise | Integration with Jira |
| Mintlify | Modern API docs | Beautiful defaults, MDX |
