# Frontend & Mobile Engineering

## Table of Contents
1. Modern Frontend Architecture
2. React & Next.js
3. State Management
4. Performance
5. Accessibility
6. Mobile Development

---

## 1. Modern Frontend Architecture

### Architecture Patterns

| Pattern | Description | Best For |
|---|---|---|
| SPA (Single Page App) | Client-side rendering, JS routing | Dashboards, apps |
| SSR (Server-Side Rendering) | Server renders HTML per request | SEO, dynamic content |
| SSG (Static Site Generation) | Pre-built HTML at build time | Blogs, docs, marketing |
| ISR (Incremental Static Regen) | Static + on-demand revalidation | E-commerce, CMS |
| Islands Architecture | Static HTML + interactive islands | Content-heavy sites |
| Micro-frontends | Independent frontend modules | Large teams, legacy migration |

### Build Tooling (2024-2025)

| Tool | Purpose | Strengths |
|---|---|---|
| Vite | Dev server + bundler | Fast HMR, ESM-native |
| Turbopack | Next.js bundler | Rust-based, incremental |
| esbuild | Bundler/minifier | Extremely fast |
| Biome | Linter + formatter | Fast, unified tooling |
| Bun | Runtime + bundler | All-in-one, fast |

### Component Design Principles

- **Composition over inheritance**: Build complex UIs from simple, composable components
- **Single responsibility**: Each component does one thing well
- **Props down, events up**: Unidirectional data flow
- **Controlled vs uncontrolled**: Prefer controlled components for forms
- **Render props / hooks**: Share behavior without coupling to UI
- **Colocation**: Keep related code (styles, tests, types) close to components

---

## 2. React & Next.js

### React Best Practices (2024-2025)

- Use Server Components by default; Client Components only when needed (interactivity, browser APIs)
- Prefer `use` hook for data fetching in Server Components
- Use React Server Actions for mutations
- Implement Suspense boundaries for loading states
- Use `React.memo`, `useMemo`, `useCallback` only when profiling shows need
- Prefer composition over context for prop drilling solutions
- Use TypeScript for all React code (strict mode)

### Next.js App Router Patterns

```
app/
├── layout.tsx          # Root layout (shared UI)
├── page.tsx            # Home page
├── loading.tsx         # Loading UI (Suspense boundary)
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── api/               # Route handlers
│   └── route.ts
└── dashboard/
    ├── layout.tsx      # Nested layout
    ├── page.tsx        # Dashboard page
    └── [id]/
        └── page.tsx    # Dynamic route
```

**Key Patterns**:
- Parallel routes for simultaneous loading of independent sections
- Intercepting routes for modals and overlays
- Route groups for organization without URL impact
- Middleware for auth, redirects, and request modification

### React Performance

- **Code splitting**: Dynamic imports with `React.lazy` and Suspense
- **Virtualization**: Use `react-window` or `tanstack-virtual` for long lists
- **Image optimization**: Use `next/image` with proper sizing and formats
- **Bundle analysis**: Regular bundle size audits with `@next/bundle-analyzer`
- **Streaming SSR**: Progressive HTML delivery with Suspense

---

## 3. State Management

### State Management Decision Tree

| State Type | Solution | Example |
|---|---|---|
| UI state (local) | `useState`, `useReducer` | Form inputs, toggles |
| Server state | TanStack Query, SWR | API data, cache |
| URL state | `useSearchParams`, router | Filters, pagination |
| Global UI state | Zustand, Jotai | Theme, sidebar open |
| Complex global | Redux Toolkit (if needed) | Large enterprise apps |
| Form state | React Hook Form, Formik | Complex forms |

### Server State (TanStack Query)

