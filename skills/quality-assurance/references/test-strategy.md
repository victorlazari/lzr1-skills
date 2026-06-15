# Test Strategy

## Table of Contents
1. Test Planning
2. Test Design Techniques
3. Testing Pyramid
4. Defect Management
5. QA Metrics

---

## 1. Test Planning

### Test Plan Components

| Component | Description |
|---|---|
| Scope | What's being tested and what's excluded |
| Objectives | Quality goals and exit criteria |
| Approach | Testing types, levels, and techniques |
| Resources | People, tools, environments |
| Schedule | Timeline, milestones, dependencies |
| Risks | Testing risks and mitigations |
| Deliverables | Reports, artifacts, sign-offs |
| Entry/Exit criteria | When to start and when to stop |

### Test Types

| Type | Purpose | When | Who |
|---|---|---|---|
| Unit | Individual functions/methods | During development | Developers |
| Integration | Component interactions | After unit tests | Dev + QA |
| API | Service contracts, endpoints | Continuous | QA + Dev |
| E2E | Full user workflows | Before release | QA |
| Regression | Existing functionality still works | Every release | Automated |
| Smoke | Critical paths work | After deployment | Automated |
| Exploratory | Find unexpected issues | Throughout | QA |
| Acceptance | Business requirements met | Before release | QA + Product |
| Security | Vulnerabilities, OWASP | Periodic + release | Security + QA |
| Accessibility | WCAG compliance | Design + release | QA + Design |

---

## 2. Test Design Techniques

### Black-Box Techniques

| Technique | Description | Best For |
|---|---|---|
| Equivalence partitioning | Divide inputs into valid/invalid groups | Reducing test cases |
| Boundary value analysis | Test at boundaries of partitions | Numeric inputs, ranges |
| Decision tables | All combinations of conditions | Complex business rules |
| State transition | Test state changes | Workflows, status changes |
| Use case testing | Test complete user scenarios | End-to-end flows |
| Error guessing | Based on experience and intuition | Experienced testers |

### Test Case Template

```
Test Case ID: TC-001
Title: [Clear, descriptive title]
Priority: High/Medium/Low
Preconditions: [Setup required before test]
Test Data: [Specific data needed]

Steps:
1. [Action]
2. [Action]
3. [Action]

Expected Result: [What should happen]
Actual Result: [What actually happened]
Status: Pass/Fail/Blocked
```

---

## 3. Testing Pyramid

### Test Pyramid Layers

| Layer | % of Tests | Speed | Cost | Confidence |
|---|---|---|---|---|
| Unit tests | 70% | Very fast (ms) | Low | Low (isolated) |
| Integration tests | 20% | Fast (seconds) | Medium | Medium |
| E2E/UI tests | 10% | Slow (minutes) | High | High (realistic) |

### Anti-Patterns

| Anti-Pattern | Description | Fix |
|---|---|---|
| Ice cream cone | Too many E2E, few unit tests | Invert the pyramid |
| No tests | Relying on manual testing only | Start with unit tests |
| Flaky tests | Tests that randomly fail | Fix or remove, don't ignore |
| Slow pipeline | Tests take too long | Parallelize, optimize, pyramid |
| Test duplication | Same thing tested at multiple levels | Test at the right level |

---

## 4. Defect Management

### Bug Report Template

```
Title: [Clear, concise description]
Severity: Critical/High/Medium/Low
Priority: P1/P2/P3/P4
Environment: [OS, browser, version, environment]
Steps to Reproduce:
1. [Step]
2. [Step]
3. [Step]
Expected: [What should happen]
Actual: [What actually happens]
Attachments: [Screenshots, logs, video]
```

### Severity Definitions

| Severity | Definition | Example | SLA |
|---|---|---|---|
| Critical | System down, data loss, security breach | Payment processing broken | Fix immediately |
| High | Major feature broken, no workaround | Login fails for subset of users | Fix within 24 hours |
| Medium | Feature broken, workaround exists | Export button broken, can use API | Fix within sprint |
| Low | Minor issue, cosmetic | Typo, alignment issue | Fix when convenient |

### Defect Lifecycle

```
New → Triaged → Assigned → In Progress → Fixed → Verified → Closed
                    ↓                         ↓
               Won't Fix                  Reopened
                    ↓
                Deferred
```

---

## 5. QA Metrics

### Key QA Metrics

| Metric | Formula | Benchmark |
|---|---|---|
| Defect density | Defects / KLOC or per feature | Decreasing over time |
| Defect escape rate | Production bugs / Total bugs found | <10% |
| Test coverage | Lines/branches covered / Total | >80% (unit) |
| Test pass rate | Passed tests / Total tests | >95% |
| Automation rate | Automated tests / Total test cases | >70% |
| Mean time to detect | Time from introduction to discovery | Decreasing |
| Regression rate | Regressions / Total bugs | <5% |
| Flaky test rate | Flaky tests / Total automated tests | <2% |

### Quality Gates

| Gate | Criteria | When |
|---|---|---|
| Code review | All code reviewed, no critical findings | Before merge |
| Unit tests | >80% coverage, all passing | Before merge |
| Integration tests | All passing, no new failures | Before deploy to staging |
| Regression | Full suite passing | Before release |
| Performance | No degradation >10% | Before release |
| Security | No critical/high vulnerabilities | Before release |
| Acceptance | Product owner sign-off | Before release |
