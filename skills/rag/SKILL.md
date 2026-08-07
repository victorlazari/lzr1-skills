---
name: rag
description: "Expert in Retrieval-Augmented Generation (RAG) architecture, including Adaptive RAG, agentic workflows, document chunking, embeddings, vector databases, and similarity search."
---

# Retrieval-Augmented Generation (RAG) Specialist

## Scope and Triggers

Use this skill when you need to:
- Design, implement, or optimize Retrieval-Augmented Generation (RAG) pipelines, including modern architectures like Adaptive RAG and agentic workflows.
- Configure vector databases (e.g., FAISS, Pinecone, Weaviate, Milvus) and indexing strategies.
- Select and fine-tune embedding models for semantic search.
- Implement document loading, preprocessing, and chunking strategies (e.g., semantic chunking, sliding window).
- Perform similarity search and hybrid retrieval (combining dense and sparse retrieval like BM25 with Reciprocal Rank Fusion).
- Troubleshoot RAG failures such as hallucinations, context overflow, or retrieval of irrelevant context.
- Conduct security audits for RAG systems, including data privacy, access control, and prompt injection mitigation.
- Set up continuous data ingestion pipelines or automated updates.

**Cross-Skill Routing:**
- `automation-and-scheduling`: Route when the task requires setting up continuous data ingestion pipelines or automated updates.
- `security-review`: Route when the task requires a deep security audit of the RAG system, beyond basic access control and prompt injection mitigation.

## Preconditions

Before modifying or deploying a RAG pipeline:
1. Identify the target environment, existing vector databases, and embedding models.
2. Verify permissions for data ingestion and vector database access.
3. Determine the specific RAG architecture required (e.g., Modular RAG, Adaptive RAG, Graph RAG).

## Source Freshness

RAG technologies evolve rapidly. For volatile facts, supported versions, and best practices, consult the `references/source-map.md` to find the authoritative source (e.g., AWS, IBM, Pinecone, Databricks) and verify the latest documentation before making architectural decisions.

## Workflow

1. **Architecture Design**: Analyze the user's RAG requirements and identify the appropriate architecture (e.g., Modular RAG, Adaptive RAG, Graph RAG, Agentic Workflows).
2. **Source Verification**: Consult `references/source-map.md` for the latest best practices and authoritative guidance on the chosen architecture.
3. **Data Strategy**: Design the data ingestion, chunking, embedding, and vector database strategy. Include continuous data updates if required.
4. **Validation**: Validate the proposed RAG configuration using `scripts/validate-rag-config.sh`.
5. **Implementation**: Implement the retrieval and generation components, incorporating hybrid search (e.g., BM25 + dense embeddings) and reranking as needed.
6. **Evaluation**: Evaluate the pipeline using deterministic validation metrics (e.g., RAGAS metrics) and address any identified issues (e.g., hallucinations, latency).
7. **Stop Condition**: Stop when the RAG pipeline meets the defined success criteria and output the final configuration and recommendations.

## Safety

- **Read-Only Discovery**: Always perform read-only discovery of existing RAG configurations and data sources before proposing changes.
- **Confirmation Required**: Require explicit user confirmation before deploying or modifying production RAG pipelines, or performing destructive actions on vector databases.
- **Dry Runs**: Implement dry-run capabilities for data ingestion scripts to verify chunking and embedding logic without modifying the database.

## Validation

- Validate RAG configuration schemas (YAML/JSON) using `scripts/validate-rag-config.sh` to ensure required fields (e.g., vector DB type, embedding model, chunking strategy) are present.
- Use deterministic metrics (e.g., RAGAS) to evaluate context relevance, groundedness, and answer relevance.

## Failure Handling

- If data ingestion fails, log errors and provide rollback instructions for vector database updates.
- If retrieval quality is poor, diagnose using RAGAS metrics, adjust chunking strategies, or implement hybrid search/reranking. Do not repeat the same configuration if it fails.

## Output Contract

The final output must include:
- A clear, structured RAG pipeline recommendation or configuration.
- Evidence of validation (e.g., RAGAS metric scores or `validate-rag-config.sh` output).
- Confidence levels for the recommendations.
- Actionable next steps for deployment or further optimization.

## Resources

- [Complete Reference Guide](./references/complete-reference.md): Detailed technical reference on RAG architectures, chunking, embeddings, and hybrid search.
- [Source Map](./references/source-map.md): Maps RAG dimensions to authoritative sources for verifying volatile facts.
- [Validate RAG Config Script](./scripts/validate-rag-config.sh): Deterministic script to validate RAG configuration schemas.

## Orchestration

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple document sources to ingest | Ingestion Agent | Parallel document loading, cleaning, and chunking |
| Multiple embedding models to evaluate | Embedding Evaluator | Parallel generation and evaluation of embeddings |
| Bulk query troubleshooting | Diagnostics Agent | Parallel issue investigation and query reformulation |

### Spawning Rules
- Spawn when 3+ independent items need the same operation.
- Each sub-agent receives: context, specific target, success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.

### Adversarial Verification Panel
For each significant RAG pipeline recommendation produced by parallel sub-agents:
1. Spawn 3 independent Refuter Agents per finding to find the strongest argument against it.
2. A finding is confirmed only if ≥2 refuters fail to refute it.
3. A finding is discarded if ≥2 refuters succeed.

### Cross-System Consistency Validator
Run one Consistency Validator Agent with all parallel outputs to flag logical contradictions and missing prerequisites before synthesis.

### Synthesis Agent
The synthesis step actively resolves contradictions, re-orders based on prerequisites, calibrates confidence, and notes analysis gaps.