```typescript
// Prefer server state libraries over manual useEffect + useState
const { data, isLoading, error } = useQuery({
  queryKey: ['users', filters],
  queryFn: () => fetchUsers(filters),
  staleTime: 5 * 60 * 1000, // 5 minutes
});

// Mutations with optimistic updates
const mutation = useMutation({
  mutationFn: updateUser,
  onMutate: async (newUser) => {
    // Optimistic update
    queryClient.setQueryData(['users'], (old) => /* update */);
  },
  onSettled: () => queryClient.invalidateQueries(['users']),
});
```

---

## 4. Performance

### Core Web Vitals

| Metric | Target | Measures |
|---|---|---|
| LCP (Largest Contentful Paint) | <2.5s | Loading performance |
| INP (Interaction to Next Paint) | <200ms | Interactivity |
| CLS (Cumulative Layout Shift) | <0.1 | Visual stability |

### Performance Optimization Checklist

- **Critical rendering path**: Minimize render-blocking resources
- **Font loading**: Use `font-display: swap`, preload critical fonts
- **Image optimization**: WebP/AVIF, responsive sizes, lazy loading
- **JavaScript**: Code split, tree shake, defer non-critical scripts
- **CSS**: Extract critical CSS, remove unused styles
- **Caching**: Immutable assets with content hashes, CDN caching
- **Prefetching**: Prefetch likely next navigations
- **Service Workers**: Offline support, background sync

### Rendering Performance

- Avoid layout thrashing (batch DOM reads/writes)
- Use CSS `contain` property for layout isolation
- Prefer CSS animations over JavaScript animations
- Use `will-change` sparingly for GPU-accelerated animations
- Implement virtual scrolling for large lists
- Debounce/throttle expensive event handlers

---

## 5. Accessibility

### WCAG 2.2 Compliance

| Level | Requirement | Examples |
|---|---|---|
| A (Minimum) | Basic accessibility | Alt text, keyboard navigation, form labels |
| AA (Standard) | Enhanced accessibility | Color contrast 4.5:1, resize text, focus visible |
| AAA (Enhanced) | Maximum accessibility | Contrast 7:1, sign language, extended audio |

### Accessibility Checklist

- **Semantic HTML**: Use correct elements (`button`, `nav`, `main`, `article`)
- **Keyboard navigation**: All interactive elements reachable and operable
- **ARIA**: Use ARIA roles, states, and properties when semantics insufficient
- **Focus management**: Visible focus indicators, logical tab order
- **Color**: Never use color alone to convey information
- **Forms**: Associated labels, error messages, required field indicators
- **Images**: Meaningful alt text, decorative images marked with `alt=""`
- **Motion**: Respect `prefers-reduced-motion` media query
- **Screen readers**: Test with VoiceOver, NVDA, or JAWS

### Testing Tools

- axe-core (automated testing)
- Lighthouse accessibility audit
- Screen reader testing (manual)
- Keyboard-only navigation testing
- Color contrast checkers

---

## 6. Mobile Development

### Cross-Platform Frameworks

| Framework | Language | Rendering | Best For |
|---|---|---|---|
| React Native | TypeScript/JS | Native components | React teams, shared logic |
| Flutter | Dart | Custom rendering (Skia) | Pixel-perfect UI, performance |
| Expo | TypeScript/JS | React Native + tools | Rapid development, managed |

### React Native Best Practices

- Use Expo for new projects (managed workflow)
- Implement navigation with React Navigation or Expo Router
- Use Reanimated for performant animations (runs on UI thread)
- Implement proper list virtualization (FlashList over FlatList)
- Handle platform differences with `Platform.select` and `.ios.tsx`/`.android.tsx`
- Test on real devices, not just simulators

### Mobile Performance

- **Startup time**: Minimize bundle size, lazy load screens
- **Memory**: Monitor memory usage, avoid memory leaks in subscriptions
- **Battery**: Minimize background processing, batch network requests
- **Network**: Implement offline-first with local storage and sync
- **Animations**: Use native driver, avoid JS thread bottlenecks
- **Images**: Proper caching, progressive loading, correct sizes
