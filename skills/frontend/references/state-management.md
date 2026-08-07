# State Management

## Local State
- Use `useState` for simple, component-level state.
- Use `useReducer` for complex state logic involving multiple sub-values or when the next state depends on the previous one.

## Global State
- **Context API:** Suitable for low-frequency updates like theme or authentication status.
- **Zustand:** A small, fast, and scalable bearbones state-management solution. Recommended for most global state needs.
- **Redux Toolkit:** Use for complex applications with extensive state requirements and a need for robust devtools.

## Server State
- **React Query (TanStack Query):** Recommended for fetching, caching, synchronizing, and updating server state.
- **SWR:** A React Hooks library for data fetching by Vercel. Good alternative to React Query.
