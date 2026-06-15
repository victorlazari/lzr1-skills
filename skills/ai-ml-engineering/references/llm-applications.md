# LLM Applications & AI Agents

## Table of Contents
1. Foundation Model Selection
2. RAG System Architecture
3. AI Agent Design Patterns
4. Production LLM Deployment
5. Evaluation and Testing
6. Cost Optimization

---

## 1. Foundation Model Selection

### Model Selection Criteria

Choose models based on task complexity, latency requirements, cost constraints, and capability needs:

| Model Tier | Use Case | Examples | Cost |
|---|---|---|---|
| Frontier (reasoning) | Complex analysis, architecture, research | Claude Opus, GPT-4, Gemini Ultra | Highest |
| Standard | Most tasks: coding, analysis, writing | Claude Sonnet, GPT-4o, Gemini Pro | Medium |
| Lightweight | Simple tasks, high volume, classification | Claude Haiku, GPT-4o-mini, Gemini Flash | Lowest |
| Open-source | Privacy-sensitive, on-premise, fine-tuning | Llama 3, Mistral, Qwen | Infrastructure |

### Key Decision Factors

- **Latency sensitivity**: Use smaller models for real-time interactions; batch complex tasks to larger models
- **Context window**: Match model context to input size; use RAG for knowledge beyond context
- **Multimodal needs**: Select models with vision/audio capabilities when processing non-text inputs
- **Fine-tuning requirements**: Open-source models for domain-specific fine-tuning; API models for general use
- **Compliance**: On-premise open-source for regulated industries; API models for speed-to-market

---

## 2. RAG System Architecture

### Core RAG Pipeline

```
Documents → Chunking → Embedding → Vector Store → Retrieval → Reranking → Generation
```

### Chunking Strategies

| Strategy | Best For | Chunk Size |
|---|---|---|
| Fixed-size | Homogeneous documents | 256-512 tokens |
| Semantic | Mixed content, articles | Variable (by topic) |
| Recursive | Structured documents | Hierarchical |
| Sentence-window | Q&A systems | Sentence + context |
| Document-based | Short documents | Full document |

### Retrieval Architecture

**Hybrid Search** (recommended for production):
- Combine dense retrieval (vector similarity) with sparse retrieval (BM25/keyword)
- Use reciprocal rank fusion (RRF) to merge results
- Implement reranking with cross-encoder models (e.g., Cohere Rerank, BGE Reranker)

**Advanced Retrieval Patterns**:
- **Multi-query retrieval**: Generate multiple query variants, retrieve for each, deduplicate
- **Parent-child chunking**: Index small chunks, retrieve parent documents for context
- **Hypothetical Document Embedding (HyDE)**: Generate hypothetical answer, use as query
- **Self-querying**: Let LLM generate metadata filters from natural language queries

### Vector Database Selection

| Database | Strengths | Best For |
|---|---|---|
| Pinecone | Managed, scalable, fast | Production SaaS |
| Weaviate | Hybrid search, multimodal | Complex queries |
| Qdrant | Performance, filtering | High-throughput |
| Chroma | Simple, local-first | Prototyping |
| pgvector | PostgreSQL integration | Existing Postgres |
| Milvus | Scale, GPU acceleration | Large-scale |

### RAG Quality Optimization

- **Chunk overlap**: 10-20% overlap between chunks prevents information loss at boundaries
- **Metadata enrichment**: Add source, date, section headers, entity tags to chunks
- **Query transformation**: Rewrite user queries for better retrieval (expand, decompose, rephrase)
- **Context compression**: Remove irrelevant passages from retrieved context before generation
- **Citation tracking**: Map generated claims back to source chunks for verification

---

## 3. AI Agent Design Patterns

Based on Anthropic's production agent research (Dec 2024), the most successful implementations use simple, composable patterns rather than complex frameworks.

### Architectural Distinction

- **Workflows**: LLMs and tools orchestrated through predefined code paths (predictable, consistent)
- **Agents**: LLMs dynamically direct their own processes and tool usage (flexible, autonomous)

### Five Workflow Patterns

**1. Prompt Chaining** — Sequential steps where each LLM call processes the output of the previous one.
- Use when: Task decomposes cleanly into fixed subtasks
- Example: Generate content → Translate → Format

**2. Routing** — Classify input and direct to specialized handler.
- Use when: Distinct categories need different processing
- Example: Route customer queries to refund/technical/general handlers

