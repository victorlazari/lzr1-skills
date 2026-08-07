# Next.js App Router

## Overview
The App Router is the new paradigm for building Next.js applications, introduced in Next.js 13. It leverages React Server Components, nested layouts, and simplified data fetching.

## Key Concepts
- **Server Components:** Default component type in the App Router. They render on the server and send HTML to the client, reducing bundle size.
- **Client Components:** Use the `"use client"` directive to opt-in to client-side rendering for interactivity.
- **Layouts:** Share UI across multiple routes using `layout.tsx`.
- **Pages:** Define unique UI for a route using `page.tsx`.
- **Routing:** File-system based routing using the `app` directory.

## Data Fetching
- Use `fetch` API directly in Server Components.
- Next.js extends `fetch` to provide caching and revalidation options.
- Avoid using `getServerSideProps` or `getStaticProps` in the App Router.
