# GraphQL API Reference

**Verified against upstream:** 2026-08-07
**Primary Source:** https://docs.requarks.io/dev/api

This reference covers authenticating and executing common GraphQL operations in Wiki.js.

## Authentication

API requests require a Bearer token. Generate an API token in the Wiki.js Administration panel under **API Access**.

Include the token in the `Authorization` header:
`Authorization: Bearer YOUR_API_TOKEN`

## Common Queries

### Get Instance Version
```graphql
query {
  site {
    info {
      version
    }
  }
}
```

### List Pages
```graphql
query {
  pages {
    list {
      id
      path
      title
    }
  }
}
```

## Common Mutations

**Warning:** Mutations that modify or delete data require explicit user confirmation before execution.

### Create Page
```graphql
mutation {
  pages {
    create(
      content: "Page content here",
      description: "Page description",
      editor: "markdown",
      isPublished: true,
      isPrivate: false,
      locale: "en",
      path: "/new-page",
      tags: ["tag1", "tag2"],
      title: "New Page Title"
    ) {
      responseResult {
        succeeded
        errorCode
        slug
        message
      }
      page {
        id
      }
    }
  }
}
```
