# SEO (Search Engine Optimization)

## Table of Contents
1. Technical SEO
2. On-Page SEO
3. Content SEO
4. Link Building
5. Local SEO
6. SEO Tools and Measurement

---

## 1. Technical SEO

### Technical SEO Checklist

| Category | Check | Priority |
|---|---|---|
| Crawlability | robots.txt configured correctly | Critical |
| Crawlability | XML sitemap submitted | Critical |
| Crawlability | No orphan pages | High |
| Indexability | Canonical tags set correctly | Critical |
| Indexability | No unintentional noindex | Critical |
| Performance | Core Web Vitals passing | High |
| Performance | Page load <3 seconds | High |
| Mobile | Mobile-friendly (responsive) | Critical |
| Security | HTTPS everywhere | Critical |
| Structure | Clean URL structure | High |
| Structure | Proper internal linking | High |
| International | hreflang tags (if multilingual) | Medium |

### Core Web Vitals

| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | ≤2.5s | 2.5-4.0s | >4.0s |
| INP (Interaction to Next Paint) | ≤200ms | 200-500ms | >500ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | 0.1-0.25 | >0.25 |

### Site Architecture

```
Homepage
├── Category 1 (pillar page)
│   ├── Subtopic 1a (cluster content)
│   ├── Subtopic 1b (cluster content)
│   └── Subtopic 1c (cluster content)
├── Category 2 (pillar page)
│   ├── Subtopic 2a
│   └── Subtopic 2b
└── Category 3 (pillar page)
    └── ...

Rule: Every page should be reachable within 3 clicks from homepage.
```

---

## 2. On-Page SEO

### On-Page Elements

| Element | Best Practice | Character Limit |
|---|---|---|
| Title tag | Primary keyword + brand, compelling | 50-60 characters |
| Meta description | Summarize page, include CTA | 150-160 characters |
| H1 | One per page, includes primary keyword | Natural length |
| H2-H6 | Logical hierarchy, include variations | Natural length |
| URL | Short, descriptive, includes keyword | 3-5 words |
| Image alt text | Descriptive, includes keyword naturally | 125 characters |
| Internal links | Link to related content with descriptive anchor | Natural |

### Content Optimization

| Factor | Guideline |
|---|---|
| Keyword placement | Title, H1, first 100 words, throughout naturally |
| Content length | Match or exceed top-ranking competitors |
| Search intent | Match the intent (informational, transactional, navigational) |
| Freshness | Update regularly, add new information |
| E-E-A-T | Experience, Expertise, Authoritativeness, Trustworthiness |
| Structured data | Schema markup for rich snippets |
| User engagement | Reduce bounce rate, increase time on page |

### Schema Markup Types

| Type | Use Case | Rich Result |
|---|---|---|
| Article | Blog posts, news | Article snippet |
| Product | E-commerce products | Price, availability, reviews |
| FAQ | Frequently asked questions | Expandable FAQ |
| HowTo | Step-by-step guides | Steps in SERP |
| Organization | Company info | Knowledge panel |
| BreadcrumbList | Navigation path | Breadcrumb trail |
| Review | Product/service reviews | Star ratings |

---

## 3. Content SEO

### Topic Cluster Strategy

```
Pillar Page (broad topic, 3000+ words)
├── Cluster 1 (specific subtopic, 1500+ words)
├── Cluster 2 (specific subtopic, 1500+ words)
├── Cluster 3 (specific subtopic, 1500+ words)
└── Cluster 4 (specific subtopic, 1500+ words)

All cluster pages link to pillar page and to each other.
Pillar page links to all cluster pages.
```

### Keyword Research Process

1. **Seed keywords**: Brainstorm core topics
2. **Expand**: Use tools to find related terms, questions, long-tail
3. **Analyze**: Check volume, difficulty, intent
4. **Prioritize**: Balance volume, difficulty, and business relevance
5. **Map**: Assign keywords to pages (one primary per page)
6. **Track**: Monitor rankings over time

### Search Intent Types

| Intent | Description | Content Type | Example |
|---|---|---|---|
| Informational | Learn something | Blog, guide, video | "what is SEO" |
| Navigational | Find specific site | Homepage, landing page | "Ahrefs login" |
| Commercial | Research before buying | Comparison, review | "best SEO tools 2025" |
| Transactional | Ready to buy/act | Product page, pricing | "buy Ahrefs subscription" |

---

## 4. Link Building

### Link Building Strategies

| Strategy | Difficulty | Scalability | Quality |
|---|---|---|---|
| Content-driven (10x content) | High | Medium | High |
| Digital PR | High | Medium | Very High |
| Guest posting | Medium | High | Medium |
| Broken link building | Medium | Medium | Medium |
| Resource page outreach | Medium | Medium | Medium-High |
| HARO/journalist queries | Medium | Low | High |
| Partnerships/co-marketing | Low | Low | High |
| Unlinked brand mentions | Low | Low | High |

### Link Quality Factors

| Factor | High Quality | Low Quality |
|---|---|---|
| Domain authority | DA 50+ | DA <20 |
| Relevance | Same industry/topic | Unrelated site |
| Traffic | Site gets real traffic | No organic traffic |
| Placement | In-content, editorial | Footer, sidebar, directory |
| Anchor text | Natural, varied | Exact-match, spammy |
| Link type | Dofollow, editorial | Nofollow, paid |

---

## 5. Local SEO

### Google Business Profile Optimization

| Element | Best Practice |
|---|---|
| Business name | Exact legal name (no keyword stuffing) |
| Categories | Primary + secondary categories |
| Description | Keyword-rich, compelling |
| Photos | Regular uploads, high quality |
| Reviews | Actively request and respond |
| Posts | Weekly updates, offers, events |
| Hours | Accurate, updated for holidays |
| Q&A | Pre-populate common questions |

### Local Ranking Factors

| Factor | Weight | Optimization |
|---|---|---|
| Google Business Profile | High | Complete, active, optimized |
| Reviews | High | Quantity, quality, recency |
| On-page (local keywords) | High | City + service in title, content |
| Citations (NAP consistency) | Medium | Consistent name, address, phone |
| Links (local relevance) | Medium | Local organizations, press |
| Behavioral | Medium | Click-through rate, engagement |

---

## 6. SEO Tools and Measurement

### SEO Tool Stack

| Tool | Primary Use | Type |
|---|---|---|
| Google Search Console | Performance data, indexing | Free |
| Google Analytics | Traffic, behavior, conversions | Free |
| Ahrefs | Backlinks, keywords, competitor | Paid |
| Semrush | All-in-one SEO suite | Paid |
| Screaming Frog | Technical SEO crawling | Freemium |
| Surfer SEO | Content optimization | Paid |
| Clearscope | Content optimization | Paid |

### SEO KPIs

| Metric | Description | Target |
|---|---|---|
| Organic traffic | Visits from search engines | Month-over-month growth |
| Keyword rankings | Position for target keywords | Top 3 for priority terms |
| Organic conversions | Goal completions from organic | Conversion rate >2% |
| Domain authority | Overall site authority score | Steady growth |
| Indexed pages | Pages in Google's index | All important pages |
| Core Web Vitals | Page experience metrics | All passing |
| Backlink growth | New referring domains | Steady acquisition |
