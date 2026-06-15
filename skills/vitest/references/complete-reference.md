# Vitest Unit Testing: Complete Reference

This document serves as a comprehensive, expert-level reference for implementing Vitest unit testing within a modern full-stack Next.js 16 application architecture utilizing React 19, Tailwind CSS v4, and shadcn/ui component primitives. It consolidates advanced mocking strategies, configuration schemas, CLI commands, troubleshooting diagnostics, and security best practices.

## 1. Vitest Architecture and Core Concepts

Vitest is a blazing fast unit testing framework built as a modern alternative to Jest, tightly integrated with the Vite build toolchain. It is optimized for TypeScript-first development and embraces ESM (ECMAScript Modules) and native modern JavaScript features.

### Core Components

-   **Vite Integration**: Vitest integrates seamlessly with Vite, using its module resolution, hot module replacement (HMR), and fast build times.
-   **Native ESM Support**: Vitest leverages Vite's native ESM handling to avoid the overhead of transpiling and bundling test code upfront, resulting in faster test startup and incremental runs.
-   **In-Process Test Execution**: Vitest runs tests within the same Node.js process as the Vite server, reducing inter-process communication overhead and improving test reliability.
-   **Dependency Graph Management**: Vitest uses Vite's dependency graph management to ensure efficient module resolution and caching. Changes in source files trigger minimal invalidations.

### Fast Execution Mechanics

-   **Module Caching**: When a test file imports a module, Vitest requests the module from Vite’s dev server, which returns a cached transformed module if available.
-   **Parallel Test Execution**: Vitest spawns multiple worker threads to parallelize test execution. Each worker runs a subset of tests independently while sharing module caches.
-   **Incremental Test Runs**: In watch mode, Vitest listens to file system events and intelligently reruns only impacted tests based on the dependency graph.

## 2. Advanced Mocking Strategies

Mocking in unit tests is essential to isolate the unit of work and avoid dependencies on external systems.

### Mocking Prisma ORM

An effective mocking approach is to abstract Prisma client calls behind repository adapters following the Hexagonal Architecture pattern.

```typescript
// src/adapters/prismaUserRepository.ts
import { PrismaClient, User } from '@prisma/client';

export interface IUserRepository {
  findUserById(id: string): Promise<User | null>;
}

export class PrismaUserRepository implements IUserRepository {
  constructor(private readonly prisma: PrismaClient) {}
  async findUserById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }
}
```

In unit tests, mock the repository interface:

```typescript
import { describe, it, expect, vi } from 'vitest';
import { IUserRepository } from '@/adapters/prismaUserRepository';
import { UserService } from '@/services/userService';

describe('UserService', () => {
  it('should return user by id', async () => {
    const mockUserRepo: IUserRepository = {
      findUserById: vi.fn().mockResolvedValue({ id: '123', email: 'test@example.com' }),
    };
    const userService = new UserService(mockUserRepo);
    const user = await userService.getUserById('123');
    expect(user).toEqual({ id: '123', email: 'test@example.com' });
  });
});
```

### Mocking Valkey Cache (ioredis)

Mock the `ioredis` client instance methods such as `get`, `set`, `del`, and `expire`.

```typescript
import Redis from 'ioredis';
import { vi } from 'vitest';

vi.mock('ioredis', () => {
  return {
    default: vi.fn().mockImplementation(() => ({
      get: vi.fn((key) => Promise.resolve(mockCache[key] || null)),
      set: vi.fn((key, value) => {
        mockCache[key] = value;
        return Promise.resolve('OK');
      }),
    })),
  };
});

const mockCache: Record<string, string> = {};
```

### Mocking RabbitMQ Queues

Mock the AMQP client by replacing the channel and connection methods.

```typescript
import amqplib from 'amqplib';
import { vi } from 'vitest';

vi.mock('amqplib', () => {
  const channelMock = {
    publish: vi.fn(),
    consume: vi.fn(),
    ack: vi.fn(),
  };
  const connectionMock = {
    createChannel: vi.fn().mockResolvedValue(channelMock),
  };
  return {
    connect: vi.fn().mockResolvedValue(connectionMock),
  };
});
```

## 3. Unit Testing React 19 Components

### Testing Server Components

Server Components are plain functions without lifecycle hooks and can be tested as pure functions using `ReactDOMServer.renderToString`.

