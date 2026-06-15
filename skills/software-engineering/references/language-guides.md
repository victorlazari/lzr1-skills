# Language & Domain Guides

## Table of Contents
1. Go (Golang)
2. Rust
3. Blockchain & Smart Contracts
4. Embedded Systems
5. Game Development

---

## 1. Go (Golang)

### Go Design Philosophy

- Simplicity over cleverness: explicit is better than implicit
- Composition over inheritance: interfaces + struct embedding
- Concurrency as a first-class citizen: goroutines + channels
- Fast compilation: rapid feedback loop
- Standard library first: minimize external dependencies

### Go Patterns

| Pattern | Implementation | Use Case |
|---|---|---|
| Interface satisfaction | Implicit (no `implements`) | Decoupling, testing |
| Functional options | `WithTimeout(5*time.Second)` | Configurable constructors |
| Table-driven tests | `[]struct{name, input, want}` | Comprehensive testing |
| Context propagation | `context.Context` first param | Cancellation, deadlines |
| Error wrapping | `fmt.Errorf("op: %w", err)` | Error chain with context |
| Worker pool | Goroutines + buffered channel | Bounded concurrency |

### Go Concurrency

```go
// Worker pool pattern
func processItems(ctx context.Context, items []Item, workers int) error {
    g, ctx := errgroup.WithContext(ctx)
    ch := make(chan Item, workers)
    
    // Producer
    g.Go(func() error {
        defer close(ch)
        for _, item := range items {
            select {
            case ch <- item:
            case <-ctx.Done():
                return ctx.Err()
            }
        }
        return nil
    })
    
    // Workers
    for i := 0; i < workers; i++ {
        g.Go(func() error {
            for item := range ch {
                if err := process(ctx, item); err != nil {
                    return err
                }
            }
            return nil
        })
    }
    
    return g.Wait()
}
```

### Go Best Practices

- Accept interfaces, return structs
- Keep interfaces small (1-3 methods)
- Use `context.Context` for cancellation and request-scoped values
- Handle errors explicitly; don't ignore them
- Use `defer` for cleanup (close files, unlock mutexes)
- Avoid global state; use dependency injection
- Use `go vet`, `staticcheck`, and `golangci-lint`
- Write table-driven tests with meaningful subtests
- Use `sync.Pool` for frequently allocated objects
- Profile with `pprof` before optimizing

---

## 2. Rust

### Rust Core Concepts

| Concept | Purpose | Key Rule |
|---|---|---|
| Ownership | Memory safety without GC | Each value has one owner |
| Borrowing | Shared access to data | Multiple `&T` OR one `&mut T` |
| Lifetimes | Reference validity | References can't outlive data |
| Traits | Polymorphism | Like interfaces + default impls |
| Enums + Pattern matching | Type-safe state machines | Exhaustive matching |
| Result/Option | Error handling | No null, no exceptions |

### Rust Error Handling

```rust
// Use thiserror for library errors
#[derive(Debug, thiserror::Error)]
enum AppError {
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("not found: {entity} with id {id}")]
    NotFound { entity: &'static str, id: String },
    #[error("validation failed: {0}")]
    Validation(String),
}

// Use anyhow for application errors
fn main() -> anyhow::Result<()> {
    let config = load_config().context("failed to load configuration")?;
    run_server(config).context("server failed")?;
    Ok(())
}
```

### Rust Async

- Use `tokio` as the async runtime (de facto standard)
- Prefer `async fn` over manual `Future` implementations
- Use `tokio::select!` for concurrent operations
- Avoid holding locks across `.await` points
- Use `Arc<Mutex<T>>` for shared mutable state (prefer channels when possible)
- Consider `rayon` for CPU-bound parallelism (not async)

### Rust Best Practices

- Use `clippy` for idiomatic code suggestions
- Prefer `&str` over `String` in function parameters
- Use builder pattern for complex struct construction
- Implement `Display` and `Debug` for all public types
- Use `#[must_use]` for functions whose return value shouldn't be ignored
- Leverage the type system to make invalid states unrepresentable
- Use `cargo bench` with Criterion for benchmarking
- Minimize `unsafe` code; encapsulate it behind safe abstractions

---

## 3. Blockchain & Smart Contracts

### Solidity (Ethereum/EVM)

**Security Patterns**:
- Checks-Effects-Interactions: Validate → update state → external calls
- Reentrancy guard: Use `nonReentrant` modifier
- Pull over push: Let users withdraw rather than sending to them
- Access control: Use OpenZeppelin's `Ownable` or role-based access