**3. Parallelization** — Run multiple LLM calls simultaneously.
- Sectioning: Break task into independent parallel subtasks
- Voting: Run same task multiple times for confidence
- Use when: Independent subtasks or need for diverse perspectives

**4. Orchestrator-Workers** — Central LLM breaks down tasks, delegates to workers, synthesizes results.
- Use when: Cannot predict subtasks in advance (e.g., multi-file code changes)
- Key difference from parallelization: subtasks determined dynamically

**5. Evaluator-Optimizer** — One LLM generates, another evaluates in a loop.
- Use when: Clear evaluation criteria exist and iterative refinement adds value
- Example: Translation with quality feedback loop

### Agent Design Principles

1. **Maintain simplicity** — Use the simplest architecture that solves the problem
2. **Prioritize transparency** — Show planning steps explicitly
3. **Craft the ACI carefully** — Agent-Computer Interface (tool documentation) is critical
4. **Ground truth at each step** — Use tool results and code execution to assess progress
5. **Include stopping conditions** — Maximum iterations, timeout, budget limits
6. **Sandbox extensively** — Test in isolated environments before production

### Tool Design for Agents

- Write clear, specific tool descriptions (the LLM reads these to decide when to use tools)
- Include parameter descriptions with types, constraints, and examples
- Return structured, parseable results
- Handle errors gracefully with informative messages
- Implement idempotency where possible

---

## 4. Production LLM Deployment

### Architecture Patterns

**Gateway Pattern**: Route all LLM calls through a central gateway for:
- Rate limiting and quota management
- Request/response logging
- Model fallback (primary → secondary → cached response)
- Cost tracking per user/feature
- A/B testing different models or prompts

**Caching Strategy**:
- Exact match cache for repeated queries
- Semantic cache for similar queries (embedding similarity threshold)
- Cache invalidation based on knowledge freshness requirements
- Typical cache hit rates: 20-40% for customer-facing, 60-80% for internal tools

### Reliability Patterns

- **Circuit breaker**: Stop calling failing models; switch to fallback
- **Retry with exponential backoff**: Handle transient API failures
- **Timeout management**: Set aggressive timeouts; stream for long responses
- **Graceful degradation**: Serve cached/simpler responses when primary model unavailable
- **Output validation**: Parse and validate LLM outputs before serving to users

### Guardrails

- **Input guardrails**: Content filtering, PII detection, injection detection
- **Output guardrails**: Toxicity filtering, hallucination detection, format validation
- **Structural guardrails**: Token limits, cost caps, rate limits per user
- **Monitoring guardrails**: Alert on quality degradation, cost spikes, latency increases

---

## 5. Evaluation and Testing

### LLM Evaluation Framework

| Evaluation Type | Method | When |
|---|---|---|
| Automated metrics | BLEU, ROUGE, exact match, F1 | Every prompt change |
| LLM-as-judge | Use stronger model to evaluate outputs | Weekly/release |
| Human evaluation | Domain experts rate outputs | Monthly/major changes |
| A/B testing | Compare in production with real users | Feature launches |
| Red teaming | Adversarial testing for safety | Pre-launch |

### RAG Evaluation Metrics

- **Retrieval quality**: Precision@K, Recall@K, MRR, NDCG
- **Generation quality**: Faithfulness (grounded in context), relevance, completeness
- **End-to-end**: Answer correctness, citation accuracy, user satisfaction

### Testing Strategy

1. **Unit tests**: Individual prompt templates with known inputs/outputs
2. **Integration tests**: Full pipeline with mock/real retrievers
3. **Regression tests**: Golden dataset that must pass on every change
4. **Stress tests**: High concurrency, long inputs, adversarial inputs
5. **Drift detection**: Monitor output quality distribution over time

---

## 6. Cost Optimization

### Token Optimization

- Use prompt caching (Anthropic, OpenAI) for repeated system prompts
- Compress context: summarize long documents before including
- Route simple queries to cheaper models (Haiku/GPT-4o-mini)
- Batch requests where latency permits
- Cache embeddings; avoid re-embedding unchanged documents

### Architecture Optimization

- Implement semantic caching to avoid redundant LLM calls
- Use streaming to improve perceived latency without changing cost
- Pre-compute common responses for FAQ-type queries
- Implement request deduplication for concurrent identical queries
- Monitor cost per feature/user to identify optimization opportunities
