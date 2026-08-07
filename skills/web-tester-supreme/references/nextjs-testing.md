# Next.js Testing Guide

**Verified against upstream:** 2026-08-07

## Overview
This guide covers testing Next.js App Router, Server/Client Components, and edge middleware.

## Authoritative Sources
- [Next.js Testing Documentation](https://nextjs.org/docs/app/building-your-application/testing)

## App Router Testing
- Test Server Components by rendering them in a Node.js environment and asserting on the generated HTML.
- Test Client Components using React Testing Library and jsdom.
- Mock Next.js specific APIs (e.g., `next/navigation`, `next/headers`) using Jest or Vitest.

## Edge Middleware
- Test edge middleware by simulating requests and asserting on the responses or modified headers.
- Use a local development server or a dedicated testing environment to validate middleware behavior.

## Best Practices
- Isolate component tests from data fetching by mocking API responses.
- Use E2E tests (e.g., Playwright) to validate the integration of Server and Client Components.