**Gas Optimization**:
- Use `uint256` (EVM word size) over smaller types
- Pack storage variables (multiple values in one 32-byte slot)
- Use `calldata` instead of `memory` for read-only function parameters
- Cache storage reads in local variables
- Use events for data that doesn't need on-chain access
- Minimize storage writes (most expensive operation)

**Common Vulnerabilities**:
| Vulnerability | Description | Mitigation |
|---|---|---|
| Reentrancy | External call re-enters contract | CEI pattern, ReentrancyGuard |
| Integer overflow | Arithmetic overflow | Solidity 0.8+ (built-in checks) |
| Front-running | Transaction ordering manipulation | Commit-reveal, batch auctions |
| Oracle manipulation | Price feed attacks | TWAP, multiple oracles |
| Flash loan attacks | Uncollateralized borrowing exploits | Delay mechanisms, TWAP |
| Access control | Missing permission checks | Role-based access, modifiers |

---

## 4. Embedded Systems

### Embedded Development Principles

- **Deterministic behavior**: No unbounded loops, no dynamic allocation in critical paths
- **Resource awareness**: Know your RAM, flash, CPU budget at all times
- **Power efficiency**: Sleep modes, clock gating, batch operations
- **Reliability**: Watchdog timers, error recovery, redundancy
- **Real-time constraints**: Meet deadlines, understand worst-case execution time

### RTOS Concepts

| Concept | Description | Consideration |
|---|---|---|
| Tasks/Threads | Independent execution units | Priority assignment, stack size |
| Scheduling | Preemptive priority-based | Priority inversion, starvation |
| Synchronization | Mutexes, semaphores, queues | Deadlock prevention |
| Interrupts | Hardware event handlers | Keep ISRs short, defer work |
| Timers | Periodic/one-shot callbacks | Timer resolution, drift |

### Hardware Interface Protocols

| Protocol | Speed | Wires | Use Case |
|---|---|---|---|
| SPI | Up to 100 MHz | 4 (MOSI, MISO, SCK, CS) | Displays, flash, sensors |
| I2C | 100-400 kHz (standard) | 2 (SDA, SCL) | Sensors, EEPROMs |
| UART | Up to 1 Mbps | 2 (TX, RX) | Debug, GPS, Bluetooth |
| CAN | Up to 1 Mbps | 2 (differential) | Automotive, industrial |
| USB | Up to 480 Mbps (HS) | 4 | PC communication |

### Embedded Best Practices

- Follow MISRA C guidelines for safety-critical code
- Use static analysis (PC-lint, Polyspace, cppcheck)
- Implement proper bootloader with firmware update capability
- Design for electromagnetic compatibility (EMC) in software
- Test with hardware-in-the-loop (HIL) simulation
- Document all hardware register accesses and timing constraints
- Use DMA for high-throughput data transfers
- Implement proper power management state machines

---

## 5. Game Development

### Game Architecture Patterns

| Pattern | Description | Use Case |
|---|---|---|
| Game Loop | Fixed timestep update + render | Core engine structure |
| ECS (Entity Component System) | Data-oriented design | Performance, flexibility |
| State Machine | Game states (menu, play, pause) | Game flow management |
| Observer/Event | Decouple game systems | UI updates, achievements |
| Object Pool | Reuse allocated objects | Bullets, particles, enemies |
| Spatial Partitioning | Efficient spatial queries | Collision, rendering |

### ECS Architecture

```
Entity: Just an ID (uint32/uint64)
Component: Pure data (Position, Velocity, Health, Sprite)
System: Logic that operates on entities with specific components

// Example systems:
MovementSystem: queries entities with (Position, Velocity) → updates Position
RenderSystem: queries entities with (Position, Sprite) → draws to screen
CollisionSystem: queries entities with (Position, Collider) → detects overlaps
```

### Performance Considerations

- **Frame budget**: 16.67ms for 60 FPS, 8.33ms for 120 FPS
- **Memory layout**: Data-oriented design, cache-friendly access patterns
- **Rendering**: Batch draw calls, frustum culling, LOD (Level of Detail)
- **Physics**: Fixed timestep, spatial partitioning, sleeping bodies
- **Networking**: Client-side prediction, server reconciliation, interpolation
- **Asset loading**: Async loading, streaming, texture atlases

### Game Engine Selection

| Engine | Language | Best For |
|---|---|---|
| Unity | C# | Cross-platform, mobile, indie |
| Unreal Engine | C++/Blueprints | AAA, high-fidelity graphics |
| Godot | GDScript/C# | Open-source, 2D, indie |
| Bevy | Rust | ECS-native, modern, performant |
| Custom | C/C++/Rust | Full control, specific needs |
