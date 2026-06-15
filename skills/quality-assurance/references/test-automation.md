# Test Automation

## Table of Contents
1. Automation Strategy
2. Framework Design
3. CI/CD Integration
4. API Testing
5. UI Testing

---

## 1. Automation Strategy

### What to Automate

| Automate | Don't Automate |
|---|---|
| Regression tests | Exploratory testing |
| Smoke tests | One-time tests |
| Data-driven tests | Tests requiring human judgment |
| API contract tests | Usability testing |
| Performance benchmarks | Tests for unstable features |
| Security scans | Ad-hoc investigation |

### Automation ROI

```
ROI = (Manual cost - Automation cost) / Automation cost

Manual cost = Time per run × Runs per year × Hourly rate
Automation cost = Development time + Maintenance time (annual)

Example:
  Manual: 4 hours × 52 weeks × $75/hr = $15,600/year
  Automation: 40 hours development + 20 hours/year maintenance = $4,500
  ROI: ($15,600 - $4,500) / $4,500 = 247%
  Breakeven: ~4 months
```

---

## 2. Framework Design

### Framework Architecture

```
test-framework/
├── config/
│   ├── environments.json
│   └── test-data/
├── src/
│   ├── pages/          (Page Object Model)
│   ├── api/            (API clients)
│   ├── utils/          (Helpers, assertions)
│   └── fixtures/       (Test setup/teardown)
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── performance/
├── reports/
└── ci/
    └── pipeline.yml
```

### Framework Selection

| Framework | Language | Best For | Speed |
|---|---|---|---|
| Playwright | JS/TS/Python/C# | Modern web E2E | Fast |
| Cypress | JavaScript | Frontend E2E | Fast |
| Selenium | Multi-language | Legacy, cross-browser | Medium |
| Jest | JavaScript | Unit + integration | Very fast |
| Pytest | Python | All levels | Fast |
| JUnit/TestNG | Java | Enterprise, unit | Fast |
| k6 | JavaScript | Performance/load | Fast |
| Postman/Newman | JavaScript | API testing | Fast |
| REST Assured | Java | API testing | Fast |

### Page Object Model

```typescript
// pages/login.page.ts
export class LoginPage {
  private page: Page;
  
  // Locators
  private emailInput = '[data-testid="email"]';
  private passwordInput = '[data-testid="password"]';
  private submitButton = '[data-testid="login-submit"]';
  
  constructor(page: Page) {
    this.page = page;
  }
  
  async login(email: string, password: string) {
    await this.page.fill(this.emailInput, email);
    await this.page.fill(this.passwordInput, password);
    await this.page.click(this.submitButton);
  }
  
  async isLoggedIn(): Promise<boolean> {
    return this.page.isVisible('[data-testid="dashboard"]');
  }
}
```

---

## 3. CI/CD Integration

### Pipeline Stages

```yaml
stages:
  - lint          # Static analysis
  - unit-test     # Unit tests (fast, parallel)
  - build         # Build application
  - integration   # Integration tests
  - deploy-staging # Deploy to staging
  - e2e           # End-to-end tests
  - performance   # Performance benchmarks
  - deploy-prod   # Deploy to production
  - smoke         # Production smoke tests
```

### Test Execution Strategy

| Stage | Tests | Trigger | Duration |
|---|---|---|---|
| Pre-commit | Lint, unit (affected) | Git hook | <30 seconds |
| PR/MR | Unit, integration | PR creation | <5 minutes |
| Merge to main | Full unit, integration, API | Merge | <10 minutes |
| Staging deploy | E2E, regression | Auto-deploy | <30 minutes |
| Pre-production | Full regression, performance | Manual gate | <1 hour |
| Post-production | Smoke tests | Auto-deploy | <5 minutes |

### Flaky Test Management

| Strategy | Description |
|---|---|
| Quarantine | Move flaky tests to separate suite |
| Retry | Auto-retry failed tests (max 2x) |
| Track | Dashboard showing flaky test trends |
| Fix SLA | Flaky tests must be fixed within 1 sprint |
| Root cause | Categorize: timing, data, environment, race condition |

---

## 4. API Testing

### API Test Categories

| Category | What to Test | Example |
|---|---|---|
| Contract | Request/response schema | JSON schema validation |
| Functional | Business logic correctness | CRUD operations work |
| Error handling | Proper error responses | 400, 401, 403, 404, 500 |
| Authentication | Auth mechanisms work | Token validation, expiry |
| Authorization | Permissions enforced | Role-based access |
| Performance | Response times, throughput | <200ms p95 |
| Integration | External service interactions | Third-party API calls |

### API Test Structure

```
Given: [Precondition/Setup]
When: [API call with specific parameters]
Then: [Expected response status, body, headers]

Example:
Given: User exists with email "test@example.com"
When: POST /api/auth/login with valid credentials
Then: 200 OK, response contains access_token and refresh_token
```

---

## 5. UI Testing

### UI Test Best Practices

| Practice | Description |
|---|---|
| Use data-testid | Stable selectors, not CSS/XPath |
| Wait for elements | Explicit waits, not sleep |
| Isolate tests | Each test independent, own data |
| Test user flows | Not individual elements |
| Visual regression | Screenshot comparison for UI changes |
| Accessibility | Include a11y checks in UI tests |
| Mobile viewports | Test responsive breakpoints |

### Visual Regression Testing

| Tool | Approach | Best For |
|---|---|---|
| Percy (BrowserStack) | Cloud-based screenshot comparison | Cross-browser |
| Chromatic | Storybook integration | Component libraries |
| Playwright screenshots | Built-in comparison | Simple visual checks |
| Applitools | AI-powered visual testing | Complex UIs |
| BackstopJS | Open-source, config-based | Budget-friendly |
