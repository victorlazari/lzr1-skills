# Product Growth

## Table of Contents
1. Growth Frameworks
2. Metrics and KPIs
3. Experimentation
4. Retention and Engagement
5. Monetization

---

## 1. Growth Frameworks

### Pirate Metrics (AARRR)

| Stage | Metric | Example |
|---|---|---|
| Acquisition | How users find you | Website visits, signups |
| Activation | First value moment | Completed onboarding, first action |
| Retention | Users coming back | DAU/MAU, D7/D30 retention |
| Revenue | Users paying | Conversion rate, ARPU, LTV |
| Referral | Users inviting others | Viral coefficient, referral rate |

### Growth Loops

```
Input → Action → Output → Reinvested as Input

Examples:
- Content loop: Create content → SEO traffic → Users create content → More SEO
- Viral loop: User invites → New user joins → New user invites → More users
- Paid loop: Revenue → Ad spend → New users → Revenue → More ad spend
- Data loop: Users → Data → Better product → More users
```

### North Star Metric

| Company Type | North Star | Why |
|---|---|---|
| Marketplace | Transactions completed | Core value exchange |
| SaaS | Weekly active users doing [core action] | Engagement = retention |
| E-commerce | Purchases per buyer per month | Revenue driver |
| Media | Time spent consuming content | Ad revenue driver |
| Fintech | Assets under management | Revenue + trust |

---

## 2. Metrics and KPIs

### SaaS Metrics

| Metric | Formula | Healthy Benchmark |
|---|---|---|
| MRR | Sum of monthly recurring revenue | Growing month-over-month |
| ARR | MRR × 12 | Growing year-over-year |
| Churn rate | Lost customers / Total customers | <5% monthly (SMB), <1% (Enterprise) |
| Net revenue retention | (Start MRR + expansion - contraction - churn) / Start MRR | >100% (ideally >120%) |
| CAC | Total acquisition cost / New customers | Payback <12 months |
| LTV | ARPU × Gross margin / Churn rate | LTV:CAC > 3:1 |
| CAC payback | CAC / (ARPU × Gross margin) | <12 months |
| Quick ratio | (New MRR + Expansion MRR) / (Contraction + Churn MRR) | >4 |

### Engagement Metrics

| Metric | Description | Calculation |
|---|---|---|
| DAU/MAU | Stickiness ratio | Daily active / Monthly active |
| L7/L30 | Weekly engagement intensity | Days active in 7/30 days |
| Session frequency | How often users return | Sessions per user per week |
| Session duration | Time spent per visit | Average session length |
| Feature adoption | % using specific feature | Users of feature / Total users |
| Activation rate | % reaching "aha moment" | Activated / Signed up |

### Retention Curves

| Shape | Interpretation | Action |
|---|---|---|
| Flattening | Product-market fit exists | Optimize, grow |
| Declining to zero | No PMF | Pivot or improve core value |
| Smile curve (uptick) | Strong habit formation | Accelerate growth |
| Step function | Event-driven usage | Optimize for events |

---

## 3. Experimentation

### Experiment Process

```
1. Observe: Notice a metric or behavior
2. Hypothesize: "If we [change], then [metric] will [improve] because [reason]"
3. Design: Control vs treatment, sample size, duration
4. Execute: Run the experiment
5. Analyze: Statistical significance + practical significance
6. Decide: Ship, iterate, or kill
7. Document: Record learnings for the team
```

### Experiment Prioritization (ICE)

| Factor | Score | Description |
|---|---|---|
| Impact | 1-10 | How much will this move the metric? |
| Confidence | 1-10 | How sure are we it will work? |
| Ease | 1-10 | How easy is it to implement? |
| ICE Score | I × C × E | Higher = higher priority |

### Common Growth Experiments

| Area | Experiment Type | Example |
|---|---|---|
| Onboarding | Reduce friction | Remove optional steps |
| Activation | Guide to value | Interactive tutorial |
| Retention | Re-engagement | Email/push after inactivity |
| Monetization | Pricing | Annual vs monthly emphasis |
| Referral | Incentive | Two-sided referral reward |
| Conversion | Social proof | Show user count, testimonials |

---

## 4. Retention and Engagement

### Retention Strategies by Stage

| Stage | Strategy | Tactic |
|---|---|---|
| Day 0-1 | Activation | Streamlined onboarding, quick win |
| Day 1-7 | Habit formation | Daily triggers, streaks, notifications |
| Day 7-30 | Value deepening | Feature discovery, use cases |
| Day 30+ | Lock-in | Data, integrations, community |
| At-risk | Re-engagement | Win-back emails, incentives |

### Engagement Loops

```
Trigger → Action → Variable Reward → Investment

Example (Slack):
Trigger: Notification of new message
Action: Open app, read message
Reward: Information, social connection (variable)
Investment: Reply (creates trigger for others)
```

### Cohort Analysis

```sql
-- Monthly retention cohort
SELECT
    cohort_month,
    months_since_signup,
    COUNT(DISTINCT user_id) AS active_users,
    COUNT(DISTINCT user_id) * 100.0 / 
        FIRST_VALUE(COUNT(DISTINCT user_id)) OVER (
            PARTITION BY cohort_month ORDER BY months_since_signup
        ) AS retention_rate
FROM user_activity_cohorts
GROUP BY cohort_month, months_since_signup
ORDER BY cohort_month, months_since_signup;
```

---

## 5. Monetization

### Pricing Models

| Model | Description | Best For |
|---|---|---|
| Freemium | Free tier + paid upgrades | High-volume, self-serve |
| Free trial | Full access for limited time | Complex products |
| Usage-based | Pay per unit consumed | APIs, infrastructure |
| Per-seat | Pay per user | Collaboration tools |
| Tiered | Feature-differentiated plans | Diverse customer segments |
| Flat rate | Single price for everything | Simple products |
| Hybrid | Combination of above | Enterprise SaaS |

### Pricing Strategy

| Strategy | Description | When to Use |
|---|---|---|
| Value-based | Price based on customer value | Strong differentiation |
| Competitor-based | Price relative to alternatives | Commodity markets |
| Cost-plus | Cost + margin | Low differentiation |
| Penetration | Low price to gain share | New market entry |
| Skimming | High price, lower over time | Innovation, early adopters |

### Conversion Optimization

| Lever | Tactic | Metric |
|---|---|---|
| Reduce friction | Fewer steps to purchase | Checkout completion rate |
| Social proof | Testimonials, logos, counts | Trust indicators |
| Urgency | Limited time offers | Time-bound conversion |
| Value demonstration | ROI calculator, case studies | Perceived value |
| Risk reduction | Free trial, money-back guarantee | Trial-to-paid rate |
| Pricing clarity | Simple, comparable plans | Plan selection rate |
