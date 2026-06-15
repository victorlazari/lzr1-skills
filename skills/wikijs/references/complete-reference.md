# Specialist: 46-wikijs

## === FILE: 46-wikijs-advanced.md ===
# Wiki.js Advanced Patterns and Operations Guide

Wiki.js is a powerful, open-source modern wiki platform built on Node.js, Vue.js, and GraphQL. As organizations scale their documentation needs, moving beyond basic page creation becomes essential. This comprehensive guide delves into the advanced patterns, configurations, and operational strategies required to manage a production-grade Wiki.js instance. From bidirectional Git synchronization and rendering pipeline customization to performance optimization and custom extension building, this document serves as the definitive resource for Wiki.js administrators and advanced users.

## 1. Git Storage Synchronization

One of the most powerful features of Wiki.js is its ability to synchronize content with external storage backends. Among the 11 supported storage backends, Git stands out for its version control capabilities, enabling a docs-as-code workflow.

### Bidirectional Sync

Wiki.js supports bidirectional synchronization with Git repositories. This means that changes made within the Wiki.js web interface are automatically committed and pushed to the Git repository, while changes pushed directly to the Git repository (e.g., via a developer's local IDE) are pulled and reflected in the wiki. This bidirectional flow ensures that technical writers and developers can collaborate seamlessly using their preferred tools.

To configure bidirectional sync, administrators must define the target repository URL, branch, and authentication credentials in the Wiki.js storage settings. The synchronization interval can be customized, or webhooks can be employed to trigger immediate pulls upon repository updates. It is crucial to ensure that the Git user configured in Wiki.js has both read and write permissions to the repository.

### Conflict Resolution

While bidirectional sync is powerful, it introduces the potential for conflicts, particularly when a page is edited simultaneously in the web interface and the Git repository. Wiki.js handles conflicts by prioritizing the database state. If a conflict occurs during a pull operation, the system will attempt to merge the changes. If an automatic merge is not possible, the sync operation may fail, requiring manual intervention.

To mitigate conflicts, it is recommended to establish clear workflows. For instance, designate specific sections of the wiki for web-based editing and others for Git-based editing. Additionally, leveraging the automatic snapshot feature in Wiki.js ensures that a version history is maintained for every update, allowing administrators to revert to a previous state if a conflict corrupts a page.

### SSH vs HTTPS Authentication

When configuring Git storage, administrators must choose between SSH and HTTPS authentication. 

**HTTPS Authentication:** This method requires a username and a personal access token (PAT) or password. It is generally easier to set up and is less prone to firewall restrictions. However, managing PATs can be cumbersome, especially when dealing with token expiration and rotation policies.

**SSH Authentication:** SSH relies on public/private key pairs, offering a more secure and robust authentication mechanism. To use SSH, administrators must generate an SSH key pair on the server hosting Wiki.js and add the public key to the Git provider (e.g., GitHub, GitLab). This method eliminates the need for passwords and tokens, making it ideal for automated, long-term synchronization. Ensure that the private key is securely stored and accessible only by the Wiki.js process.

## 2. Multi-Language and Locale Support

In a globalized environment, documentation must cater to diverse audiences. Wiki.js provides robust multi-language and locale support, allowing administrators to create and manage content in multiple languages seamlessly.

### Locale Configuration

Wiki.js supports a wide array of locales. Administrators can define the default locale for the wiki and enable additional locales as needed. Each page in Wiki.js is associated with a specific locale, and the system uses the `locale` parameter in conjunction with the `path` and `privateNS` to generate a unique SHA1 hash for the page.

### Page Migration and Translation

When expanding documentation to new languages, Wiki.js facilitates page migration and translation. Users can create a new version of an existing page in a different locale. The system maintains a link between the different language versions of a page, allowing users to switch seamlessly between translations using the language selector in the user interface.

It is important to note that Wiki.js does not automatically translate content. Administrators must rely on manual translation or integrate third-party translation services. When migrating pages, ensure that the path structure remains consistent across locales to maintain a logical hierarchy and facilitate easy navigation.

## 3. Custom CSS and JS Injection

To align the wiki with corporate branding or to introduce custom interactivity, Wiki.js allows the injection of custom Cascading Style Sheets (CSS) and JavaScript (JS).

### Global vs Per-Page Injection

Administrators can inject CSS and JS globally, affecting the entire wiki, or on a per-page basis. Global injection is configured in the administration panel under the "Theme" settings. This is ideal for applying brand colors, typography, and global navigation modifications.

Per-page injection provides granular control, allowing specific styles or scripts to be applied only to individual pages. This is particularly useful for creating interactive dashboards, custom calculators, or unique layouts for specific documentation sections.

### Lifecycle Hooks and Security

When injecting custom JS, it is crucial to understand the Wiki.js lifecycle. Because Wiki.js is a single-page application (SPA) built with Vue.js, standard DOM load events may not fire as expected when navigating between pages. To ensure that custom scripts execute correctly, developers must use the provided lifecycle hooks. Specifically, custom JS must use `window.boot.register('page-ready', callback)` to execute code after a page has fully rendered.

Security is a paramount concern when allowing custom JS injection. By default, Wiki.js employs a security sanitizer that strips custom HTML and potentially malicious scripts. Administrators must carefully manage permissions, granting the `write:styles` and `write:scripts` permissions only to trusted users.

## 4. Rendering Pipeline Customization

Wiki.js features a highly customizable rendering pipeline, supporting 14 Markdown rendering extensions and 11 HTML post-processing extensions. This flexibility allows administrators to tailor the rendering process to their specific needs.

### Enabling and Disabling Extensions

Administrators can enable or disable specific extensions in the administration panel. For instance, if the wiki does not require mathematical rendering, the KaTeX and MathJax extensions can be disabled to improve rendering performance. Conversely, enabling extensions like `emoji`, `tasklists`, and `footnotes` can significantly enhance the richness of the documentation.

### Mathematical Rendering: KaTeX vs MathJax

For technical documentation requiring mathematical formulas, Wiki.js offers two primary rendering engines: KaTeX and MathJax.

**KaTeX:** Known for its exceptional rendering speed, KaTeX is the preferred choice for wikis with extensive mathematical content. It renders formulas synchronously and does not require heavy client-side processing, resulting in faster page load times.

**MathJax:** While slightly slower than KaTeX, MathJax offers broader compatibility and supports a wider range of LaTeX macros and extensions. It is highly configurable and provides excellent accessibility features. Administrators should choose the engine that best balances performance and feature requirements.

### Diagramming: Mermaid, PlantUML, and Kroki

Visualizing complex architectures and workflows is essential in technical documentation. Wiki.js supports several diagramming tools:

**Mermaid:** A JavaScript-based diagramming and charting tool that renders Markdown-inspired text definitions dynamically in the browser. It is lightweight and ideal for flowcharts, sequence diagrams, and Gantt charts.

**PlantUML:** A versatile tool that generates UML diagrams from a specialized text language. PlantUML requires a backend server to render the diagrams into images. Wiki.js can be configured to point to a public or self-hosted PlantUML server.

**Kroki:** A unified API that provides access to multiple diagramming libraries, including BlockDiag, GraphViz, and Nomnoml. By integrating Kroki, Wiki.js users can leverage a vast array of diagramming tools through a single interface.

## 5. Advanced Content Components

Beyond standard text and images, Wiki.js supports advanced content components that enhance the interactivity and organization of documentation.

### Tabsets

Tabsets allow authors to group related content into selectable tabs, reducing page clutter and improving readability. This is particularly useful for providing code examples in multiple programming languages or presenting step-by-step instructions for different operating systems. The `tabset` HTML post-processing extension must be enabled to utilize this feature.

### Pivot Tables

For data-heavy documentation, the `pivot-table` Markdown extension enables the creation of interactive pivot tables directly within the wiki. Authors can define the data source and configuration parameters, allowing users to dynamically aggregate, filter, and analyze data without leaving the page.

### Task Lists

The `tasklists` extension transforms standard Markdown lists into interactive checklists. This feature is invaluable for creating onboarding guides, deployment checklists, and project tracking pages. Users can check and uncheck items, providing a visual indication of progress.

## 6. Building Custom Extensions

While Wiki.js offers a rich set of built-in extensions, organizations may require custom functionality. Wiki.js supports the integration of external tools and the development of custom extensions.

### Pandoc Integration

Pandoc is a universal document converter that can transform files between numerous formats (e.g., Markdown, HTML, Word, PDF). By integrating Pandoc, Wiki.js can support advanced document import and export capabilities. Administrators must install Pandoc on the host server and configure the Wiki.js Pandoc extension to define the conversion parameters and supported formats.

### Puppeteer and Sharp

For advanced rendering and image processing, Wiki.js can leverage Puppeteer and Sharp.

**Puppeteer:** A Node library that provides a high-level API to control headless Chrome or Chromium. In the context of Wiki.js, Puppeteer can be used to generate high-quality PDF exports of wiki pages, ensuring that the layout and styling are preserved perfectly.

**Sharp:** A high-performance Node.js image processing library. Integrating Sharp allows Wiki.js to automatically resize, compress, and optimize uploaded images, significantly improving page load times and reducing storage consumption.

## 7. CleanCSS Minification

To optimize the delivery of CSS assets, Wiki.js utilizes CleanCSS for minification. CleanCSS is a fast and efficient CSS optimizer that removes whitespace, comments, and redundant rules, resulting in smaller file sizes and faster download times.

Administrators can configure the CleanCSS integration to define the level of optimization and compatibility settings. It is important to note that aggressive minification can sometimes break complex CSS rules. Therefore, it is recommended to test custom styles thoroughly after enabling minification. Additionally, when using external optimization services like Cloudflare, administrators must disable features like Auto Minify, Mirage, and Rocket Loader, as they can conflict with Wiki.js's internal asset management and break the rendering pipeline.

## 8. Page Tree Management and Tag System

Organizing content effectively is crucial for maintaining a usable wiki. Wiki.js provides robust tools for structuring and categorizing pages.

### Page Tree Management

Wiki.js employs a hierarchical page tree structure, allowing administrators to organize content into logical folders and subfolders. The page path dictates its position in the tree. It is important to adhere to the path rules: no dots, spaces, backslashes, or double slashes, and no starting or ending slashes.

Administrators can manage the page tree through the administration panel, moving, renaming, and deleting pages as needed. When a page is moved or renamed, Wiki.js automatically updates internal links to prevent broken references.

### Tag System

In addition to the hierarchical structure, Wiki.js features a flexible tag system. Authors can assign multiple tags to a page, enabling cross-categorization and faceted search. Tags are particularly useful for grouping related content that spans different sections of the page tree, such as "troubleshooting," "api," or "deprecated."

Administrators can manage the global tag vocabulary, merging duplicate tags and deleting obsolete ones to maintain a clean and consistent taxonomy.

## 9. Scheduled Publishing

For organizations that require strict control over content release cycles, Wiki.js supports scheduled publishing. Authors can define a `publishStartDate` and a `publishEndDate` in the page metadata.

**Publish Start Date:** The page will remain hidden from standard users until the specified date and time. This is ideal for preparing release notes, announcements, or embargoed documentation in advance.

**Publish End Date:** The page will automatically become inaccessible to standard users after the specified date and time. This is useful for time-sensitive content, such as promotional offers or temporary event information.

Administrators and users with the `manage:pages` permission can view and edit scheduled pages regardless of the current date.

## 10. Private Pages and Namespaces

Security and access control are paramount in enterprise environments. Wiki.js provides granular permissions to restrict access to sensitive information.

### Private Pages

Authors can designate individual pages as private, restricting access to specific users or groups. This is useful for drafting content, storing internal notes, or sharing confidential information with a limited audience.

### Namespaces

For broader access control, administrators can utilize namespaces. A namespace is a distinct section of the wiki with its own set of permissions and configurations. By assigning pages to a private namespace, administrators can ensure that only authorized users can view, edit, or manage the content within that namespace. The page hash generation incorporates the `privateNS` parameter, ensuring cryptographic separation between public and private content.

## 11. Asset Management

Effective asset management is essential for maintaining a performant and organized wiki. Wiki.js provides a centralized asset manager for uploading, organizing, and inserting images, documents, and other files.

Administrators can define the maximum file size for uploads and restrict the allowed file types to prevent the distribution of malicious content. The asset manager supports folder structures, allowing users to categorize assets logically.

When integrating with external storage backends like S3 or Azure Blob Storage, Wiki.js can offload asset storage, reducing the burden on the local server and leveraging the scalability and durability of cloud storage providers.

## 12. Performance Optimization

As a Wiki.js instance grows in content and user base, performance optimization becomes critical. Administrators must implement strategies to ensure fast response times and high availability.

### Connection Pooling

Wiki.js relies heavily on its database backend (PostgreSQL is recommended and required for High Availability). To optimize database interactions, administrators must configure connection pooling in the `config.yml` file. Connection pooling maintains a cache of database connections, reducing the overhead of establishing new connections for every request. Properly tuning the pool size based on the server's resources and expected traffic is essential for preventing database bottlenecks.

### Caching Strategies

Caching is a highly effective technique for improving read performance. Wiki.js supports various caching mechanisms to reduce database load and accelerate page rendering.

**In-Memory Caching:** Wiki.js utilizes in-memory caching for frequently accessed data, such as configuration settings and user permissions.

**Page Caching:** For static content, administrators can implement page caching using a reverse proxy like Nginx or Redis. This allows the server to serve pre-rendered HTML pages directly from the cache, bypassing the Node.js application entirely.

### CDN Integration

To optimize the delivery of static assets (CSS, JS, images) to a global audience, administrators should integrate a Content Delivery Network (CDN). A CDN caches assets on edge servers distributed worldwide, reducing latency and improving load times for users geographically distant from the origin server.

When configuring a CDN, ensure that the Wiki.js `bindIP` and `port` settings are correctly configured to handle forwarded requests. As mentioned earlier, disable aggressive optimization features on the CDN (e.g., Cloudflare's Auto Minify) to prevent conflicts with Wiki.js's internal asset management.

## 13. Known Limitations and Workarounds

While Wiki.js is a robust platform, it has certain limitations that administrators must be aware of. Understanding these limitations and implementing appropriate workarounds is crucial for maintaining a stable production environment.

1. **Subfolder Installation:** Wiki.js cannot be installed in a subfolder (e.g., `example.com/wiki`). It must be hosted on a dedicated subdomain or root domain (e.g., `wiki.example.com`).
2. **Real-Time Collaborative Editing:** Wiki.js does not currently support real-time collaborative editing (like Google Docs). Users must coordinate edits to avoid conflicts, or rely on Git storage synchronization for version control.
3. **High Availability (HA) Mode:** HA mode requires PostgreSQL. SQLite cannot be used in HA mode due to its file-based nature and lack of concurrent write support. To enable HA, set `ha: true` in `config.yml`.
4. **MySQL Authentication:** MySQL `caching_sha2_password` is not supported. Administrators must configure MySQL to use `mysql_native_password` for the Wiki.js database user.
5. **Editor Conversion:** Converting content between different editors (e.g., from Markdown to WYSIWYG) may result in formatting loss. It is recommended to choose an editor and stick with it for a given page.
6. **Custom HTML Stripping:** By default, the security sanitizer strips custom HTML. To use custom HTML, administrators must disable the sanitizer or carefully configure allowed tags, balancing functionality with security risks.
7. **API Rate Limiting:** Wiki.js does not have native API rate limiting. To protect the GraphQL endpoint from abuse, administrators must implement rate limiting at the reverse proxy level (e.g., using Nginx `limit_req`).
8. **Git Sync Conflicts:** As discussed, Git storage sync can conflict with direct database edits. Establish clear workflows to minimize concurrent modifications.
9. **Page Path Restrictions:** Page paths cannot contain dots, spaces, or special characters. Use hyphens for separation and adhere strictly to the path rules.
10. **Cloudflare Optimizations:** Cloudflare's Auto Minify, Mirage, and Rocket Loader break Wiki.js assets. These features must be disabled for the Wiki.js domain.
11. **Docker Updates:** When deploying via Docker, the `wiki-update-companion` container must be updated separately from the main `wiki` container to ensure smooth version upgrades.
12. **Custom JS Execution:** Custom JS must use `window.boot.register('page-ready', callback)` to execute reliably within the SPA architecture.
13. **Port Binding:** Binding Wiki.js to a port lower than 1024 (e.g., 80 or 443) requires special privileges. Use `setcap` to grant the Node.js binary permission, or use `iptables` to redirect traffic from a higher port.

## 14. Conclusion

Managing a production-grade Wiki.js instance requires a deep understanding of its architecture, configuration options, and operational nuances. By leveraging advanced patterns such as Git synchronization, rendering pipeline customization, and robust performance optimization strategies, administrators can build a highly scalable, secure, and performant documentation platform. Adhering to best practices and understanding the platform's limitations ensures a seamless experience for both content creators and consumers, solidifying Wiki.js as a premier choice for modern knowledge management.

## === FILE: 46-wikijs-cli-reference.md ===
# Wiki.js CLI and API Reference Guide

## Introduction

Wiki.js is a powerful, modern, and open-source wiki platform built on Node.js, Vue.js, and GraphQL. As an enterprise-grade knowledge management system, it provides extensive capabilities for automation, integration, and administration through its GraphQL API and various command-line interfaces. This comprehensive reference guide is designed for system administrators, DevOps engineers, and developers who need to interact with Wiki.js programmatically or manage its infrastructure from the command line.

Wiki.js v2.x, the current stable version, exposes almost all of its functionality through a robust GraphQL API endpoint located at `/graphql`. This API is the same one used by the Wiki.js frontend, ensuring that any action possible through the web interface can also be automated via API calls. Furthermore, managing a Wiki.js deployment involves interacting with Docker, Kubernetes, and database command-line tools, especially in high-availability (HA) setups or disaster recovery scenarios.

This document covers the complete spectrum of Wiki.js operations, including GraphQL API authentication, page mutations, page queries, user and group management, asset uploads, Docker and Kubernetes deployment commands, and database-level interventions.

---

## GraphQL API Authentication

All API requests to Wiki.js must be authenticated using a Bearer token. These tokens are generated within the Wiki.js administration panel under the **API Access** section. 

### Generating an API Token

To generate an API token, an administrator must navigate to the Administration area, select API Access, and create a new key. The key can be assigned specific permissions, which map directly to the GraphQL mutations and queries it can execute. Available permissions include `read:pages`, `write:pages`, `manage:pages`, `delete:pages`, `write:styles`, `write:scripts`, `read:source`, `read:history`, and `manage:system`.

### Using the Bearer Token

Once the token is generated, it must be included in the `Authorization` header of every HTTP request made to the `/graphql` endpoint.

**Example cURL Request:**

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN_HERE" \
  -d '{"query": "{ site { title } }"}' \
  https://wiki.example.com/graphql
```

It is crucial to keep this token secure. If a token is compromised, it should be immediately revoked from the administration panel. There is no native API rate limiting in Wiki.js; therefore, it is highly recommended to implement rate limiting at the reverse proxy level (e.g., NGINX, Traefik, or Cloudflare) to prevent abuse of the API endpoint.

---

## Page Mutations

Page mutations allow you to create, update, move, delete, and manage the lifecycle of wiki pages programmatically. Wiki.js supports multiple editors, including `markdown`, `wysiwyg`, `ckeditor`, `code`, `api`, and `asciidoc`. When creating or updating a page, you must specify the content type corresponding to the editor used.

### Create Page

Creating a new page requires specifying the path, title, content, description, editor type, and locale. Note that page paths cannot contain dots, spaces, backslashes, or double slashes, and must not start or end with a slash.

**GraphQL Mutation:**

```graphql
mutation {
  pages {
    create(
      content: "# Hello World\n\nThis is a new page created via API.",
      description: "An example page",
      editor: "markdown",
      isPublished: true,
      isPrivate: false,
      locale: "en",
      path: "development/api-example",
      tags: ["api", "example"],
      title: "API Example Page"
    ) {
      responseResult {
        succeeded
        errorCode
        slug
        message
      }
      page {
        id
        path
        title
      }
    }
  }
}
```

**cURL Example:**

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"query": "mutation { pages { create(content: \"# Hello World\", description: \"Test\", editor: \"markdown\", isPublished: true, isPrivate: false, locale: \"en\", path: \"test-page\", tags: [], title: \"Test Page\") { responseResult { succeeded message } } } }"}' \
  https://wiki.example.com/graphql
```

### Update Page

Updating a page creates an automatic snapshot in the version history. You must provide the page ID and the updated fields.

**GraphQL Mutation:**

```graphql
mutation {
  pages {
    update(
      id: 123,
      content: "# Updated Content\n\nThis page has been updated.",
      description: "Updated description",
      editor: "markdown",
      isPublished: true,
      isPrivate: false,
      locale: "en",
      path: "development/api-example",
      tags: ["api", "updated"],
      title: "Updated API Example"
    ) {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

### Move Page

Moving a page changes its path and/or locale. This operation updates the page hash, which is calculated as `SHA1(locale + path + privateNS)`.

**GraphQL Mutation:**

```graphql
mutation {
  pages {
    move(
      id: 123,
      destinationPath: "development/new-api-example",
      destinationLocale: "en"
    ) {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

### Delete Page

Deleting a page removes it from the active wiki. Depending on the configuration, it may be soft-deleted or permanently removed.

**GraphQL Mutation:**

```graphql
mutation {
  pages {
    delete(id: 123) {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

### Convert Page Editor

Converting a page between different editors (e.g., from `markdown` to `wysiwyg`) is possible, but be aware of the known limitation: converting between editors may lose formatting.

**GraphQL Mutation:**

```graphql
mutation {
  pages {
    convert(id: 123, editor: "wysiwyg") {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

### Restore Page Version

You can restore a page to a previous version from its history.

**GraphQL Mutation:**

```graphql
mutation {
  pages {
    restore(id: 123, versionId: 456) {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

### Render Page

Forces the rendering engine to re-process the page content. This is useful if extensions or rendering rules have changed.

**GraphQL Mutation:**

```graphql
mutation {
  pages {
    render(id: 123) {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

### Flush Cache

Flushes the cache for a specific page, ensuring the latest content is served.

**GraphQL Mutation:**

```graphql
mutation {
  pages {
    flushCache(id: 123) {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

### Rebuild Tree

Rebuilds the navigation tree. This is an administrative function typically used when the tree becomes out of sync.

**GraphQL Mutation:**

```graphql
mutation {
  pages {
    rebuildTree {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

### Purge History

Purges the version history for a page, which can be useful for saving database space.

**GraphQL Mutation:**

```graphql
mutation {
  pages {
    purgeHistory(id: 123) {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

### Migrate to Locale

Migrates all pages from one locale to another.

**GraphQL Mutation:**

```graphql
mutation {
  pages {
    migrateToLocale(sourceLocale: "en", targetLocale: "en-US") {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

---

## Page Queries

Page queries allow you to retrieve information about pages, their history, and their relationships.

### List Pages

Retrieves a list of pages, optionally filtered and paginated.

**GraphQL Query:**

```graphql
query {
  pages {
    list(orderBy: TITLE, orderByDirection: ASC) {
      id
      path
      title
      locale
      updatedAt
    }
  }
}
```

### Single Page by ID

Retrieves detailed information about a single page using its ID.

**GraphQL Query:**

```graphql
query {
  pages {
    single(id: 123) {
      id
      path
      title
      content
      description
      editor
      createdAt
      updatedAt
    }
  }
}
```

### Single Page by Path

Retrieves a page using its path and locale.

**GraphQL Query:**

```graphql
query {
  pages {
    singleByPath(path: "development/api-example", locale: "en") {
      id
      title
      content
    }
  }
}
```

### Search Pages

Searches for pages using the configured search engine (e.g., PostgreSQL pg_trgm, Elasticsearch, Algolia).

**GraphQL Query:**

```graphql
query {
  pages {
    search(query: "API documentation") {
      results {
        id
        title
        description
        path
      }
    }
  }
}
```

### Page History

Retrieves the version history of a specific page.

**GraphQL Query:**

```graphql
query {
  pages {
    history(id: 123) {
      versionId
      createdAt
      authorName
      action
    }
  }
}
```

### Page Version

Retrieves the content of a specific historical version of a page.

**GraphQL Query:**

```graphql
query {
  pages {
    version(id: 123, versionId: 456) {
      content
      title
    }
  }
}
```

### Page Tree

Retrieves the hierarchical tree structure of pages.

**GraphQL Query:**

```graphql
query {
  pages {
    tree {
      id
      path
      title
      parent
      isFolder
    }
  }
}
```

### Page Links

Retrieves incoming and outgoing links for a page.

**GraphQL Query:**

```graphql
query {
  pages {
    links(id: 123) {
      incoming {
        id
        path
      }
      outgoing {
        id
        path
      }
    }
  }
}
```

### Page Tags

Retrieves all tags associated with pages.

**GraphQL Query:**

```graphql
query {
  pages {
    tags {
      tag
      count
    }
  }
}
```

### Check Conflicts

Checks for editing conflicts before saving a page. This is crucial since Wiki.js does not support real-time collaborative editing.

**GraphQL Query:**

```graphql
query {
  pages {
    checkConflicts(id: 123, updatedAt: "2023-10-27T10:00:00Z") {
      hasConflict
      latestVersionUpdatedAt
    }
  }
}
```

---

## User and Group Management

Managing users and groups via the API allows for automated onboarding and offboarding processes.

### Create User

**GraphQL Mutation:**

```graphql
mutation {
  users {
    create(
      email: "newuser@example.com",
      name: "New User",
      password: "SecurePassword123!",
      providerKey: "local",
      groups: [2]
    ) {
      responseResult {
        succeeded
        message
      }
      user {
        id
        email
      }
    }
  }
}
```

### Update User

**GraphQL Mutation:**

```graphql
mutation {
  users {
    update(
      id: 45,
      name: "Updated Name",
      groups: [2, 3]
    ) {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

### Delete User

**GraphQL Mutation:**

```graphql
mutation {
  users {
    delete(id: 45) {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

### Create Group

**GraphQL Mutation:**

```graphql
mutation {
  groups {
    create(
      name: "API Developers",
      permissions: ["read:pages", "write:pages"]
    ) {
      responseResult {
        succeeded
        message
      }
      group {
        id
        name
      }
    }
  }
}
```

---

## Asset Upload API

Uploading assets (images, documents) requires a multipart form-data request. The GraphQL API handles the metadata, while the actual file upload is processed through a specific endpoint.

**cURL Example for Asset Upload:**

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -F "mediaUpload=@/path/to/local/image.png" \
  -F "folderId=0" \
  https://wiki.example.com/graphql
```

Note: The exact implementation of asset uploads can vary based on the configured storage backend (e.g., S3, Azure, Local Disk). When using Cloudflare, ensure that Auto Minify, Mirage, and Rocket Loader are disabled, as they can break asset loading and uploads.

---

## Docker CLI Commands

Wiki.js is commonly deployed using Docker. The official image is `ghcr.io/requarks/wiki`. A companion container, `wiki-update-companion`, is used for handling updates.

### Starting the Stack

Using `docker-compose`, you can start the Wiki.js application and its database (preferably PostgreSQL for HA support).

```bash
docker-compose up -d
```

### Stopping the Stack

```bash
docker-compose down
```

### Viewing Logs

To troubleshoot issues, viewing the logs is essential.

```bash
docker-compose logs -f wiki
```

### Executing Commands Inside the Container

Sometimes you need to run commands directly inside the Wiki.js container.

```bash
docker-compose exec wiki /bin/sh
```

### Managing the Update Companion

The `wiki-update-companion` container must be updated separately from the main Wiki.js container. It handles the downloading and extraction of new Wiki.js versions.

```bash
docker pull ghcr.io/requarks/wiki-update-companion:latest
docker-compose restart wiki-update-companion
```

---

## Kubernetes Helm Chart Commands

For enterprise deployments, Kubernetes is often the platform of choice. Wiki.js provides an official Helm chart.

### Add the Helm Repository

```bash
helm repo add requarks https://charts.js.wiki
helm repo update
```

### Install Wiki.js

```bash
helm install my-wiki requarks/wiki -n wiki-namespace --create-namespace
```

### Upgrade Wiki.js

```bash
helm upgrade my-wiki requarks/wiki -n wiki-namespace -f custom-values.yaml
```

### Uninstall Wiki.js

```bash
helm uninstall my-wiki -n wiki-namespace
```

---

## Database CLI Operations

Direct database manipulation is sometimes necessary for disaster recovery, such as resetting an administrator password or fixing configuration issues when the web interface is inaccessible. PostgreSQL is the recommended database and is required for High Availability (HA) mode.

### Connecting to PostgreSQL

```bash
psql -h localhost -U wiki_user -d wiki_db
```

### Resetting an Administrator Password

If you lose access to the admin account, you can reset the password directly in the database. Wiki.js uses bcrypt for password hashing. You must generate a bcrypt hash for your new password and update the database.

1. Generate a bcrypt hash (e.g., using a Node.js script or an online tool). Let's assume the hash for `NewPassword123` is `$2b$10$YourGeneratedHashHere`.
2. Execute the SQL update:

```sql
UPDATE users SET password = '$2b$10$YourGeneratedHashHere' WHERE email = 'admin@example.com';
```

### Manipulating Settings

Wiki.js stores many of its settings in the database. If a setting prevents the application from starting, you can modify it directly.

```sql
-- View all settings
SELECT key, value FROM settings;

-- Update a specific setting (e.g., changing the site URL)
UPDATE settings SET value = '{"host":"https://new-wiki.example.com"}' WHERE key = 'host';
```

### Fixing Git Storage Conflicts

A known limitation is that Git storage synchronization can conflict with direct database edits. If the database and Git repository become out of sync, you may need to manually resolve the conflict by either forcing a push from the database or pulling from Git, depending on which source of truth you prefer. This often involves clearing the `page_history` or adjusting the `pages` table hashes.

---

## Configuration File (`config.yml`)

The `config.yml` file is the core configuration file for Wiki.js. It defines the port, database connection, SSL settings, and more.

**Example `config.yml` Snippet:**

```yaml
port: 3000
bindIP: 0.0.0.0
logLevel: info
ha: true # Requires PostgreSQL
dataPath: ./data
bodyParserLimit: 5mb

db:
  type: postgres
  host: db
  port: 5432
  user: wiki
  pass: wiki_password
  db: wiki
  ssl: false
  pool:
    max: 5
    min: 0
    idle: 10000
```

**Important Notes on Configuration:**
- **HA Mode:** Setting `ha: true` requires PostgreSQL. SQLite cannot be used in HA mode.
- **Ports:** Binding to a port `< 1024` (like 80 or 443) requires `setcap` on the Node.js binary or using `iptables` redirects, as Node.js runs as an unprivileged user by default.
- **MySQL:** If using MySQL 8+, the `caching_sha2_password` plugin is not supported. You must configure the database user to use `mysql_native_password`.

---

## Known Limitations and Workarounds

When operating Wiki.js in a production environment, administrators must be aware of several known limitations:

1. **Subfolder Installation:** Wiki.js cannot be installed in a subfolder (e.g., `example.com/wiki`). It must be hosted on a dedicated subdomain or root domain (e.g., `wiki.example.com`).
2. **Real-time Collaboration:** There is no real-time collaborative editing (like Google Docs). Users must rely on the `checkConflicts` API or UI warnings to avoid overwriting each other's work.
3. **Custom HTML:** Custom HTML is stripped by default by the security sanitizer. To use custom HTML, you must adjust the security settings in the administration panel, understanding the associated XSS risks.
4. **Custom JavaScript:** Any custom JavaScript injected into the site must use the Wiki.js boot sequence: `window.boot.register('page-ready', callback)`. Standard `DOMContentLoaded` events may not fire as expected due to the Vue.js SPA architecture.

## Conclusion

Wiki.js provides a comprehensive and powerful set of tools for programmatic management and automated deployment. By leveraging the GraphQL API, Docker/Kubernetes orchestration, and understanding the underlying database structure, administrators can build highly resilient, automated, and integrated knowledge management systems. Always ensure that API tokens are secured, database backups are regular, and configuration changes are tested in a staging environment before production deployment.


## Deep Dive: Advanced GraphQL Operations

To fully harness the power of Wiki.js, one must understand the intricacies of its GraphQL schema. The schema is self-documenting, meaning you can use tools like GraphQL Playground or Apollo Studio to introspect the API and discover all available queries, mutations, and types.

### Introspection Query

You can fetch the entire schema using an introspection query. This is particularly useful for developers building custom integrations or client applications.

```graphql
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args {
        ...InputValue
      }
    }
  }
}

fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}

fragment InputValue on __InputValue {
  name
  description
  type { ...TypeRef }
  defaultValue
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}
```

### Handling Pagination in Queries

Many queries in Wiki.js, such as listing pages or searching, return paginated results. It is essential to handle pagination correctly to ensure all data is retrieved without overwhelming the server.

```graphql
query {
  pages {
    list(orderBy: TITLE, orderByDirection: ASC, limit: 50, offset: 0) {
      id
      title
    }
  }
}
```

By incrementing the `offset` parameter by the `limit` value in subsequent requests, you can iterate through the entire dataset.

## Storage Backends and Synchronization

Wiki.js supports 11 different storage backends: Azure, Box, DigitalOcean, Disk, Dropbox, Google Drive, Git, OneDrive, S3, S3 Generic, and SFTP. Configuring these backends correctly is vital for data durability and backup strategies.

### Git Storage Backend

The Git storage backend is particularly popular as it allows for version control of the wiki content outside of the database. However, as noted in the limitations, direct database edits can conflict with Git synchronization.

When configuring Git storage, you must provide the repository URL, branch, and authentication credentials (SSH key or username/password). Wiki.js will automatically commit and push changes to the repository whenever a page is created, updated, or deleted.

**Troubleshooting Git Sync:**

If synchronization fails, check the Wiki.js logs for Git-related errors. Common issues include incorrect credentials, network connectivity problems, or merge conflicts. In case of a merge conflict, you may need to manually resolve it by accessing the local Git repository stored within the Wiki.js data directory (usually `./data/repo`) and performing standard Git operations (`git status`, `git merge`, `git push`).

### S3 Storage Backend

Using S3 or S3 Generic (for MinIO, DigitalOcean Spaces, etc.) is highly recommended for storing assets (images, documents) in a High Availability setup. This ensures that all Wiki.js instances in the cluster have access to the same files.

Configuration requires the endpoint URL, region, bucket name, access key, and secret key. Ensure that the bucket permissions are configured correctly to allow Wiki.js to read and write objects.

## Search Engine Integration

Wiki.js supports 8 search engines: Algolia, AWS, Azure, Database (built-in), Elasticsearch, Manticore, PostgreSQL (pg_trgm), Solr, and Sphinx.

### PostgreSQL (pg_trgm)

For most deployments using PostgreSQL, the built-in `pg_trgm` extension provides excellent search capabilities without the need for external services. It uses trigram matching to perform fast full-text searches.

To enable this, ensure the `pg_trgm` extension is installed in your PostgreSQL database:

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

Then, select PostgreSQL as the search engine in the Wiki.js administration panel.

### Elasticsearch

For large-scale enterprise deployments, Elasticsearch offers superior performance and advanced search features. Configuring Elasticsearch requires providing the node URLs and authentication details. Wiki.js will automatically create the necessary indices and keep them synchronized with the page content.

If the search index becomes corrupted or out of sync, you can trigger a full reindex from the administration panel or via the GraphQL API.

## Authentication Modules

With 21 supported authentication modules, Wiki.js can integrate into almost any enterprise identity management system.

### SAML 2.0 Integration

Integrating with SAML 2.0 identity providers (like Okta, OneLogin, or Active Directory Federation Services) requires careful configuration of the Identity Provider (IdP) URL, Issuer URI, and the X.509 certificate.

Wiki.js acts as the Service Provider (SP). You must map the SAML attributes (e.g., email, display name, groups) to the corresponding Wiki.js user properties. This allows for automatic user provisioning and group assignment upon first login.

### OAuth2 and OIDC

OpenID Connect (OIDC) is the modern standard for authentication. Configuring OIDC requires the Client ID, Client Secret, and the Authorization/Token endpoints. Similar to SAML, attribute mapping is crucial for seamless user onboarding.

## Advanced Docker Deployments

While a simple `docker-compose up` is sufficient for testing, production deployments require more robust configurations.

### Docker Swarm

Deploying Wiki.js in a Docker Swarm cluster allows for high availability and load balancing.

**Example `docker-compose.yml` for Swarm:**

```yaml
version: '3.8'
services:
  wiki:
    image: ghcr.io/requarks/wiki:2
    environment:
      DB_TYPE: postgres
      DB_HOST: db
      DB_PORT: 5432
      DB_USER: wiki
      DB_PASS: wiki_password
      DB_NAME: wiki
      HA_ACTIVE: "true"
    networks:
      - wiki-net
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure

  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: wiki
      POSTGRES_USER: wiki
      POSTGRES_PASSWORD: wiki_password
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - wiki-net
    deploy:
      placement:
        constraints:
          - node.role == manager

networks:
  wiki-net:
    driver: overlay

volumes:
  db-data:
```

In this setup, we deploy 3 replicas of the Wiki.js container. The `HA_ACTIVE` environment variable is crucial here, as it tells Wiki.js to use the database for session storage and coordinate cache invalidation across the cluster.

## Performance Tuning and Optimization

To ensure Wiki.js runs smoothly under heavy load, several optimizations can be applied.

### Node.js Memory Limits

By default, Node.js has a memory limit of around 1.5GB. For large wikis, you may need to increase this limit using the `NODE_OPTIONS` environment variable.

```bash
export NODE_OPTIONS="--max-old-space-size=4096"
```

### Database Connection Pooling

The `config.yml` file allows you to configure the database connection pool. For high-traffic sites, increasing the `max` pool size can prevent connection bottlenecks.

```yaml
db:
  pool:
    max: 20
    min: 2
    idle: 10000
```

### Caching Strategies

Wiki.js heavily relies on caching to deliver fast page loads. In a single-node setup, it uses in-memory caching. In an HA setup, it uses Redis (if configured) or the database to coordinate cache invalidation. Ensuring your caching layer is performant is critical.

## Disaster Recovery and Backup

A robust backup strategy is essential for any knowledge management system.

### Database Backups

Since all content, users, and settings are stored in the database, regular database backups are the most critical component of disaster recovery.

For PostgreSQL, use `pg_dump`:

```bash
pg_dump -h localhost -U wiki_user -F c -b -v -f "/backups/wiki_db_$(date +%Y%m%d).backup" wiki_db
```

### Asset Backups

If you are using local disk storage for assets, you must also back up the `data/uploads` directory. If using S3 or another cloud storage provider, ensure that versioning or automated backups are enabled on the bucket.

### Restoration Process

To restore a Wiki.js instance from a backup:

1. Stop the Wiki.js application.
2. Drop and recreate the database.
3. Restore the database dump using `pg_restore`.
4. Restore the asset files to the appropriate location.
5. Start the Wiki.js application.

```bash
# Drop and recreate DB
dropdb -h localhost -U postgres wiki_db
createdb -h localhost -U postgres -O wiki_user wiki_db

# Restore DB
pg_restore -h localhost -U wiki_user -d wiki_db -1 "/backups/wiki_db_20231027.backup"
```

## Extending Wiki.js

Wiki.js supports various extensions to enhance its functionality.

### Rendering Extensions

With 14 Markdown rendering extensions (e.g., Katex, Mermaid, PlantUML) and 11 HTML post-processing extensions, you can customize how content is displayed. These extensions can be enabled and configured in the administration panel.

For example, enabling the Mermaid extension allows users to embed diagrams directly in their Markdown content:

```markdown
```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```
```

### Custom CSS and JavaScript

Administrators can inject custom CSS and JavaScript globally or per page. This is useful for theming or integrating third-party analytics tools.

As mentioned in the limitations, custom JavaScript must use the Wiki.js boot sequence to ensure it executes correctly within the Vue.js lifecycle.

```javascript
window.boot.register('page-ready', function() {
  console.log('Wiki.js page is fully loaded and rendered.');
  // Initialize custom scripts here
});
```

## Security Considerations

Securing a Wiki.js deployment involves multiple layers of defense.

### Network Security

Ensure that the Wiki.js application is deployed behind a reverse proxy (like NGINX or Traefik) that handles SSL/TLS termination. Do not expose the Node.js application directly to the internet.

### Access Control

Regularly review user permissions and group assignments. Utilize the principle of least privilege, granting users only the permissions they need to perform their tasks.

### Content Security Policy (CSP)

Implement a strict Content Security Policy to mitigate Cross-Site Scripting (XSS) attacks. This can be configured at the reverse proxy level.

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self';";
```

Note that Wiki.js requires `'unsafe-inline'` and `'unsafe-eval'` for some of its frontend components (like Vue.js and certain editors) to function correctly.

## Conclusion and Best Practices

Managing a Wiki.js instance requires a solid understanding of its architecture, API, and deployment options. By following the guidelines and utilizing the commands outlined in this reference, administrators can ensure a stable, secure, and highly performant knowledge base.

**Key Takeaways:**
- Always use Bearer tokens for API authentication and secure them properly.
- Leverage the GraphQL API for automation and integration tasks.
- Use PostgreSQL for production deployments, especially if High Availability is required.
- Implement a robust backup strategy covering both the database and uploaded assets.
- Be aware of the known limitations, such as the inability to install in a subfolder and the lack of real-time collaborative editing, and plan your deployment accordingly.

## Detailed API Reference: Advanced Scenarios

### Bulk Page Operations

While the GraphQL API provides single-page mutations, administrators often need to perform bulk operations, such as migrating content or applying tags to multiple pages. This requires writing custom scripts that iterate over a list of pages and execute mutations sequentially or in parallel (respecting server load).

**Example Node.js Script for Bulk Tagging:**

```javascript
const axios = require('axios');

const API_URL = 'https://wiki.example.com/graphql';
const API_TOKEN = 'YOUR_API_TOKEN';

const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${API_TOKEN}`
};

async function addTagToPage(pageId, tag) {
  const query = `
    mutation {
      pages {
        update(id: ${pageId}, tags: ["${tag}"]) {
          responseResult {
            succeeded
            message
          }
        }
      }
    }
  `;

  try {
    const response = await axios.post(API_URL, { query }, { headers });
    console.log(`Page ${pageId}: ${response.data.data.pages.update.responseResult.message}`);
  } catch (error) {
    console.error(`Error updating page ${pageId}:`, error.message);
  }
}

// Example usage: Add 'archived' tag to a list of page IDs
const pageIdsToArchive = [101, 102, 103, 104];
pageIdsToArchive.forEach(id => addTagToPage(id, 'archived'));
```

### Monitoring and Health Checks

For Kubernetes or Docker Swarm deployments, configuring health checks is critical for maintaining high availability. Wiki.js provides a basic health check endpoint that can be used by load balancers and orchestrators.

While there isn't a dedicated `/health` REST endpoint in the traditional sense, you can query the GraphQL API for basic site information to verify the application is responsive and connected to the database.

**Liveness Probe Example (Kubernetes):**

```yaml
livenessProbe:
  httpGet:
    path: /
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10
```

For a more robust check, a script could execute a simple GraphQL query:

```bash
curl -f -X POST -H "Content-Type: application/json" -d '{"query": "{ site { title } }"}' http://localhost:3000/graphql || exit 1
```

### Handling Large File Uploads

By default, Wiki.js has a body parser limit (configured in `config.yml` as `bodyParserLimit: 5mb`). If users need to upload large assets (e.g., video files or large PDFs), this limit must be increased.

1. Update `config.yml`:
   ```yaml
   bodyParserLimit: 50mb
   ```
2. Update Reverse Proxy Settings (e.g., NGINX):
   ```nginx
   client_max_body_size 50M;
   ```
3. Restart the Wiki.js service.

### Customizing the Theme

Wiki.js uses Vuetify for its UI components. While full custom themes require modifying the source code and rebuilding the frontend, administrators can achieve significant customization through the **Code Injection** feature in the administration panel.

By injecting custom CSS, you can override Vuetify variables and classes.

**Example CSS Injection:**

```css
/* Change the primary toolbar color */
.v-toolbar.primary {
  background-color: #2c3e50 !important;
  border-color: #2c3e50 !important;
}

/* Customize heading styles in markdown content */
.contents h1 {
  color: #e74c3c;
  border-bottom: 2px solid #ecf0f1;
  padding-bottom: 10px;
}
```

### Troubleshooting Common Issues

1. **Blank Page on Load:** This is often caused by Cloudflare's Rocket Loader or Auto Minify interfering with Vue.js scripts. Disable these features in the Cloudflare dashboard for the Wiki.js domain.
2. **Database Connection Errors:** Ensure the database container is fully initialized before Wiki.js starts. In `docker-compose`, use `depends_on` with a health check, or implement a wait-for-it script.
3. **Search Not Returning Results:** If using PostgreSQL `pg_trgm`, ensure the extension is installed. If using Elasticsearch, check the connection and trigger a manual reindex from the admin panel.
4. **Cannot Login After Update:** Clear your browser cache and cookies. Sometimes, old session data conflicts with new authentication logic. If the issue persists, check the database `users` table to ensure the account is active.

By mastering these advanced configurations, CLI commands, and API interactions, you can ensure your Wiki.js deployment is robust, scalable, and perfectly tailored to your organization's needs.

## === FILE: 46-wikijs-config-schemas.md ===
# Wiki.js Specialist Guide: Configuration Schemas and References

Wiki.js v2.x is a powerful, open-source (AGPL-3.0) wiki platform built on Node.js (>= 20), Vue.js 2, Vuetify, and a GraphQL API. Authored by Nicolas Giard (Requarks), it has become a staple for documentation, knowledge bases, and internal team wikis. This guide provides a comprehensive, deep-dive reference for all configuration schemas, environment variables, deployment manifests, GraphQL types, and module configurations required to operate, troubleshoot, and scale Wiki.js in production environments.

## 1. Core Configuration: `config.yml` Reference

The `config.yml` file is the primary configuration mechanism for Wiki.js when not using environment variables. It dictates how the Node.js application binds to the network, connects to the database, and handles core operational modes. Understanding every parameter in this file is crucial for system administrators.

### 1.1 Network and Server Settings

```yaml
# Port the server should listen on. Default is 3000.
# Note: Binding to ports < 1024 requires setcap or iptables redirect.
port: 3000

# Bind IP address (optional)
# Set to '0.0.0.0' to listen on all interfaces, or '127.0.0.1' for localhost only.
# In Docker, this is typically left as 0.0.0.0.
bindIP: 0.0.0.0

# Maximum request body size limit (e.g., for file uploads via the API or UI)
# Accepts string values like '5mb', '100kb', '1gb'.
bodyParserLimit: 5mb

# Data path for local storage, cache, and temporary files.
# Ensure the Node.js process has read/write permissions to this directory.
dataPath: ./data

# Offline mode
# Disables external network requests for air-gapped environments.
# This prevents Wiki.js from fetching external avatars, telemetry, or updates.
offline: false

# High Availability mode
# Enables multi-node clustering.
# CRITICAL: This strictly requires PostgreSQL as the database backend.
ha: false
```

*Note on High Availability (HA):* Setting `ha: true` enables multi-node clustering. This **strictly requires PostgreSQL** as the database backend because Wiki.js relies on PostgreSQL's `LISTEN/NOTIFY` pub/sub mechanism to synchronize state (like cache invalidation and search index updates) across multiple instances. SQLite cannot be used in HA mode.

### 1.2 Database Configuration (`db` block)

Wiki.js supports multiple database backends. PostgreSQL is highly recommended and required for HA. Other supported databases include MySQL 8+, MariaDB 10.2.7+, MSSQL 2012+, and SQLite 3.9+.

#### PostgreSQL (Recommended)
```yaml
db:
  type: postgres
  host: localhost
  port: 5432
  user: wikijs
  pass: wikijsrocks
  db: wiki
  ssl: false
```

#### MySQL / MariaDB
*Limitation:* MySQL `caching_sha2_password` is not supported by the underlying Node.js driver used by Wiki.js. You must configure your MySQL users to use `mysql_native_password`.
```yaml
db:
  type: mysql
  host: localhost
  port: 3306
  user: wikijs
  pass: wikijsrocks
  db: wiki
  ssl: false
```

#### SQLite
SQLite is suitable for small, single-node deployments or testing.
```yaml
db:
  type: sqlite
  storage: path/to/database.sqlite
```

#### Connection Pool Options (`pool` block)
Wiki.js uses `tarn.js` for connection pooling under the hood (via Knex.js). You can configure the pool behavior to optimize database connections, especially in high-traffic environments or when dealing with strict database connection limits.
```yaml
db:
  type: postgres
  host: localhost
  port: 5432
  user: wikijs
  pass: wikijsrocks
  db: wiki
  pool:
    min: 2
    max: 10
    acquireTimeoutMillis: 30000
    createTimeoutMillis: 30000
    idleTimeoutMillis: 30000
    reapIntervalMillis: 1000
    createRetryIntervalMillis: 200
```

### 1.3 SSL Configuration (`ssl` block)

Wiki.js can handle SSL termination directly, though using a reverse proxy (like Nginx, Traefik, or HAProxy) is generally recommended for production deployments to offload TLS processing.

#### Custom Certificates
```yaml
ssl:
  enabled: true
  provider: custom
  format: pem
  key: /path/to/privkey.pem
  cert: /path/to/cert.pem
  # Optional CA bundle for intermediate certificates
  ca: /path/to/chain.pem
```

#### Let's Encrypt (Automatic)
Wiki.js can automatically provision and renew Let's Encrypt certificates. This requires port 80 to be accessible from the internet for the HTTP-01 challenge.
```yaml
ssl:
  enabled: true
  provider: letsencrypt
  domain: wiki.example.com
  subscriberEmail: admin@example.com
```

### 1.4 Logging Configuration

Proper logging configuration is essential for troubleshooting and auditing.

```yaml
# Log level: error, warn, info, verbose, debug, silly
# Use 'debug' or 'silly' only for troubleshooting as they generate massive output.
logLevel: info

# Log format: default, json
# Use 'json' for structured logging, which is ideal for ingestion into ELK, Datadog, or Splunk.
logFormat: default
```

---

## 2. Environment Variables

For containerized deployments (Docker, Kubernetes), configuring Wiki.js via environment variables is the standard practice. Environment variables override the corresponding values in `config.yml`.

### Database Variables
- `DB_TYPE`: Database type (`postgres`, `mysql`, `mariadb`, `mssql`, `sqlite`).
- `DB_HOST`: Database server hostname or IP address.
- `DB_PORT`: Database server port.
- `DB_USER`: Database username.
- `DB_PASS`: Database password.
- `DB_NAME`: Database name.
- `DB_SSL`: Set to `true` to enable SSL/TLS for the database connection.

### Operational Variables
- `HA_ACTIVE`: Set to `true` to enable High Availability mode (requires PostgreSQL).
- `UPGRADE_COMPANION`: Set to `1` to enable the Wiki.js Update Companion (used in Docker deployments to handle automated updates).
- `PORT`: Overrides the listening port (default 3000). Note: Port < 1024 requires `setcap` or iptables redirect.
- `WIKI_ADMIN_EMAIL`: Used during initial setup to pre-configure the admin user.
- `WIKI_ADMIN_PASSWORD`: Used during initial setup to pre-configure the admin password.

---

## 3. Deployment Manifests

### 3.1 Docker Compose Schema

The standard Docker Compose deployment utilizes the official `ghcr.io/requarks/wiki` image alongside PostgreSQL and the `wiki-update-companion`. The companion container allows Wiki.js to update itself via the web UI by interacting with the Docker socket.

```yaml
version: "3.8"
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: wiki
      POSTGRES_PASSWORD: wikijsrocks
      POSTGRES_USER: wikijs
    logging:
      driver: "none"
    restart: unless-stopped
    volumes:
      - db-data:/var/lib/postgresql/data

  wiki:
    image: ghcr.io/requarks/wiki:2
    depends_on:
      - db
    environment:
      DB_TYPE: postgres
      DB_HOST: db
      DB_PORT: 5432
      DB_USER: wikijs
      DB_PASS: wikijsrocks
      DB_NAME: wiki
      UPGRADE_COMPANION: 1
    restart: unless-stopped
    ports:
      - "80:3000"
    volumes:
      - wiki-data:/wiki/data

  wiki-update-companion:
    image: ghcr.io/requarks/wiki-update-companion:latest
    container_name: wiki-update-companion
    privileged: true
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - WIKI_CONTAINER_NAME=wiki

volumes:
  db-data:
  wiki-data:
```
*Limitation:* The `wiki-update-companion` container must be updated separately from the main Wiki.js container. It cannot update itself.

### 3.2 Kubernetes Helm `values.yaml` Schema

When deploying via the official Helm chart, the `values.yaml` file controls the deployment schema. Key configuration blocks include replica counts, database connections, ingress rules, and resource limits.

```yaml
replicaCount: 2 # Set > 1 for HA (requires PostgreSQL)

image:
  repository: ghcr.io/requarks/wiki
  tag: "2.5.300"
  pullPolicy: IfNotPresent

# Database configuration (using the bitnami/postgresql subchart)
postgresql:
  enabled: true
  postgresqlUsername: wikijs
  postgresqlPassword: wikijsrocks
  postgresqlDatabase: wiki

# Or use an external database (e.g., AWS RDS, GCP Cloud SQL)
externalDatabase:
  type: postgres
  host: external-db.example.com
  port: 5432
  user: wikijs
  password: wikijsrocks
  database: wiki

ingress:
  enabled: true
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: wiki.example.com
      paths:
        - /
  tls:
    - secretName: wiki-tls
      hosts:
        - wiki.example.com

# High Availability
ha:
  enabled: true # Automatically sets HA_ACTIVE=true in the container environment

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 256Mi
```

---

## 4. GraphQL API Schemas

Wiki.js is built entirely on a GraphQL API, accessible at `/graphql` with Bearer token authentication. Understanding the core types is essential for automation, custom integrations, and headless CMS usage.

### 4.1 `Page` Type Schema

The `Page` type represents a full wiki page, including its content, metadata, and rendering state.

```graphql
type Page {
  id: Int!
  path: String!
  hash: String! # SHA1(locale + path + privateNS)
  title: String!
  description: String
  isPublished: Boolean!
  isPrivate: Boolean!
  privateNS: String
  contentType: String! # e.g., markdown, html, adoc
  createdAt: Date!
  updatedAt: Date!
  editor: String! # markdown, wysiwyg, ckeditor, code, api, asciidoc
  locale: String!
  authorId: Int!
  authorName: String!
  creatorId: Int!
  creatorName: String!
  content: String! # Raw content (e.g., raw markdown)
  render: String # Rendered HTML output
  toc: String # Table of Contents JSON representation
  tags: [Tag]!
}
```
*Note on Page Paths:* Page paths cannot contain dots, spaces, backslashes, or double slashes. They must not start or end with a slash.

### 4.2 `PageListItem` Type Schema

Used in list queries (like search results or recent changes), this is a lightweight version of the `Page` type without the full content payload, optimizing API response times.

```graphql
type PageListItem {
  id: Int!
  path: String!
  title: String!
  description: String
  isPublished: Boolean!
  isPrivate: Boolean!
  privateNS: String
  contentType: String!
  createdAt: Date!
  updatedAt: Date!
  locale: String!
  tags: [Tag]!
}
```

### 4.3 `PageTreeItem` Type Schema

Used for rendering the navigation tree in the sidebar.

```graphql
type PageTreeItem {
  id: Int!
  path: String!
  title: String!
  isFolder: Boolean!
  hasChildren: Boolean!
  parent: Int
  locale: String!
  isPrivate: Boolean!
  privateNS: String
}
```

### 4.4 Example GraphQL Query

To fetch a page by its ID:

```graphql
query {
  pages {
    single(id: 123) {
      id
      title
      path
      content
      render
    }
  }
}
```

---

## 5. Internal Data Formats

### 5.1 Session JSONL Format

Wiki.js stores session data in the database, but when exported or logged, it often follows a JSONL (JSON Lines) format. Each line represents a distinct session state, containing cookie configurations, passport authentication state, and JWT tokens.

```json
{"sid":"sess:1a2b3c4d","sess":{"cookie":{"originalMaxAge":2592000000,"expires":"2023-12-01T12:00:00.000Z","secure":true,"httpOnly":true,"path":"/"},"passport":{"user":1},"jwt":"eyJhbG..."},"expire":"2023-12-01T12:00:00.000Z"}
{"sid":"sess:5e6f7g8h","sess":{"cookie":{"originalMaxAge":2592000000,"expires":"2023-12-02T15:30:00.000Z","secure":true,"httpOnly":true,"path":"/"},"passport":{"user":42},"jwt":"eyJhbG..."},"expire":"2023-12-02T15:30:00.000Z"}
```

---

## 6. Module Configuration Schemas

Wiki.js is highly modular. Configurations for rendering, search, and storage are stored in the database but managed via the UI or API. Below are the underlying configuration schemas for these modules.

### 6.1 Rendering Pipeline Configuration

Wiki.js uses a multi-stage rendering pipeline. It supports 14 Markdown rendering extensions (core, abbr, emoji, expandtabs, footnotes, imsize, katex, kroki, mathjax, multi-table, pivot-table, plantuml, supsub, tasklists) and 11 HTML post-processing extensions (core, asciinema, blockquotes, codehighlighter, diagram/draw.io, image-prefetch, mediaplayers, mermaid, security, tabset, twemoji).

#### Markdown-Core Options
The `markdown-core` extension is the foundation of the rendering pipeline. Its configuration schema includes:

```json
{
  "allowHTML": false,      // Allow raw HTML in markdown (often stripped by security sanitizer)
  "breaks": true,          // Convert \n to <br>
  "linkify": true,         // Autoconvert URL-like text to links
  "typographer": true,     // Enable smartquotes and other typographic replacements
  "quotes": "“”‘’",        // Characters to use for quotes if typographer is true
  "underline": false       // Enable underline syntax
}
```
*Limitation:* Custom HTML is stripped by default by the `security` HTML post-processing extension. If `allowHTML` is true, you must also configure the security sanitizer to allow specific tags, or disable the security sanitizer entirely (not recommended for public wikis).

### 6.2 Search Engine Configuration

Wiki.js supports 8 search engines: Algolia, AWS, Azure, Database (built-in), Elasticsearch, Manticore, PostgreSQL (pg_trgm), Solr, and Sphinx.

#### PostgreSQL (pg_trgm) Schema
When using PostgreSQL, the native `pg_trgm` extension provides excellent search capabilities without external dependencies.
```json
{
  "dict": "english",       // Text search dictionary
  "threshold": 0.3         // Similarity threshold for trigram matching
}
```

#### Elasticsearch Schema
```json
{
  "node": "http://elasticsearch:9200",
  "index": "wikijs",
  "auth": {
    "username": "elastic",
    "password": "changeme"
  },
  "sniffOnStart": false
}
```

#### Algolia Schema
```json
{
  "appId": "YOUR_APP_ID",
  "apiKey": "YOUR_ADMIN_API_KEY",
  "indexName": "wikijs"
}
```

### 6.3 Storage Module Configuration

Wiki.js supports 11 storage backends for syncing content and assets: Azure, Box, DigitalOcean, Disk, Dropbox, Google Drive, Git, OneDrive, S3, S3 Generic, and SFTP.

#### Git Storage Schema
The Git storage module allows two-way synchronization between Wiki.js and a Git repository, enabling a docs-as-code workflow.

```json
{
  "localRepoPath": "./data/repo",
  "branch": "main",
  "remote": "git@github.com:organization/wiki-content.git",
  "authType": "ssh", // Options: basic, ssh, none
  "sshKey": "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW\n... \n-----END OPENSSH PRIVATE KEY-----",
  "sshPublicKey": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... user@host",
  "username": "",    // Used for basic auth
  "password": "",    // Used for basic auth or SSH key passphrase
  "signatureName": "Wiki.js Sync",
  "signatureEmail": "wiki@example.com",
  "syncInterval": "*/5 * * * *" // Cron expression for sync frequency
}
```
*Limitation:* Git storage sync can conflict with direct DB edits if changes occur simultaneously. Version history in Wiki.js automatically creates a snapshot on every update, but Git merge conflicts require manual resolution via the server's filesystem.

#### S3 Storage Schema
```json
{
  "region": "us-east-1",
  "bucket": "my-wiki-assets",
  "accessKeyId": "AKIAIOSFODNN7EXAMPLE",
  "secretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
  "endpoint": "", // Used for S3 Generic (e.g., MinIO, DigitalOcean Spaces)
  "forcePathStyle": false
}
```

### 6.4 Authentication Modules

Wiki.js supports 21 Authentication modules: Auth0, Azure AD, CAS, Discord, Dropbox, Facebook, Firebase, GitHub, GitLab, Google, Keycloak, LDAP/AD, Local, Microsoft, OAuth2, OIDC, Okta, Rocket.chat, SAML 2.0, Slack, and Twitch.

Configuration for these modules typically involves setting a Client ID, Client Secret, and Authorization/Token endpoints. For enterprise environments, SAML 2.0 and LDAP/AD are commonly used.

### 6.5 Comment Systems

Wiki.js supports 4 Comment systems: Artalk, Commento, Default (built-in), and Disqus. The built-in system stores comments directly in the database, while the others require external service configuration (e.g., Disqus shortname).

---

## 7. Known Limitations and Operational Gotchas

When operating Wiki.js in production, be aware of the following architectural constraints and known issues:

1. **Subfolder Installation:** Wiki.js cannot be installed in a subfolder (e.g., `example.com/wiki`). It strictly requires a dedicated subdomain or root domain (e.g., `wiki.example.com`).
2. **Real-time Collaboration:** There is no real-time collaborative editing (like Google Docs). Concurrent edits may result in the last writer winning, though version history is preserved.
3. **HA Constraints:** SQLite cannot be used in High Availability mode. HA requires PostgreSQL.
4. **MySQL Authentication:** MySQL `caching_sha2_password` is not supported. You must configure MySQL users with `mysql_native_password`.
5. **Editor Conversions:** Wiki.js supports 6 editors (markdown, wysiwyg, ckeditor, code, api, asciidoc). Converting a page between editors (e.g., Markdown to WYSIWYG) may result in formatting loss.
6. **Custom HTML:** Custom HTML is stripped by default by the security sanitizer.
7. **Rate Limiting:** There is no native API rate limiting. You must implement rate limiting at the reverse proxy layer (e.g., Nginx `limit_req`).
8. **Git Sync Conflicts:** Git storage sync can conflict with direct DB edits.
9. **Path Restrictions:** Page paths cannot contain dots, spaces, or special characters.
10. **Cloudflare Optimizations:** Cloudflare optimization features (Auto Minify, Mirage, Rocket Loader) break Wiki.js assets. These must be disabled via Page Rules for the Wiki.js domain.
11. **Companion Updates:** The `wiki-update-companion` container must be updated separately from the main application container.
12. **Custom JavaScript:** Custom JS injected via the admin panel must use the specific bootloader hook: `window.boot.register('page-ready', callback)`. Standard `DOMContentLoaded` events may not fire reliably due to the Vue.js SPA architecture.
13. **Privileged Ports:** Binding to a port < 1024 (like 80 or 443) directly requires `setcap` on the Node binary or an iptables redirect, as Wiki.js drops root privileges.

---

## 8. Permissions and Access Control

Wiki.js implements a granular permission system. When configuring roles via the API or database, the following core permission flags are utilized:

- `read:pages`: View published pages.
- `write:pages`: Create and edit pages.
- `manage:pages`: Move, rename, and manage page metadata.
- `delete:pages`: Delete pages.
- `write:styles`: Inject custom CSS.
- `write:scripts`: Inject custom JavaScript.
- `read:source`: View the raw source code of a page.
- `read:history`: View page version history.
- `manage:system`: Access the administration area.

These permissions are mapped to user groups and can be scoped to specific namespaces or page paths using rules.

---

## 9. Advanced Troubleshooting

### 9.1 Database Connection Issues
If Wiki.js fails to start with database connection errors, verify the `pool` configuration in `config.yml`. In environments with aggressive connection culling (like some serverless databases or strict firewalls), you may need to decrease `idleTimeoutMillis` and enable `createRetryIntervalMillis`.

### 9.2 Search Index Corruption
If the built-in database search or an external search engine (like Elasticsearch) stops returning accurate results, you can trigger a full reindex via the GraphQL API:

```graphql
mutation {
  searchRebuildIndex {
    success
    message
  }
}
```

### 9.3 Asset Loading Failures
If the UI loads but assets (CSS/JS) return 404s or fail to execute:
1. Verify the `Site URL` in the administration panel exactly matches the URL used to access the site (including `http/https`).
2. If behind Cloudflare, ensure Rocket Loader and Auto Minify are disabled.
3. Check the `dataPath` in `config.yml` to ensure the application has write permissions to the cache directory.

By understanding and properly managing these configuration schemas, you can ensure a stable, secure, and performant Wiki.js deployment tailored to your organization's needs.

## === FILE: 46-wikijs-deep-dive.md ===
# Wiki.js Architecture Deep Dive: A Comprehensive Guide

## 1. Introduction to Wiki.js Architecture

Wiki.js is a modern, open-source wiki platform built on Node.js, designed for performance, extensibility, and ease of use. Currently in its stable v2.x release, Wiki.js leverages a robust technology stack to deliver a seamless experience for both administrators and end-users. The core architecture is built upon Node.js (requiring version 20 or higher), utilizing the Express.js framework for HTTP server capabilities, and exposing a comprehensive GraphQL API for all frontend and external interactions.

The frontend is a Single Page Application (SPA) powered by Vue.js 2 and the Vuetify material design framework. This separation of concerns between the backend API and the frontend client allows for high flexibility and performance. The backend interacts with various relational databases through the Objection.js Object-Relational Mapping (ORM) library, which itself is built on top of the Knex.js query builder. Supported databases include PostgreSQL (which is highly recommended and strictly required for High Availability setups), MySQL 8+, MariaDB 10.2.7+, MSSQL 2012+, and SQLite 3.9+.

Wiki.js is licensed under the AGPL-3.0 license and is primarily authored by Nicolas Giard (Requarks). Its architecture is highly modular, supporting a wide array of editors, rendering extensions, authentication strategies, storage backends, and search engines. This deep dive will explore the intricate details of the Wiki.js request lifecycle, rendering pipeline, page models, version history, and more, providing a thorough understanding of its internal workings.

## 2. Request Lifecycle: From Client to Database

The request lifecycle in Wiki.js is a well-defined path that ensures security, efficiency, and consistency. When a client makes a request, it typically follows this trajectory: Express > GraphQL > Objection.js > Knex > Database.

### Express.js Middleware
At the outermost layer, Express.js handles incoming HTTP requests. It manages routing, static file serving, and initial middleware processing. Security headers, CORS configurations, and rate limiting (though native rate limiting is not present and requires a reverse proxy) are handled here. The Express server listens on the configured port (defined in `config.yml`) and routes API requests to the GraphQL endpoint at `/graphql`.

### GraphQL API Layer
Wiki.js relies heavily on GraphQL for its API. Instead of traditional REST endpoints, clients send GraphQL queries and mutations to the `/graphql` endpoint. This endpoint is protected by Bearer token authentication. The GraphQL layer defines the schema, types, and resolvers. When a query is received, the corresponding resolver is invoked. Resolvers are responsible for validating permissions (e.g., `read:pages`, `write:pages`, `manage:system`) and orchestrating the business logic.

```graphql
# Example GraphQL Query to fetch a page
query {
  pages {
    single(id: 123) {
      id
      path
      title
      description
      content
      contentType
      createdAt
      updatedAt
    }
  }
}
```

### Objection.js and Knex.js
Once the resolver has validated the request, it interacts with the database using Objection.js. Objection.js is an ORM that provides a structured way to define models and relationships. It translates JavaScript objects and methods into SQL queries. Under the hood, Objection.js uses Knex.js, a powerful SQL query builder. Knex.js handles the actual generation of SQL dialects specific to the configured database (PostgreSQL, MySQL, etc.) and manages connection pooling.

### Database Execution
Finally, the generated SQL query is executed against the database. The results are returned through Knex.js to Objection.js, which instantiates the corresponding model objects. These objects are then formatted by the GraphQL resolver and sent back to the client as a JSON response.

## 3. Rendering Pipeline Internals

The rendering pipeline in Wiki.js is a sophisticated process that transforms raw content from various editors into safe, optimized HTML for display. Wiki.js supports 6 different editors: `markdown`, `wysiwyg` (HTML), `ckeditor` (HTML), `code` (HTML), `api` (YML), and `asciidoc` (ADOC).

### Markdown Rendering (markdown-it)
For Markdown content, Wiki.js uses `markdown-it` as its core rendering engine. The rendering process is highly extensible, utilizing a chain of 14 Markdown rendering extensions. These include:
- `core`: Basic Markdown syntax.
- `abbr`: Abbreviations.
- `emoji`: Emoji shortcodes.
- `expandtabs`: Tab expansion.
- `footnotes`: Footnote support.
- `imsize`: Image sizing.
- `katex` / `mathjax`: Mathematical formulas.
- `kroki` / `plantuml`: Diagram generation.
- `multi-table` / `pivot-table`: Advanced tables.
- `supsub`: Superscript and subscript.
- `tasklists`: Task lists.

### HTML Post-Processing
Once the raw content is converted to HTML (or if the content was already HTML from a WYSIWYG editor), it passes through an HTML post-processing phase. This phase uses 11 extensions to enhance the HTML:
- `core`: Basic HTML adjustments.
- `asciinema`: Asciinema player integration.
- `blockquotes`: Enhanced blockquotes.
- `codehighlighter`: Syntax highlighting for code blocks.
- `diagram` (draw.io): Draw.io diagram rendering.
- `image-prefetch`: Optimizing image loading.
- `mediaplayers`: Audio and video player embedding.
- `mermaid`: Mermaid.js diagram rendering.
- `security`: Crucial security sanitization.
- `tabset`: Tabbed content.
- `twemoji`: Twitter emoji integration.

### Security Sanitization
The `security` post-processing extension is critical. It uses libraries like DOMPurify to strip out potentially malicious HTML tags and attributes, preventing Cross-Site Scripting (XSS) attacks. By default, custom HTML is aggressively stripped. If administrators need to allow specific custom HTML, they must carefully configure the sanitization rules, balancing functionality with security.

### Caching the Rendered Output
To ensure high performance, the final rendered HTML is cached. This page render cache prevents the system from having to re-parse and re-render complex Markdown or diagrams on every page load. The cache is invalidated when the page content is updated.

## 4. Page Model Internals

The Page model is central to Wiki.js. It encapsulates all metadata and content associated with a wiki page.

### Hash Generation
Every page in Wiki.js is uniquely identified by a hash. This hash is generated using the SHA1 algorithm based on three components: the locale, the path, and the private namespace (privateNS).
`Page Hash = SHA1(locale + path + privateNS)`
This ensures that pages with the same path but in different languages or namespaces are treated as distinct entities. Page paths have strict rules: they cannot contain dots, spaces, backslashes, or double slashes, and they cannot start or end with a slash.

### Content Types
The `contentType` field in the Page model indicates the format of the raw content. This determines which editor was used and which rendering pipeline should be applied. Supported content types include `markdown`, `html`, `yml`, and `adoc`.

### Table of Contents (TOC) Generation
During the rendering pipeline, Wiki.js automatically generates a Table of Contents (TOC) by extracting heading tags (H1, H2, H3, etc.) from the rendered HTML. This TOC is stored alongside the page metadata and is used by the frontend to display a navigation sidebar.

## 5. Version History Implementation

Wiki.js maintains a comprehensive version history for all pages, ensuring that no data is ever permanently lost due to accidental edits or malicious changes.

### Automatic Snapshots
The version history system operates on an automatic snapshot mechanism. Every time a page is updated, a new snapshot of the page's content and metadata is created and stored in the database. This happens transparently during the Objection.js model lifecycle hooks (e.g., `beforeUpdate`).

### Restore Mechanism
Administrators and users with the `read:history` and `write:pages` permissions can view the version history of a page. The frontend provides an interface to compare different versions and restore a previous version. When a restore action is triggered, the system creates a *new* version that contains the content of the restored version, preserving the linear history of changes.

## 6. Search Engine Abstraction Layer

Wiki.js features a powerful search engine abstraction layer that allows administrators to choose the best search backend for their needs. It supports 8 different search engines:
- Algolia
- AWS CloudSearch
- Azure Search
- Database (built-in, basic LIKE queries)
- Elasticsearch
- Manticore
- PostgreSQL (pg_trgm, highly recommended for PostgreSQL users)
- Solr
- Sphinx

The abstraction layer defines a common interface for indexing documents, updating indexes, and performing search queries. When a page is created, updated, or deleted, the event system triggers an update to the active search engine index. This ensures that search results are always up-to-date.

## 7. Storage Sync Architecture

To facilitate backups, offline access, and version control, Wiki.js includes a robust storage sync architecture. It supports 11 storage backends, including Azure, Box, DigitalOcean, Disk, Dropbox, Google Drive, Git, OneDrive, S3, S3 Generic, and SFTP.

### Bidirectional Git Sync
The Git storage backend is particularly powerful, offering bidirectional synchronization. When a page is modified in Wiki.js, the changes are committed and pushed to the configured Git repository. Conversely, if changes are pushed to the Git repository externally, Wiki.js can pull those changes and update the database. However, this can lead to conflicts if direct database edits and Git edits occur simultaneously.

### Disk Export and Cloud Storage Push
Other storage backends typically operate in a push-only mode (export). Wiki.js can be configured to periodically export the entire wiki content as Markdown files (or other raw formats) to a local disk directory or push them to cloud storage providers like AWS S3 or Google Drive. This provides a reliable backup mechanism.

## 8. Authentication Flow

Security and access control are paramount in Wiki.js. The authentication flow is built on top of Passport.js, a popular authentication middleware for Node.js.

### Passport.js Strategies
Wiki.js supports an impressive 21 authentication modules, covering almost every conceivable identity provider. These include Auth0, Azure AD, CAS, Discord, Dropbox, Facebook, Firebase, GitHub, GitLab, Google, Keycloak, LDAP/AD, Local (built-in username/password), Microsoft, OAuth2, OIDC, Okta, Rocket.chat, SAML 2.0, Slack, and Twitch.

When a user attempts to log in, the request is routed to the appropriate Passport.js strategy. The strategy handles the interaction with the external identity provider (e.g., redirecting to Google for OAuth2 consent).

### JWT Tokens and Session Management
Upon successful authentication, Wiki.js generates a JSON Web Token (JWT). This token contains the user's identity and permissions. The JWT is sent back to the client and stored (typically in local storage or a cookie). For all subsequent requests to the GraphQL API, the client includes this JWT in the `Authorization: Bearer <token>` header. The backend verifies the JWT signature and extracts the user information, establishing the session context for the request.

## 9. Caching Layer

To deliver fast response times, Wiki.js employs a multi-tiered caching layer.

### Page Render Cache
As mentioned earlier, the final rendered HTML of a page is cached. This is the most critical cache for read performance, as it bypasses the entire rendering pipeline for frequently accessed pages.

### Tree Cache
Wiki.js caches the hierarchical structure of the wiki (the navigation tree). Generating this tree requires complex database queries to resolve parent-child relationships and permissions. Caching the tree significantly speeds up the initial load of the frontend SPA.

### Search Index Cache
Some search engines (like the built-in database search) utilize caching to store recent search results, reducing the load on the database for common queries.

## 10. Event System (WIKI.events)

Wiki.js utilizes an internal event emitter system, accessible via `WIKI.events`, to facilitate inter-module communication. This decoupled architecture allows different parts of the system to react to changes without tight coupling.

For example, when a page is updated, the page module emits a `page-updated` event. Other modules listen for this event:
- The search module listens to update the search index.
- The storage module listens to trigger a Git commit or cloud storage push.
- The cache module listens to invalidate the page render cache.

This event-driven approach makes the codebase highly extensible and maintainable.

## 11. Database Migration System

As Wiki.js evolves, the database schema must be updated to support new features. Wiki.js uses a robust database migration system based on versioned JavaScript files.

When Wiki.js starts, it checks the current database schema version against the available migration files. If the database is outdated, it sequentially executes the necessary migration scripts. These scripts use Knex.js schema building methods to create tables, add columns, and modify indexes. This ensures that upgrades are smooth and data integrity is maintained across versions.

## 12. Module Loading System

Wiki.js features a dynamic module loading system. During startup, the system scans specific directories (e.g., `/server/modules`) to discover available modules, editors, rendering extensions, and authentication strategies.

This dynamic discovery mechanism allows developers to easily add new features by simply dropping a new module folder into the appropriate directory. The module loading system reads the module's configuration (usually a `module.yml` or `package.json` file) and registers its capabilities with the core system.

## 13. Vue.js Frontend Architecture

The frontend of Wiki.js is a modern Single Page Application (SPA) built with Vue.js 2.

### Vuetify Material Design
The user interface is constructed using Vuetify, a comprehensive UI component framework based on Google's Material Design specification. Vuetify provides a consistent, responsive, and accessible design language across the entire application.

### Apollo GraphQL Client
To interact with the backend GraphQL API, the frontend uses the Apollo Client. Apollo manages data fetching, caching, and state management. It seamlessly integrates with Vue.js, allowing components to declaratively request the data they need.

### Editor Integration
The frontend integrates powerful third-party editors. For Markdown, it uses CodeMirror, providing syntax highlighting, line numbers, and a smooth typing experience. For WYSIWYG editing, it integrates CKEditor, offering a rich text editing interface familiar to users of traditional word processors.

## 14. Known Limitations and Workarounds

While Wiki.js is a powerful platform, it has several known limitations that administrators must be aware of:

1.  **Subfolder Installation:** Wiki.js cannot be installed in a subfolder (e.g., `example.com/wiki`). It must be hosted on a dedicated subdomain or root domain (e.g., `wiki.example.com`).
2.  **Real-time Collaboration:** There is no native support for real-time collaborative editing (like Google Docs). If two users edit the same page simultaneously, the last save wins.
3.  **SQLite in HA Mode:** SQLite cannot be used in High Availability (HA) mode due to its file-based nature and lack of concurrent write support. PostgreSQL is strictly required for HA.
4.  **MySQL Authentication:** MySQL 8's default `caching_sha2_password` authentication plugin is not supported. Users must configure their MySQL server to use `mysql_native_password`.
5.  **Editor Conversion:** Converting content between different editors (e.g., from Markdown to WYSIWYG) may result in formatting loss, as the underlying syntax differs significantly.
6.  **Custom HTML Stripping:** As a security measure, custom HTML is stripped by default by the security sanitizer. Administrators must explicitly configure the sanitizer to allow specific tags.
7.  **Rate Limiting:** There is no native API rate limiting. To protect against brute-force attacks or API abuse, administrators must implement rate limiting at the reverse proxy level (e.g., using Nginx or HAProxy).
8.  **Git Sync Conflicts:** The bidirectional Git storage sync can encounter conflicts if direct database edits and external Git commits modify the same page simultaneously. Manual intervention may be required to resolve these conflicts.
9.  **Page Path Restrictions:** Page paths cannot contain dots, spaces, or special characters. This can be restrictive for users migrating from other wiki platforms with more lenient naming conventions.
10. **CloudFlare Optimizations:** CloudFlare's optimization features (Auto Minify, Mirage, Rocket Loader) can break Wiki.js assets. These features must be disabled for the Wiki.js domain.
11. **Docker Updates:** When running via Docker, the `wiki-update-companion` container must be updated separately from the main `wiki` container.
12. **Custom JS Execution:** Custom JavaScript injected via the administration panel must be wrapped in `window.boot.register('page-ready', callback)` to ensure it executes after the SPA has fully loaded the page content.
13. **Privileged Ports:** Binding Wiki.js to ports below 1024 (like 80 or 443) requires special privileges. Administrators must use `setcap` on the Node.js binary or configure `iptables` port redirection.

## 15. Production Operations and Worst-Case Scenarios

Operating Wiki.js in a production environment requires careful planning and monitoring.

### High Availability (HA) Configuration
For mission-critical deployments, Wiki.js should be configured in HA mode. This requires setting `ha: true` in the `config.yml` file and using PostgreSQL as the database. In HA mode, multiple Wiki.js instances can run concurrently behind a load balancer. The instances use PostgreSQL's listen/notify features to synchronize cache invalidations and events across the cluster.

```yaml
# config.yml snippet for HA
port: 3000
db:
  type: postgres
  host: pg-cluster.internal
  port: 5432
  user: wiki
  pass: securepassword
  db: wikijs
ha: true
```

### Docker and Kubernetes Deployment
The recommended deployment method is using Docker. The official image is available at `ghcr.io/requarks/wiki`. For Kubernetes environments, an official Helm chart is available, simplifying the deployment and management of HA clusters.

```bash
# Example Docker run command
docker run -d -p 8080:3000 --name wiki --restart unless-stopped -e DB_TYPE=postgres -e DB_HOST=db -e DB_PORT=5432 -e DB_USER=wiki -e DB_PASS=wiki -e DB_NAME=wiki ghcr.io/requarks/wiki:2
```

### Worst-Case Scenarios and Disaster Recovery

**Scenario 1: Database Corruption**
If the primary database becomes corrupted, the system will fail.
*Recovery:* Restore the database from the latest automated backup. If Git storage sync is enabled, the raw Markdown content is safe in the Git repository, but user accounts, permissions, and history metadata will be lost if the database backup is unavailable.

**Scenario 2: Compromised Administrator Account**
If an admin account is compromised, the attacker could delete pages or modify system settings.
*Recovery:* Immediately revoke the compromised user's access via the database or identity provider. Use the version history feature to restore any modified or deleted pages. Review the audit logs (if configured via a reverse proxy) to determine the extent of the breach.

**Scenario 3: Storage Sync Failure**
If the Git repository becomes unreachable, Wiki.js will queue the sync events. However, if the queue overflows or the server restarts, sync events may be lost.
*Recovery:* Manually trigger a full sync from the administration panel once the Git repository is available again. Monitor the Wiki.js logs for sync errors.

**Scenario 4: Out of Memory (OOM) Crashes**
Large wikis with complex rendering tasks can consume significant memory, leading to Node.js OOM crashes.
*Recovery:* Increase the memory limit for the Node.js process using the `--max-old-space-size` flag. Optimize the rendering pipeline by disabling unnecessary extensions. Ensure the page render cache is functioning correctly.

By understanding the intricate architecture of Wiki.js, administrators can effectively deploy, manage, and troubleshoot this powerful wiki platform, ensuring a reliable and performant experience for all users.

## === FILE: 46-wikijs-security-audit.md ===
# Wiki.js Security Audit & Hardening Guide

## 1. Introduction
Wiki.js (v2.x) is a powerful, open-source (AGPL-3.0) wiki platform built on Node.js (>= 20), Vue.js 2, Vuetify, and a robust GraphQL API. Created by Nicolas Giard (Requarks), it has become a staple for enterprise knowledge management. While it offers extensive features—including 21 authentication modules, 11 storage backends, 8 search engines, and multiple editors—securing a production deployment requires a comprehensive, defense-in-depth approach. 

This document serves as a deep-dive security audit and hardening guide for Wiki.js. It covers everything from authentication and API security to infrastructure hardening, database encryption, and container security. Whether you are deploying via Docker, Kubernetes, or bare metal, adhering to these guidelines will ensure your knowledge base remains secure against internal and external threats.

## 2. Authentication Module Selection & Best Practices
Wiki.js supports an impressive array of 21 authentication modules, including Auth0, Azure AD, CAS, Discord, Dropbox, Facebook, Firebase, GitHub, GitLab, Google, Keycloak, LDAP/AD, Local, Microsoft, OAuth2, OIDC, Okta, Rocket.chat, SAML 2.0, Slack, and Twitch. Selecting and configuring the right module is critical for enterprise security.

### LDAP / Active Directory Integration
When integrating with legacy LDAP or Active Directory environments, security must be prioritized at the network and protocol levels.
- **Secure Transport (LDAPS):** Ensure that connections are secured using LDAPS (LDAP over SSL/TLS) on port 636, rather than plain text LDAP on port 389. Plain text LDAP transmits credentials in the clear, making them susceptible to packet sniffing.
- **Service Accounts:** Use a dedicated service account with read-only permissions to bind to the directory. Never use domain admin credentials or accounts with write access to the directory.
- **Search Base Optimization:** Restrict the search base to the specific organizational unit (OU) containing the users who need access to the wiki. This minimizes the attack surface and improves query performance.
- **Group Mapping:** Map LDAP groups to Wiki.js groups to automate role-based access control (RBAC). This ensures users are automatically deprovisioned or downgraded when their roles change in the central directory.

### SAML 2.0 and OIDC (OpenID Connect)
For modern enterprise environments, SAML 2.0 or OIDC (via providers like Keycloak, Okta, or Azure AD) are the strongly recommended authentication methods.
- **Enforce MFA at the IdP:** Enforce Multi-Factor Authentication (MFA) at the Identity Provider (IdP) level. Wiki.js relies entirely on the IdP for authentication verification, so securing the IdP is paramount.
- **Token Expiration:** Configure short-lived access tokens and refresh tokens in your OIDC provider to minimize the window of opportunity for stolen tokens.
- **Attribute Mapping:** Carefully map attributes (e.g., email, name, groups) to ensure accurate user provisioning. Avoid mapping sensitive attributes that are not required by Wiki.js. Ensure that the `email` attribute is verified by the IdP before trusting it in Wiki.js.

### Local Authentication Risks
If local authentication must be used, enforce strong password policies. However, administrators must be aware that Wiki.js does not have built-in brute force protection or account lockout mechanisms for local accounts. This critical security gap must be mitigated at the reverse proxy or Web Application Firewall (WAF) level.

## 3. API Token Management and Permission Scopes
Wiki.js exposes a powerful GraphQL endpoint at `/graphql` secured via Bearer token authentication. API tokens are used for programmatic access, automation, and third-party integrations.

### Token Generation and Storage
- **Principle of Least Privilege:** Generate API tokens with the absolute minimum permissions required for the specific task. Wiki.js permissions are granular and include `read:pages`, `write:pages`, `manage:pages`, `delete:pages`, `write:styles`, `write:scripts`, `read:source`, `read:history`, and `manage:system`.
- **Secure Storage:** Treat API tokens like highly sensitive passwords. Store them securely in a secrets management system (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault) and never hardcode them in scripts, CI/CD pipelines, or source code repositories.

### High-Risk Permission Scopes
Carefully assign scopes to API tokens. For example, a backup script that only needs to export pages should only be granted `read:pages` and `read:source`.
- **The Danger of `manage:system`:** The `manage:system`, `write:styles`, and `write:scripts` scopes are extremely high-risk. Tokens with these scopes can completely compromise the wiki, alter configurations, or inject malicious code. They should be strictly controlled, rarely issued, and heavily audited.

### Example: Secure GraphQL Query
When querying the API, always enforce HTTPS to protect the Bearer token in transit. Pass the token in the Authorization header:
```bash
curl -X POST https://wiki.example.com/graphql \
  -H "Authorization: Bearer YOUR_HIGHLY_SECURE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { pages { list { id path title isPrivate } } }"}'
```

## 4. HTML Security Sanitizer & Custom Script Injection Risks
Wiki.js supports 6 different editors: markdown, wysiwyg (html), ckeditor (html), code (html), api (yml), and asciidoc (adoc). To protect against Cross-Site Scripting (XSS) attacks, Wiki.js employs an HTML security sanitizer (whitelist-based filtering) by default during its post-processing phase.

### The Security Sanitizer Mechanism
The built-in security sanitizer aggressively strips out potentially dangerous HTML tags and attributes, such as `<script>`, `<iframe>`, `object`, `embed`, and inline event handlers like `onload` or `onerror`. 
- **Do Not Disable:** Never disable the security sanitizer unless absolutely necessary for a specific, highly trusted internal use case. Disabling it opens the door to stored XSS attacks, allowing malicious users to execute arbitrary JavaScript in the browsers of other users.
- **Handling Custom HTML:** If users need to embed custom content (e.g., diagrams, videos, complex tables), mandate the use of built-in extensions (e.g., diagram via draw.io, mediaplayers, plantuml) rather than allowing raw HTML bypasses.

### Custom Script Injection Risks
Wiki.js allows administrators to inject custom CSS and JavaScript globally via the administration panel. This feature requires the `write:styles` and `write:scripts` permissions.
- **High Risk Vector:** These permissions are equivalent to full administrative control over the frontend application. A malicious user or compromised account with `write:scripts` can inject keyloggers, steal session tokens, redirect users to phishing sites, or deface the entire wiki.
- **Strict Access Control:** Only grant these permissions to highly trusted, senior administrators.
- **Code Review Process:** Any custom scripts should be thoroughly reviewed for security vulnerabilities and performance impacts before being injected into the production environment.
- **Implementation Note:** Custom JS must use `window.boot.register('page-ready', callback)` to execute properly within the Vue.js lifecycle. Failure to do so may result in race conditions or broken functionality.

## 5. Reverse Proxy Hardening & SSL/TLS Configuration
Wiki.js should never be exposed directly to the internet. It is designed to be deployed behind a robust reverse proxy such as Nginx, Apache, HAProxy, or Traefik. The reverse proxy is responsible for SSL/TLS termination, security header injection, and rate limiting.

### SSL/TLS Configuration Best Practices
- **Let's Encrypt vs Custom Certs:** Use Let's Encrypt for automated, free certificates, or provision custom enterprise certificates. Ensure that the reverse proxy is configured to use strong cipher suites and modern TLS versions (strictly TLS 1.2 and TLS 1.3). Disable older, vulnerable protocols like TLS 1.0 and 1.1.
- **HSTS Implementation:** Enable HTTP Strict Transport Security (HSTS) to force clients to connect via HTTPS, preventing SSL stripping attacks.

### Nginx Hardening Example
Below is an example of a hardened Nginx configuration tailored for Wiki.js:

```nginx
server {
    listen 443 ssl http2;
    server_name wiki.example.com;

    ssl_certificate /etc/letsencrypt/live/wiki.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/wiki.example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Content Security Policy (CSP)
    # Note: Adjust CSP based on your specific extensions, search engines (e.g., Algolia), and integrations
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' wss:;" always;

    # Block hidden files and directories
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support for potential future features or extensions
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 6. Database Security
Wiki.js supports multiple database engines: PostgreSQL (recommended, required for HA), MySQL 8+, MariaDB 10.2.7+, MSSQL 2012+, and SQLite 3.9+. PostgreSQL is highly recommended for production deployments due to its robustness, performance, and support for High Availability (HA) mode.

### Connection Encryption
Ensure that the connection between the Wiki.js Node.js application and the database is encrypted using SSL/TLS. This prevents man-in-the-middle (MITM) attacks on the database traffic, which could expose sensitive wiki content or user credentials.
- In `config.yml`, configure the database connection to require SSL. For PostgreSQL, this often involves setting `ssl: true` in the database configuration block.

### User Privileges and Isolation
- **Dedicated User:** Create a dedicated database user specifically for Wiki.js. Never use the `postgres`, `root`, or `sa` administrative users.
- **Least Privilege:** Grant the Wiki.js database user only the permissions necessary to operate on its specific database (e.g., `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`, `DROP`, `INDEX` on the `wikijs` database).
- **MySQL Limitation Warning:** Note that MySQL's `caching_sha2_password` authentication plugin is not supported by the underlying Node.js driver used by Wiki.js. You must configure the Wiki.js database user to use `mysql_native_password`.

## 7. CORS, CSP Headers, and Brute Force Protection

### Cross-Origin Resource Sharing (CORS)
Wiki.js API endpoints should be protected by strict CORS policies. If you are building custom integrations that query the GraphQL API from a browser, ensure that the reverse proxy only allows CORS requests from explicitly trusted origins. Wildcard (`*`) CORS policies should be strictly prohibited in production.

### Content Security Policy (CSP) Deep Dive
A robust CSP is critical for mitigating XSS attacks. The CSP should restrict the sources from which scripts, styles, images, and other resources can be loaded.
- **The Vue.js Challenge:** Wiki.js relies heavily on inline scripts and styles for its Vue.js frontend and various rich text editors. A strict CSP without `'unsafe-inline'` and `'unsafe-eval'` will break the application's core functionality.
- **Pragmatic Mitigation:** Use a pragmatic CSP (as shown in the Nginx example above) that allows necessary inline execution but restricts external domains. If you use external services like Algolia for search or AWS S3 for storage, you must explicitly add their domains to the respective CSP directives (e.g., `connect-src`, `img-src`).

### Brute Force Protection Implementation
As noted earlier, Wiki.js lacks native rate limiting or brute force protection. This must be implemented externally.
- **Fail2Ban Integration:** Use Fail2Ban to parse reverse proxy access and error logs. Configure it to block IP addresses that exhibit brute-force behavior (e.g., multiple failed POST requests to `/login` or `/graphql` within a short timeframe).
- **Nginx Rate Limiting:** Implement strict rate limiting on authentication and API endpoints to prevent resource exhaustion and credential stuffing.

```nginx
# Define rate limit zones
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;
limit_req_zone $binary_remote_addr zone=graphql_limit:10m rate=30r/m;

server {
    # ...
    location /login {
        limit_req zone=login_limit burst=5 nodelay;
        proxy_pass http://127.0.0.1:3000;
        # ...
    }
    
    location /graphql {
        limit_req zone=graphql_limit burst=20 nodelay;
        proxy_pass http://127.0.0.1:3000;
        # ...
    }
}
```

## 8. Account Verification & Rate Limiting
- **Email Verification:** If local authentication is enabled, strictly enforce email verification for all new accounts. This prevents automated bots from creating fake accounts and spamming the wiki.
- **GraphQL Rate Limiting:** The GraphQL endpoint (`/graphql`) is particularly susceptible to resource exhaustion attacks. Complex, deeply nested queries can consume significant CPU and database resources. Rate limiting at the reverse proxy is essential to maintain availability.

## 9. File Upload Security
Wiki.js allows users to upload images and attachments. This presents a significant security risk, including malware distribution and storage exhaustion.
- **Storage Backends:** Wiki.js supports 11 storage backends (e.g., S3, Azure, DigitalOcean, Disk). Using cloud object storage (like AWS S3 or Azure Blob Storage) is strongly recommended over local disk storage. It isolates uploaded files from the application server, preventing local file inclusion (LFI) or remote code execution (RCE) vulnerabilities if a malicious file is somehow executed.
- **File Type Restrictions:** Configure Wiki.js to only allow specific, safe file extensions (e.g., `.jpg`, `.png`, `.pdf`, `.docx`). Explicitly reject dangerous extensions like `.exe`, `.sh`, `.php`, `.html`, or `.js`.
- **Malware Scanning:** In high-security environments, integrate a reverse proxy or ICAP server to scan uploaded files for malware using ClamAV or a commercial antivirus solution before they reach the storage backend.

## 10. Private Pages, Namespace Isolation, and Group-Based Access Control
Wiki.js uses a robust Group-Based Access Control (GBAC) system to manage permissions.
- **Cryptographic Page Hashes:** Page hashes are calculated as `SHA1(locale + path + privateNS)`. This ensures that private namespaces are cryptographically separated in the database, preventing direct object reference (IDOR) attacks from guessing page IDs.
- **Namespace Isolation:** Use namespaces to isolate sensitive documentation (e.g., HR, Finance, Security). Assign permissions to these namespaces strictly based on groups.
- **Default Group Auditing:** Carefully review the permissions assigned to the "Guest" and "Default" groups. Ensure that anonymous users cannot access private namespaces, view source code (`read:source`), or perform unauthorized actions.
- **Path Rules:** Remember that page paths cannot contain dots, spaces, backslashes, or double slashes. No starting or ending slashes are allowed. This strict routing prevents directory traversal attacks but requires strict naming conventions.

## 11. Audit Logging and Monitoring
Comprehensive audit logging is essential for incident response, compliance, and forensic analysis.
- **Log Level Configuration:** Set the `logLevel` in `config.yml` to `info` for production environments. Use `debug` only for temporary troubleshooting, as it may expose sensitive data.
- **Centralized Logging:** Forward Wiki.js logs (stdout/stderr) and reverse proxy logs to a centralized logging system (e.g., ELK stack, Splunk, Datadog, Graylog) for analysis, retention, and alerting.
- **Monitor High-Risk Actions:** Create automated alerts for high-risk actions, such as:
  - Changes to user permissions or group assignments.
  - Spikes in failed login attempts.
  - Modifications to custom scripts or styles.
  - Unexpected database connection errors.

## 12. Docker & Kubernetes Security
Wiki.js is commonly deployed using Docker (`ghcr.io/requarks/wiki`) or Kubernetes (via the official Helm chart). Securing the container runtime is critical.

### Docker Security Best Practices
- **Non-Root User Execution:** The official Docker image is designed to run as the `node` user (UID 1000) by default. Ensure that you do not override this to run as `root`. Running as a non-root user mitigates the impact of container breakout vulnerabilities.
- **Read-Only Filesystem:** Run the container with a read-only root filesystem to prevent attackers from modifying the application code, installing unauthorized packages, or dropping malware.
```yaml
# docker-compose.yml security-hardened example
services:
  wiki:
    image: ghcr.io/requarks/wiki:2
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
      - /wiki/data/cache
    volumes:
      - ./config.yml:/wiki/config.yml:ro
      - wiki-data:/wiki/data
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
```
- **wiki-update-companion Risks:** If using the `wiki-update-companion` container for automated updates, be aware that it requires access to the Docker socket (`/var/run/docker.sock`). This is a massive security risk, as access to the Docker socket is equivalent to root access on the host. It is generally safer to manage updates via standard CI/CD pipelines rather than exposing the Docker socket.

### Kubernetes Security Best Practices
- **Network Policies:** Implement strict Kubernetes Network Policies to restrict traffic to the Wiki.js pods. Only allow ingress from the designated Ingress Controller and egress to the database and necessary external services (e.g., IdP, cloud storage backends). Deny all other traffic by default.
- **Secrets Management:** Never store the `config.yml` or database credentials in plain text ConfigMaps. Use Kubernetes Secrets, or better yet, integrate with an external secrets manager like HashiCorp Vault or AWS Secrets Manager using the CSI Secrets Store driver.
- **Pod Security Context:** Enforce strict security contexts on the pods to ensure they run with the least privilege necessary:
```yaml
# Kubernetes Pod Security Context
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
```

## 13. Known Limitations & Security Trade-offs
When auditing and deploying Wiki.js, administrators must be aware of the following known limitations and their security implications:
1. **Subfolder Installation:** Wiki.js cannot be installed in a subfolder (e.g., `example.com/wiki`); it requires a dedicated subdomain (e.g., `wiki.example.com`). This actually improves security by simplifying cookie scoping and reducing the risk of session fixation or cross-site scripting attacks from neighboring applications on the same domain.
2. **SQLite in HA:** SQLite cannot be used in High Availability (HA) mode. For HA, PostgreSQL is strictly required. Using SQLite in a production environment presents an availability risk and should be avoided for mission-critical deployments.
3. **CloudFlare Optimization Conflicts:** CloudFlare optimizations (Auto Minify, Mirage, Rocket Loader) break Wiki.js assets and Vue.js hydration. You must disable these features (often via Page Rules) to ensure the frontend functions correctly and securely.
4. **Git Storage Sync Conflicts:** Git storage sync can conflict with direct database edits. If using Git as a storage backend, ensure strict access controls on the Git repository, as commits directly modify wiki content, bypassing the Wiki.js application layer security.
5. **Port Binding Restrictions:** Binding to ports < 1024 requires `setcap` or iptables redirects. It is significantly safer to run Wiki.js on an unprivileged port (e.g., 3000) and use a reverse proxy to bind to port 443.
6. **Editor Conversion Data Loss:** Converting between the 6 different editors may lose formatting. While not a direct security vulnerability, it can lead to data integrity issues.
7. **Real-time Collaboration:** Wiki.js v2.x does not support real-time collaborative editing. This prevents race conditions but may impact user workflows.

## Conclusion
Securing Wiki.js requires a comprehensive, multi-layered approach. By carefully selecting authentication modules, strictly managing API tokens, hardening the reverse proxy, securing the database connection, and enforcing container security best practices, organizations can safely deploy Wiki.js as a robust and secure enterprise knowledge base. Continuous monitoring, regular updates, and strict access control are essential to maintaining a strong security posture against evolving threats.

## === FILE: 46-wikijs-specialist.md ===
# Wiki.js Comprehensive Specialist Guide (Specialist #46)

## 1. Introduction and Architectural Overview

Wiki.js is a powerful, modern, and open-source wiki platform built on a robust technology stack. As the current stable version (v2.x), it has been designed to offer a highly extensible and performant environment for documentation, knowledge management, and collaborative content creation. Authored by Nicolas Giard under the Requarks organization, Wiki.js is distributed under the AGPL-3.0 license, ensuring that it remains free and open for the community.

### 1.1 Core Technology Stack

The architecture of Wiki.js is built upon several key technologies that work in tandem to deliver a seamless user experience and a highly scalable backend:

- **Backend Framework**: The core of Wiki.js is powered by **Node.js** (requiring version 20 or higher). Node.js provides an asynchronous, event-driven runtime that is highly efficient for handling concurrent requests, making it ideal for a web-based wiki platform.
- **Frontend Framework**: The user interface is constructed using **Vue.js 2**, a progressive JavaScript framework. Vue.js allows for reactive data binding and composable view components. The UI components are styled and structured using **Vuetify**, a Material Design component framework for Vue.js, which ensures a responsive and aesthetically pleasing design across all devices.
- **API Layer**: Communication between the frontend and backend is facilitated entirely through a **GraphQL API**. This endpoint, located at `/graphql`, allows the client to request exactly the data it needs, reducing over-fetching and improving performance. It utilizes Bearer token authentication for secure access.
- **Database ORM**: To interact with various database systems, Wiki.js employs **Objection.js**, an ORM (Object-Relational Mapping) tool built on top of Knex.js. Objection.js provides a powerful and flexible way to define models and relationships, abstracting the underlying SQL queries and enabling support for multiple database engines.

### 1.2 Architectural Principles

The architecture is designed with modularity and extensibility in mind. Features such as authentication, storage, search, and rendering are implemented as modular plugins or extensions. This allows administrators to tailor the platform to their specific needs without modifying the core codebase. The use of GraphQL further decouples the frontend from the backend, enabling third-party integrations and custom client applications to interact with the wiki data seamlessly.

---

## 2. Supported Database Systems

Wiki.js is highly versatile when it comes to data persistence, supporting a wide range of relational database management systems (RDBMS). The choice of database can significantly impact the performance, scalability, and high availability (HA) capabilities of the platform.

### 2.1 PostgreSQL (Recommended)

**PostgreSQL** is the officially recommended database for Wiki.js. It offers the best performance, most robust feature set, and is the **only database supported for High Availability (HA) mode**. When deploying Wiki.js in an enterprise environment or a multi-node cluster, PostgreSQL is mandatory. Furthermore, PostgreSQL provides built-in search capabilities via the `pg_trgm` extension, which can be utilized as a search engine backend.

### 2.2 MySQL 8+ and MariaDB 10.2.7+

Wiki.js supports **MySQL version 8.0 and above**, as well as **MariaDB version 10.2.7 and above**. These are popular choices for many web applications and provide excellent performance for single-node deployments.

**Important Operational Note for MySQL 8+**: Wiki.js does not currently support the `caching_sha2_password` authentication plugin, which is the default in MySQL 8. You must configure the database user to use the `mysql_native_password` plugin. This can be done with the following SQL command:

```sql
ALTER USER 'wikijs'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_secure_password';
FLUSH PRIVILEGES;
```

### 2.3 Microsoft SQL Server (MSSQL) 2012+

For organizations heavily invested in the Microsoft ecosystem, Wiki.js supports **MSSQL 2012 and newer**. This allows seamless integration into existing Windows Server environments and utilizes existing database administration expertise.

### 2.4 SQLite 3.9+

**SQLite** (version 3.9+) is supported for lightweight, single-node deployments, testing, or development environments. It requires no separate database server process, as the database is stored in a single file on disk.

**Critical Limitation**: SQLite **cannot** be used in High Availability (HA) mode. It is strictly for single-instance deployments. Attempting to use SQLite with multiple Wiki.js nodes will result in database corruption and inconsistent state.

---

## 3. Editors and Content Creation

Wiki.js provides a diverse set of editors to cater to different user preferences and content types. Each editor is optimized for a specific workflow.

### 3.1 The 6 Available Editors

1.  **Markdown (contentType: markdown)**: The default and most popular editor. It provides a split-pane view with raw Markdown on the left and a live preview on the right. It supports a wide array of rendering extensions.
2.  **Visual Editor / WYSIWYG (contentType: html)**: A rich text editor designed for users who prefer a Microsoft Word-like experience. It generates HTML directly.
3.  **CKEditor (contentType: html)**: An alternative, highly customizable rich text editor that also outputs HTML. It is often preferred for its advanced formatting options.
4.  **Code (contentType: html)**: A raw code editor with syntax highlighting, ideal for writing raw HTML, CSS, or JavaScript directly into a page.
5.  **API (contentType: yml)**: A specialized editor for documenting APIs, typically using YAML format to define endpoints, parameters, and responses.
6.  **AsciiDoc (contentType: adoc)**: An editor for AsciiDoc, a lightweight markup language similar to Markdown but with more advanced features for technical documentation.

### 3.2 Page Path Rules and Hashing

When creating pages, the URL path is subject to strict validation rules to ensure consistency and prevent routing conflicts:
-   **No dots (`.`)**: File extensions or dot-notation are not allowed in paths.
-   **No spaces**: Spaces must be replaced with hyphens (`-`) or underscores (`_`).
-   **No backslashes (`\`)**: Only forward slashes (`/`) are permitted for defining hierarchy.
-   **No double slashes (`//`)**: Paths must be normalized.
-   **No starting or ending slash**: Paths must be relative to the root, e.g., `engineering/architecture`, not `/engineering/architecture/`.
-   **No special characters**: Paths should generally stick to alphanumeric characters, hyphens, and underscores.

Internally, Wiki.js identifies pages using a unique hash. The **Page Hash** is calculated as the SHA1 checksum of the locale, path, and private namespace:
`Page Hash = SHA1(locale + path + privateNS)`

### 3.3 Editor Limitations

**Warning**: Converting a page between different editors (e.g., from Markdown to WYSIWYG and back) is highly discouraged. Because different editors use different underlying content types (Markdown vs. HTML), converting between them **will likely result in a loss of formatting**, broken layouts, or corrupted content. It is best practice to choose an editor upon page creation and stick with it.

---

## 4. Rendering and Post-Processing Extensions

Wiki.js boasts a powerful rendering pipeline that transforms raw input (like Markdown) into the final HTML presented to the user. This pipeline is highly extensible.

### 4.1 Markdown Rendering Extensions (14 Modules)

For the Markdown editor, Wiki.js supports 14 rendering extensions that add specialized syntax and features:
1.  **core**: The standard Markdown parser.
2.  **abbr**: Support for abbreviations.
3.  **emoji**: Renders standard emoji shortcodes (e.g., `:smile:`).
4.  **expandtabs**: Converts tabs to spaces for consistent alignment.
5.  **footnotes**: Support for Markdown footnotes.
6.  **imsize**: Allows specifying image dimensions in Markdown syntax.
7.  **katex**: Fast math typesetting using KaTeX.
8.  **kroki**: Renders diagrams from textual descriptions using the Kroki API.
9.  **mathjax**: Alternative math typesetting using MathJax.
10. **multi-table**: Advanced table formatting.
11. **pivot-table**: Creates interactive pivot tables from data.
12. **plantuml**: Renders UML diagrams using PlantUML.
13. **supsub**: Support for superscript and subscript.
14. **tasklists**: Renders GitHub-style task lists (checkboxes).

### 4.2 HTML Post-Processing Extensions (11 Modules)

After the initial rendering (or directly from HTML editors), the content passes through 11 HTML post-processors:
1.  **core**: Basic HTML cleanup and structuring.
2.  **asciinema**: Embeds Asciinema terminal recordings.
3.  **blockquotes**: Enhances blockquote styling.
4.  **codehighlighter**: Applies syntax highlighting to code blocks using Prism.js.
5.  **diagram (draw.io)**: Embeds interactive draw.io diagrams.
6.  **image-prefetch**: Optimizes image loading.
7.  **mediaplayers**: Embeds audio and video players.
8.  **mermaid**: Renders Mermaid.js diagrams directly in the browser.
9.  **security**: **Crucial module**. Sanitizes HTML to prevent XSS attacks.
10. **tabset**: Creates interactive tabbed content areas.
11. **twemoji**: Replaces native emojis with Twitter's Twemoji for cross-platform consistency.

**Security Note**: The `security` post-processor is active by default and will strip out custom HTML tags, inline styles, and scripts that are not explicitly whitelisted. If users complain that their custom HTML or iframe embeds are disappearing upon saving, this sanitizer is the cause. It can be configured in the administration panel, but disabling it entirely poses a significant security risk.

---

## 5. Authentication Modules

Enterprise environments require flexible authentication. Wiki.js supports an impressive array of **21 authentication modules**, allowing integration with virtually any identity provider (IdP).

The supported modules include:
1. Auth0
2. Azure AD
3. CAS (Central Authentication Service)
4. Discord
5. Dropbox
6. Facebook
7. Firebase
8. GitHub
9. GitLab
10. Google
11. Keycloak
12. LDAP / Active Directory
13. Local (Built-in username/password)
14. Microsoft
15. OAuth2 (Generic)
16. OIDC (OpenID Connect)
17. Okta
18. Rocket.chat
19. SAML 2.0
20. Slack
21. Twitch

This extensive list ensures that whether an organization uses a legacy LDAP server, a modern cloud IdP like Okta or Azure AD, or social logins for a public wiki, Wiki.js can accommodate the requirement.

---

## 6. Storage Backends

Data backup and synchronization are critical for disaster recovery. Wiki.js supports **11 storage backends** to automatically sync your content to external services.

The supported storage targets are:
1. Azure Blob Storage
2. Box
3. DigitalOcean Spaces
4. Disk (Local file system)
5. Dropbox
6. Google Drive
7. Git (Bidirectional sync)
8. OneDrive
9. S3 (Amazon Web Services)
10. S3 Generic (MinIO, Wasabi, etc.)
11. SFTP

### 6.1 The Git Storage Conflict Issue

The **Git** storage backend is particularly popular as it allows bidirectional synchronization. You can edit a page in Wiki.js, and it commits to Git. Conversely, you can push a Markdown file to the Git repository, and Wiki.js will ingest it.

**Operational Hazard**: Git storage sync can conflict with direct database edits. If a user edits a page via the Wiki.js UI at the exact same time a commit is pushed to the Git repository modifying the same page, a race condition occurs. Wiki.js attempts to handle this gracefully, but in worst-case scenarios, one set of changes may overwrite the other. It is recommended to establish clear workflows: either treat the Wiki UI as the single source of truth and Git as a read-only backup, or treat Git as the source of truth and disable UI editing for those specific paths.

---

## 7. Search Engines

A wiki is only as good as its search functionality. Wiki.js provides **8 search engine integrations** to scale from small personal wikis to massive enterprise knowledge bases.

1.  **Algolia**: A powerful, hosted search API.
2.  **AWS CloudSearch**: Amazon's managed search service.
3.  **Azure Search**: Microsoft's cloud search offering.
4.  **Database (built-in)**: Basic ILIKE/LIKE queries. Good for small wikis but scales poorly.
5.  **Elasticsearch**: The industry standard for enterprise search. Highly recommended for large deployments.
6.  **Manticore Search**: A fast, open-source search engine.
7.  **PostgreSQL (pg_trgm)**: Utilizes PostgreSQL's trigram matching. An excellent middle-ground that requires no extra infrastructure if you are already using PostgreSQL.
8.  **Solr**: Apache Solr, another robust enterprise search platform.
9.  **Sphinx**: A classic open-source full-text search server.

---

## 8. Page CRUD Operations via GraphQL API

Wiki.js is built API-first. Every action available in the UI can be performed programmatically via the GraphQL API located at `/graphql`.

### 8.1 Authentication

API requests require a Bearer token. You must generate an API key in the Administration -> API Access section and include it in the HTTP headers:
`Authorization: Bearer YOUR_API_KEY`

### 8.2 API Rate Limiting Limitation

**Critical Limitation**: Wiki.js has **no native API rate limiting**. If you expose the GraphQL API to the public internet or untrusted networks, a malicious actor could easily overwhelm the Node.js process with complex queries or brute-force attacks.
**Mitigation**: You **must** implement rate limiting at the reverse proxy layer (e.g., Nginx, HAProxy, Traefik, or Cloudflare) before traffic reaches the Wiki.js container.

### 8.3 GraphQL Examples

Here are practical examples of performing CRUD operations on pages.

**Create a Page (Mutation)**
```graphql
mutation {
  pages {
    create(
      content: "# Hello World\nThis is a test page."
      description: "A test page created via API"
      editor: "markdown"
      isPublished: true
      isPrivate: false
      locale: "en"
      path: "api-test/hello-world"
      tags: ["api", "test"]
      title: "Hello World API"
    ) {
      responseResult {
        succeeded
        errorCode
        slug
        message
      }
      page {
        id
        path
      }
    }
  }
}
```

**Read a Page (Query)**
```graphql
query {
  pages {
    single(id: 123) {
      id
      title
      path
      content
      createdAt
      updatedAt
      authorName
    }
  }
}
```

**Update a Page (Mutation)**
```graphql
mutation {
  pages {
    update(
      id: 123
      content: "# Updated Content\nThis page was updated."
      title: "Updated Title"
    ) {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

**Delete a Page (Mutation)**
```graphql
mutation {
  pages {
    delete(id: 123) {
      responseResult {
        succeeded
        message
      }
    }
  }
}
```

---

## 9. Version History System

Wiki.js features a robust version history system. It takes an **automatic snapshot on every update**. Whenever a user saves a page, the previous state is preserved in the database. Users can view the history of a page, compare differences between versions, and restore previous versions if necessary. This provides a safety net against accidental deletions or malicious edits.

---

## 10. Permissions Model

Security and access control are managed through a granular permissions model based on user groups. Permissions are divided into specific scopes.

Key permissions include:
-   **read:pages**: Allows viewing published pages.
-   **write:pages**: Allows creating new pages and editing existing ones.
-   **manage:pages**: Allows moving, renaming, and altering metadata of pages.
-   **delete:pages**: Allows permanently deleting pages.
-   **write:styles**: Allows injecting custom CSS into the wiki. (High risk, grant only to trusted admins).
-   **write:scripts**: Allows injecting custom JavaScript. (Highest risk, potential for XSS, grant only to trusted admins).
-   **read:source**: Allows viewing the raw source code (e.g., raw Markdown) of a page.
-   **read:history**: Allows viewing the version history of a page.
-   **manage:system**: Grants full access to the administration panel.

Administrators can assign these permissions globally or restrict them to specific page paths using Page Rules, allowing for complex organizational structures (e.g., the HR group can only write to `/hr/*`).

---

## 11. Deployment Options and Infrastructure

Wiki.js is designed to be deployed in modern containerized environments, though manual installation is possible.

### 11.1 Docker Deployment

The most common and supported method is via Docker. The official image is hosted on the GitHub Container Registry: `ghcr.io/requarks/wiki`.

A standard `docker-compose.yml` for a PostgreSQL-backed instance looks like this:

```yaml
version: "3"
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: wiki
      POSTGRES_PASSWORD: wikijsrocks
      POSTGRES_USER: wikijs
    volumes:
      - db-data:/var/lib/postgresql/data

  wiki:
    image: ghcr.io/requarks/wiki:2
    environment:
      DB_TYPE: postgres
      DB_HOST: db
      DB_PORT: 5432
      DB_USER: wikijs
      DB_PASS: wikijsrocks
      DB_NAME: wiki
    ports:
      - "3000:3000"
    depends_on:
      - db
    restart: unless-stopped

  wiki-update-companion:
    image: ghcr.io/requarks/wiki-update-companion:latest
    environment:
      - WIKI_CONTAINER_NAME=wiki
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    restart: unless-stopped

volumes:
  db-data:
```

**Crucial Note on Updates**: The `wiki-update-companion` container is required if you want to use the built-in updater in the Wiki.js admin panel. It communicates with the Docker socket to pull the new image and restart the main container. However, **the `wiki-update-companion` container itself must be updated separately** (e.g., via Watchtower or manual `docker pull`).

### 11.2 Kubernetes Deployment

For enterprise scale, Wiki.js provides an **official Helm chart**. This allows for easy deployment, scaling, and management within a Kubernetes cluster. The Helm chart supports configuring ingress, persistent volumes, and connecting to external database clusters.

### 11.3 Deployment Limitations and Gotchas

1.  **Subfolder Installation**: Wiki.js **cannot be installed in a subfolder** (e.g., `https://example.com/wiki/`). It strictly requires its own subdomain or root domain (e.g., `https://wiki.example.com/`). This is a hard limitation of the Vue.js router configuration.
2.  **Privileged Ports**: By default, Node.js cannot bind to ports below 1024 (like 80 or 443) without root privileges. Running the container as root is a security risk. If you must bind directly to these ports without a reverse proxy, you must use `setcap` on the Node binary or configure `iptables` redirects. The best practice is to run Wiki.js on port 3000 and use a reverse proxy (Nginx/Traefik) to handle ports 80/443 and SSL termination.
3.  **Cloudflare Optimization Conflicts**: If you place Wiki.js behind Cloudflare, you **must disable** Auto Minify (JS/CSS/HTML), Mirage, and Rocket Loader. These Cloudflare optimizations aggressively modify the DOM and script loading order, which breaks the Vue.js hydration process, resulting in a blank page or broken assets.

---

## 12. Configuration and High Availability (HA)

The core configuration of Wiki.js is managed via a `config.yml` file. When using Docker, these values are typically overridden by environment variables.

### 12.1 The config.yml File

Key parameters include:
-   `port`: The port the Node.js server listens on (default 3000).
-   `db`: Database connection details (type, host, port, user, pass, db).
-   `ssl`: Configuration for built-in HTTPS (usually handled by a reverse proxy instead).
-   `pool`: Database connection pool settings (min/max connections).
-   `bindIP`: The IP address to bind to (default `0.0.0.0`).
-   `logLevel`: Logging verbosity (info, warn, error, debug).
-   `ha`: High Availability toggle.
-   `dataPath`: Location for local file storage.
-   `bodyParserLimit`: Maximum size for incoming requests (useful for large uploads).

### 12.2 High Availability (HA) Mode

To run multiple instances of Wiki.js behind a load balancer for redundancy and scale, you must enable HA mode.

**Requirements for HA:**
1.  **PostgreSQL is strictly required**. MySQL, MariaDB, MSSQL, and SQLite are not supported for HA.
2.  You must set `ha: true` in the `config.yml` (or `HA_ACTIVE=true` via environment variable) on all nodes.
3.  All nodes must connect to the same PostgreSQL database cluster.
4.  You must use an external search engine (like Elasticsearch or PostgreSQL pg_trgm). The built-in database search may behave inconsistently across nodes.
5.  Storage must be centralized (e.g., S3, Azure Blob) rather than local disk, so all nodes have access to the same assets.

When `ha: true` is set, Wiki.js utilizes PostgreSQL's LISTEN/NOTIFY pub/sub system to broadcast cache invalidations and configuration changes across all connected nodes instantly.

---

## 13. Advanced Troubleshooting and Customization

### 13.1 Custom JavaScript Execution

Administrators can inject custom JavaScript via the admin panel. However, because Wiki.js is a Single Page Application (SPA) built with Vue.js, standard `document.addEventListener('DOMContentLoaded', ...)` will not work as expected when navigating between pages.

**Rule**: Custom JS must hook into the Wiki.js lifecycle using the global boot object:
```javascript
window.boot.register('page-ready', function() {
    // Your custom code here. This runs every time a page finishes rendering.
    console.log("Page loaded and rendered!");
});
```

### 13.2 No Real-Time Collaborative Editing

**Known Limitation**: Wiki.js does **not** support real-time collaborative editing (like Google Docs or Etherpad). If two users edit the same page simultaneously, the last one to save will overwrite the other's changes. The version history will capture both, but manual merging is required.

---

## 14. Relation to Other Specialist Files

This file (Specialist #46) serves as the comprehensive guide to the Wiki.js platform. It relates to the other 6 specialist files in the repository in the following ways:

1.  **Specialist #40 (PostgreSQL Architecture)**: As PostgreSQL is the recommended database and strictly required for HA mode in Wiki.js, Specialist #40 provides the necessary deep dive into tuning, scaling, and managing the database backend that powers this wiki.
2.  **Specialist #41 (Node.js Performance Tuning)**: Wiki.js is a Node.js application. The principles of event loop monitoring, memory management, and garbage collection detailed in Specialist #41 are directly applicable to optimizing the Wiki.js backend process.
3.  **Specialist #42 (GraphQL API Security)**: Wiki.js relies entirely on a GraphQL API. Specialist #42 covers advanced techniques for securing GraphQL endpoints, which is critical for Wiki.js given its lack of native rate limiting and the potential for complex query abuse.
4.  **Specialist #43 (Vue.js SPA Deployment)**: The frontend of Wiki.js is a Vue.js Single Page Application. Specialist #43 provides context on how SPAs are built, hydrated, and served, explaining why Cloudflare optimizations break Wiki.js and why subfolder deployments are unsupported.
5.  **Specialist #44 (Docker & Helm Orchestration)**: This file outlines the deployment of Wiki.js via Docker and Kubernetes. Specialist #44 provides the foundational knowledge required to manage these containerized deployments, handle persistent volumes, and configure ingress controllers.
6.  **Specialist #45 (Enterprise Identity Providers)**: Wiki.js supports 21 authentication modules. Specialist #45 details the protocols (SAML, OIDC, OAuth2) and configurations required to integrate platforms like Wiki.js with enterprise IdPs such as Azure AD, Okta, and Keycloak.

By understanding the interplay between these technologies, an administrator can deploy, secure, and scale Wiki.js to meet the demands of any enterprise environment.

## === FILE: 46-wikijs-troubleshooting.md ===
# Wiki.js Troubleshooting and Operations Guide

Welcome to the definitive troubleshooting and operations guide for Wiki.js (v2.x). Wiki.js is a powerful, open-source (AGPL-3.0) wiki platform built on Node.js (>= 20), Vue.js 2, Vuetify, and a robust GraphQL API. While it offers extensive features including 6 editors, 14 Markdown rendering extensions, 11 HTML post-processing extensions, 21 authentication modules, 11 storage backends, and 8 search engines, operating it in production can present unique challenges.

This guide covers the most common and complex issues encountered by system administrators, DevOps engineers, and technical support teams when deploying and maintaining Wiki.js.

---

## 1. Installation and Deployment Limitations

### 1.1 Cannot Install in Subfolder (Subdomain Only)
**Symptom:** Attempting to serve Wiki.js from a subfolder (e.g., `https://example.com/wiki/`) results in broken assets, routing failures, and API errors.
**Root Cause:** Wiki.js v2.x is strictly designed to run at the root of a domain or subdomain. The Vue.js frontend router and GraphQL API endpoints are hardcoded to expect the root path `/`.
**Resolution:** 
You must deploy Wiki.js on a dedicated subdomain (e.g., `https://wiki.example.com`). If you absolutely must serve it under a main domain, you can use a reverse proxy to handle the subdomain routing, but the application itself must believe it is at the root.
*Note: Subfolder support is a known limitation and is not supported in the 2.x branch.*

### 1.2 Port Binding Issues (Ports < 1024)
**Symptom:** Wiki.js fails to start when configured to run on port 80 or 443, throwing an `EACCES: permission denied` error.
**Root Cause:** By default, Linux prevents non-root users from binding to privileged ports (ports below 1024). Running Node.js as root is a severe security risk.
**Resolution:**
There are three recommended ways to resolve this:
1. **Reverse Proxy (Recommended):** Run Wiki.js on a high port (e.g., 3000) and use Nginx, Apache, Caddy, or Traefik to proxy traffic from port 80/443 to port 3000.
2. **Setcap:** Grant the Node.js binary permission to bind to privileged ports:
   ```bash
   sudo setcap cap_net_bind_service=+ep /usr/bin/node
   ```
3. **iptables Redirect:** Forward traffic from port 80 to 3000 at the firewall level:
   ```bash
   sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3000
   ```

---

## 2. Reverse Proxy and CDN Issues

### 2.1 Cannot Upload Large Files
**Symptom:** Uploading files larger than a few megabytes fails with a `413 Payload Too Large` error or simply times out.
**Root Cause:** This is almost always caused by the reverse proxy (Nginx, Apache, etc.) or the `bodyParserLimit` in Wiki.js `config.yml`.
**Resolution:**
1. **Nginx:** Increase the `client_max_body_size` in your Nginx configuration block:
   ```nginx
   server {
       client_max_body_size 100M;
       # ... other config
   }
   ```
2. **Wiki.js Config:** Ensure the `bodyParserLimit` in `config.yml` is set high enough (default is usually sufficient, but check if modified):
   ```yaml
   bodyParserLimit: 100mb
   ```
3. **Cloudflare:** If using Cloudflare, note that the Free plan limits uploads to 100MB per request.

### 2.2 Cloudflare Breaking Assets
**Symptom:** The Wiki.js interface looks broken, icons are missing, scripts fail to load, or the page remains blank.
**Root Cause:** Cloudflare's aggressive optimization features interfere with Vue.js and Vuetify's dynamic asset loading and script execution.
**Resolution:**
You must disable specific Cloudflare optimizations for your Wiki.js domain. In the Cloudflare dashboard, navigate to your domain and disable:
- **Auto Minify:** Disable for JavaScript, CSS, and HTML. Wiki.js already minifies its assets.
- **Rocket Loader:** This alters the execution order of scripts and completely breaks Vue.js initialization. **Must be OFF.**
- **Mirage:** Disable image optimization that alters DOM loading.
Create a Page Rule in Cloudflare for `*wiki.yourdomain.com/*` to explicitly disable these features.

### 2.3 SSL Redirect Loops
**Symptom:** Accessing the wiki results in an `ERR_TOO_MANY_REDIRECTS` error in the browser.
**Root Cause:** The reverse proxy is handling SSL (HTTPS) and forwarding the request to Wiki.js via HTTP, but Wiki.js is configured to force HTTPS or the Site URL in the database is mismatched.
**Resolution:**
1. Ensure your reverse proxy passes the correct headers:
   ```nginx
   proxy_set_header X-Forwarded-Proto $scheme;
   ```
2. If you cannot access the admin panel to fix the Site URL, you must fix it directly in the database. Connect to your database (e.g., PostgreSQL) and run:
   ```sql
   UPDATE settings SET value = '{"host":"https://wiki.example.com"}' WHERE key = 'host';
   ```
   Restart the Wiki.js process after modifying the database.

---

## 3. Database and High Availability (HA)

### 3.1 MySQL caching_sha2_password Error
**Symptom:** Wiki.js fails to connect to a MySQL 8+ database, logging `ER_NOT_SUPPORTED_AUTH_MODE: Client does not support authentication protocol requested by server; consider upgrading MySQL client`.
**Root Cause:** MySQL 8 defaults to the `caching_sha2_password` authentication plugin, which the underlying Node.js MySQL driver used by Wiki.js does not fully support in all environments.
**Resolution:**
You must change the authentication plugin for the Wiki.js database user to `mysql_native_password`.
Log into MySQL as root and execute:
```sql
ALTER USER 'wiki'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_strong_password';
FLUSH PRIVILEGES;
```

### 3.2 High Availability (HA) Mode Cache Issues
**Symptom:** In a multi-node deployment, users see stale content, or updates made on one node do not reflect on others.
**Root Cause:** HA mode is not properly configured, or an unsupported database is being used.
**Resolution:**
1. **Database Requirement:** HA mode **requires** PostgreSQL. SQLite, MySQL, MariaDB, and MSSQL cannot be used for HA because Wiki.js relies on PostgreSQL's `LISTEN/NOTIFY` pub/sub mechanism to invalidate caches across nodes.
2. **Configuration:** Ensure `ha: true` is set in the `config.yml` of **every** node.
   ```yaml
   ha: true
   ```
3. **Clock Sync:** Ensure all nodes have their system clocks synchronized via NTP.

---

## 4. Content and Editor Troubleshooting

### 4.1 HTML Sanitization Stripping Content
**Symptom:** Custom HTML tags, iframes, or inline styles are removed when saving a page using the WYSIWYG or Code editors.
**Root Cause:** Wiki.js includes a strict HTML security sanitizer (one of its 11 HTML post-processing extensions) enabled by default to prevent XSS attacks.
**Resolution:**
If you trust your authors and need custom HTML:
1. Go to **Administration > Rendering > HTML**.
2. Locate the **Security** tab.
3. You can either disable the sanitizer entirely (not recommended for public wikis) or configure the allowed tags and attributes.
4. To allow iframes (e.g., for YouTube embeds), add `iframe` to the allowed tags and `src`, `width`, `height`, `allowfullscreen` to the allowed attributes.

### 4.2 Custom JS Not Executing
**Symptom:** JavaScript added via the Code Injection settings or within pages does not run when navigating between pages.
**Root Cause:** Wiki.js is a Single Page Application (SPA). Standard `window.onload` or `document.addEventListener('DOMContentLoaded', ...)` events only fire once on the initial page load, not on subsequent SPA navigations.
**Resolution:**
You must use the Wiki.js specific boot registration pattern. Wrap your custom JavaScript as follows:
```javascript
window.boot.register('page-ready', function() {
    // Your custom code here
    console.log('Page has fully loaded and rendered!');
});
```

### 4.3 Editor Conversion Data Loss
**Symptom:** Switching a page from the Markdown editor to the WYSIWYG editor, or vice versa, results in lost formatting or broken content.
**Root Cause:** The 6 different editors (markdown, wysiwyg, ckeditor, code, api, asciidoc) store data differently. Converting between them is not a 1:1 lossless process. Markdown to HTML is one-way; HTML back to Markdown relies on heuristics and often fails on complex layouts.
**Resolution:**
- **Best Practice:** Choose one editor standard for your team and stick to it.
- **Recovery:** If data is lost during conversion, Wiki.js automatically creates a snapshot on every update. Go to the page's **History** tab and restore the previous version.

### 4.4 Page Creation Failures
**Symptom:** Users cannot create a new page, receiving an error about invalid paths or duplicate content.
**Root Cause:** Wiki.js enforces strict rules on page paths.
**Resolution:**
- **Path Rules:** Page paths cannot contain dots (`.`), spaces, backslashes (`\`), or double slashes (`//`). They cannot start or end with a slash.
- **Duplicate Path:** Ensure the path isn't already taken. The page hash is calculated as `SHA1(locale + path + privateNS)`.
- **Empty Content:** A page must have at least some content to be saved.

---

## 5. System and Integration Failures

### 5.1 Upgrade Button Not Working
**Symptom:** Clicking the "Upgrade" button in the Administration panel does nothing or throws an error, especially in Docker environments.
**Root Cause:** The main Wiki.js Node process cannot overwrite its own files while running, especially inside a containerized environment where the filesystem might be read-only or ephemeral.
**Resolution:**
For Docker deployments (`ghcr.io/requarks/wiki`), you must use the `wiki-update-companion` container.
1. Ensure the companion container is running and mapped to the same volume as the main wiki container.
2. The companion container handles the actual file replacement and restarts the main process.
3. Alternatively, update by pulling the latest Docker image and recreating the container:
   ```bash
   docker pull ghcr.io/requarks/wiki:2
   docker-compose up -d
   ```

### 5.2 Git Storage Sync Conflicts
**Symptom:** The Git storage backend stops syncing, or pages edited in the UI are overwritten by old versions from Git.
**Root Cause:** Git storage sync can conflict with direct database edits or simultaneous edits. If a merge conflict occurs, the Wiki.js Git extension (which uses simple git commands) may halt.
**Resolution:**
1. **Check Logs:** Look at the Wiki.js logs for Git merge conflict errors.
2. **Manual Resolution:** Access the server, navigate to the local Git repository used by Wiki.js, and manually resolve the conflict using standard Git commands (`git status`, `git merge --abort`, etc.).
3. **Force Sync:** In the Admin panel under Storage, you can force a push or pull, but this may overwrite data. Always backup the database first.

### 5.3 Search Engine Not Indexing
**Symptom:** New pages do not appear in search results.
**Root Cause:** The search index is out of sync, or the configured search engine (e.g., Elasticsearch, PostgreSQL pg_trgm) is unreachable.
**Resolution:**
1. Go to **Administration > Search Engine**.
2. Click **Rebuild Index**.
3. If using PostgreSQL (`pg_trgm`), ensure the extension is installed in the database:
   ```sql
   CREATE EXTENSION IF NOT EXISTS pg_trgm;
   ```
4. Check the GraphQL API logs for indexing errors.

### 5.4 Telegram/Email Notification Failures
**Symptom:** Users do not receive password reset emails or Telegram notifications.
**Root Cause:** Incorrect SMTP settings, blocked ports, or invalid Telegram bot tokens.
**Resolution:**
- **Email:** Verify SMTP host, port (usually 587 for TLS or 465 for SSL), and credentials. Ensure your hosting provider (e.g., DigitalOcean, AWS) does not block outbound port 25/587.
- **Telegram:** Ensure the Bot Token is correct and the bot has been started by the user. Check the Wiki.js logs for `TELEGRAM_API_ERROR`.

### 5.5 Session Problems and Slow Loading Times
**Symptom:** Users are frequently logged out, or the wiki takes a long time to load.
**Root Cause:** Session issues are often tied to reverse proxy misconfigurations (dropping cookies) or database latency. Slow loading is usually due to large assets, unoptimized databases, or lack of caching.
**Resolution:**
- **Sessions:** Ensure your reverse proxy passes the `X-Forwarded-For` and `X-Forwarded-Proto` headers. If using multiple nodes without HA mode, sessions will not be shared.
- **Performance:** 
  - Use PostgreSQL.
  - Enable Redis for caching if supported in your architecture.
  - Ensure Cloudflare is configured correctly (see section 2.2).
  - Check the `config.yml` `logLevel` (set to `info` or `warn` in production, not `debug`).

### 5.6 Menu Items Showing Keys Instead of Text
**Symptom:** The navigation menu or UI elements show translation keys like `locales.en.menu.home` instead of the actual text.
**Root Cause:** The locale files failed to load, or the configured locale is missing/corrupted.
**Resolution:**
1. Go to **Administration > Locale**.
2. Ensure the desired locale is downloaded and set as default.
3. Click the cloud icon to force an update of the locale files from the Requarks servers.
4. Restart the Wiki.js process to flush the locale cache.

---

## 6. Advanced Debugging via GraphQL

Wiki.js relies heavily on its GraphQL API endpoint at `/graphql`. When the UI fails, you can often diagnose issues by querying the API directly.

### 6.1 Authenticating API Requests
You must use a Bearer token for API requests. Generate an API token in the Administration panel under **API Access**.

```bash
curl -X POST   -H "Content-Type: application/json"   -H "Authorization: Bearer YOUR_API_TOKEN"   -d '{"query": "{ site { title } }"}'   https://wiki.example.com/graphql
```

### 6.2 Checking System Status
Query the system status to verify database connectivity and version info:

```graphql
query {
  system {
    version
    dbVersion
    nodejsVersion
  }
}
```

### 6.3 Verifying Permissions
If a user cannot access a page, verify their group permissions. Wiki.js uses granular permissions like `read:pages`, `write:pages`, `manage:pages`, `delete:pages`, `write:styles`, `write:scripts`, `read:source`, `read:history`, `manage:system`.

---

## 7. Deep Dive: Understanding Wiki.js Architecture

To effectively troubleshoot Wiki.js, it is crucial to understand its underlying architecture and how its various components interact.

### 7.1 The Node.js Backend
Wiki.js is built on Node.js (requiring version 20 or higher for the latest 2.x releases). The backend is responsible for handling API requests, managing database connections, processing authentication, and serving the initial HTML payload. It uses a modular architecture where features like authentication, storage, and search are implemented as plugins.

### 7.2 The Vue.js Frontend
The frontend is a Single Page Application (SPA) built with Vue.js 2 and the Vuetify UI framework. When a user navigates to a page, the frontend requests the page data via the GraphQL API and renders it dynamically. This SPA architecture is why custom JavaScript must be registered using `window.boot.register` rather than standard DOM events.

### 7.3 The GraphQL API
Almost all communication between the frontend and backend occurs via the GraphQL API. This API is also available for external integrations. Understanding how to query this API is essential for advanced troubleshooting, as it can reveal information not always visible in the UI.

### 7.4 Storage Backends
Wiki.js supports 11 different storage backends, including local disk, Git, S3, and various cloud providers. The storage system is designed to be pluggable, allowing administrators to choose the best option for their infrastructure. However, this flexibility can also introduce complexity, especially when dealing with synchronization issues or permission errors.

### 7.5 Search Engines
The platform supports 8 different search engines, ranging from the built-in database search to powerful external engines like Elasticsearch and Algolia. Choosing the right search engine depends on the size of the wiki and the required search capabilities. Troubleshooting search issues often involves verifying the connection to the search engine and ensuring the index is up to date.

### 7.6 Authentication Modules
With 21 supported authentication modules, Wiki.js can integrate with almost any identity provider. Configuring these modules can be complex, and troubleshooting often involves checking the configuration settings, verifying the identity provider's response, and examining the Wiki.js logs for authentication errors.

---

## 8. Best Practices for Production Deployments

To minimize issues and ensure a stable Wiki.js deployment, follow these best practices:

### 8.1 Use PostgreSQL
While Wiki.js supports multiple databases, PostgreSQL is the recommended choice for production deployments. It is required for High Availability (HA) mode and generally offers better performance and reliability than other options.

### 8.2 Implement a Robust Backup Strategy
Regularly backup both the database and the storage backend. Wiki.js's built-in snapshot feature is useful for recovering individual pages, but a comprehensive backup strategy is essential for disaster recovery.

### 8.3 Monitor System Performance
Monitor the performance of the Node.js process, the database, and the reverse proxy. Use tools like Prometheus and Grafana to track key metrics and set up alerts for potential issues.

### 8.4 Keep Wiki.js Updated
Regularly update Wiki.js to the latest stable version to benefit from bug fixes, security patches, and new features. If using Docker, ensure the `wiki-update-companion` container is configured correctly to facilitate seamless updates.

### 8.5 Secure the Deployment
Implement strong security measures, including HTTPS, firewall rules, and regular security audits. Review the HTML sanitization settings to ensure they align with your security requirements.

---

## 9. Conclusion

Operating Wiki.js in production requires a solid understanding of Node.js environments, reverse proxy configurations, and database management. By adhering to the architectural requirements (like using PostgreSQL for HA and avoiding subfolder deployments) and understanding the nuances of its SPA architecture and security sanitizers, you can maintain a stable and highly performant knowledge base. Always remember to leverage the built-in snapshot version history and keep regular database backups to prevent data loss during editor conversions or storage sync conflicts.