```tsx
import React from 'react';
import { renderToString } from 'react-dom/server';
import { ServerComponent } from '@/app/components/ServerComponent';

describe('ServerComponent', () => {
  it('renders expected static markup', () => {
    const html = renderToString(<ServerComponent title="Test" />);
    expect(html).toContain('<h1>Test</h1>');
  });
});
```

### Testing Client Components

Client Components require a DOM environment. Use `@testing-library/react` to render and interact with components.

```tsx
import { render, screen } from '@testing-library/react';
import { Button } from 'shadcn/ui/button';
import React from 'react';

describe('Button component', () => {
  it('renders with correct text and styles', () => {
    render(<Button className="bg-blue-500">Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });
    expect(button).toBeVisible();
    expect(button).toHaveClass('bg-blue-500');
  });
});
```

### Mocking Next.js App Router Hooks

Create manual mocks for `next/navigation` hooks like `useRouter` and `usePathname`.

```typescript
import { renderHook } from '@testing-library/react-hooks';
import { useRouter, usePathname } from 'next/navigation';

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
  }),
  usePathname: () => '/test-path',
}));
```

## 4. Snapshot Testing

Snapshot testing captures the rendered output of React components, serialized objects, or stringified results.

```tsx
import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Button from '@/components/ui/Button';

describe('Button component', () => {
  it('matches the snapshot', () => {
    const { container } = render(<Button variant="primary">Click me</Button>);
    expect(container).toMatchSnapshot();
  });
});
```

## 5. Testing Zod Schemas

Testing Zod schemas ensures input validation is robust and aligns with business rules.

```typescript
import { describe, it, expect } from 'vitest';
import { userSchema } from '@/validation/user';

describe('userSchema validation', () => {
  it('accepts valid user data', () => {
    const data = { id: 'uuid', email: 'test@example.com', name: 'John' };
    expect(() => userSchema.parse(data)).not.toThrow();
  });

  it('rejects invalid email', () => {
    const data = { id: 'uuid', email: 'invalid', name: 'John' };
    expect(() => userSchema.parse(data)).toThrow();
  });
});
```

## 6. Vitest Configuration Schemas

The `vitest.config.ts` file allows extensive customization.

-   `include`: Glob patterns specifying which files to include as test files.
-   `exclude`: Glob patterns for files and directories to exclude.
-   `environment`: The test environment to use (`node`, `jsdom`, `happy-dom`).
-   `coverage`: Configuration options for code coverage reporting (`provider`, `reporters`, `include`, `exclude`).
-   `setupFiles`: List of files to be loaded before the test suite is executed.
-   `maxConcurrency`: Maximum number of test files to run concurrently.

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./vitest.setup.ts'],
    coverage: {
      provider: 'c8',
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

## 7. Vitest CLI Command Reference

-   `vitest`: Starts the test runner in watch mode (dev) or run mode (CI).
-   `vitest run`: Runs the test suite once and exits.
-   `vitest watch`: Starts the test runner in watch mode.
-   `vitest related <files...>`: Runs tests related to a list of source files.
-   `--ui`: Enable the Vitest UI.
-   `--coverage`: Enable coverage report generation.
-   `--update`, `-u`: Update snapshot files.
-   `--shard <shard>`: Test suite shard to execute (e.g., `1/3`).

## 8. Troubleshooting & Diagnostics

Vitest provides a multi-layered diagnostics architecture encompassing error handling, logging, and tracing.

### Common Error Codes

-   `VIT001`: Test Suite Initialization Failure (e.g., syntax errors in config).
-   `VIT002`: Test Case Execution Timeout (e.g., infinite loops, network issues).
-   `VIT003`: Assertion Failure (mismatch between expected and actual results).
-   `VIT004`: Module Not Found (issues with module paths or missing dependencies).

### Logging and Tracing

Configure logging levels (`error`, `warning`, `info`, `debug`) and enable tracing to capture function call sequences and execution times.

## 9. Security Audit Checklist

Ensure the integration of Vitest adheres to stringent security practices.

-   **Environment Configuration**: Do not expose sensitive information in environment variables.
-   **Dependency Management**: Regularly run `npm audit` and lock dependency versions.
-   **Test Code Review**: Ensure no sensitive data is hardcoded in test scripts. Use mocks for sensitive data.
-   **File System Permissions**: Restrict access to test files using role-based access control (RBAC).
-   **CI/CD Security**: Ensure CI/CD tools have minimum required permissions and use secure tokens.
