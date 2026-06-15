---
name: rag
description: "Expert in Retrieval-Augmented Generation (RAG) architecture, document chunking, embeddings, vector databases, and similarity search."
---

# Retrieval-Augmented Generation (RAG) Specialist

## When to Use

Use this skill when you need to:
- Design, implement, or optimize Retrieval-Augmented Generation (RAG) pipelines.
- Configure vector databases (e.g., FAISS, Pinecone, Weaviate, Milvus) and indexing strategies.
- Select and fine-tune embedding models for semantic search.
- Implement document loading, preprocessing, and chunking strategies (e.g., semantic chunking, sliding window).
- Perform similarity search and hybrid retrieval (combining dense and sparse retrieval).
- Troubleshoot RAG failures such as hallucinations, context overflow, or retrieval of irrelevant context.
- Conduct security audits for RAG systems, including data privacy, access control, and prompt injection mitigation.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple document sources to ingest | Ingestion Agent | Parallel document loading, cleaning, and chunking |
| Multiple embedding models to evaluate | Embedding Evaluator | Parallel generation and evaluation of embeddings |
| Multiple vector databases to benchmark | Vector DB Tester | Parallel indexing and search performance testing |
| Bulk query troubleshooting | Diagnostics Agent | Parallel issue investigation and query reformulation |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Architecture Design**: Determine the appropriate RAG variant (e.g., Modular RAG, Graph RAG) and components based on the use case.
2. **Data Ingestion & Preprocessing**: Load documents from various sources, clean the text, and apply suitable chunking strategies (e.g., fixed-size, semantic, overlapping).
3. **Embedding Generation**: Select an embedding model (e.g., Sentence-BERT, OpenAI embeddings) and generate dense vector representations for the chunks.
4. **Vector Database Setup**: Choose a vector database, configure indexing algorithms (e.g., HNSW, IVF-PQ), and insert the embeddings.
5. **Retrieval Optimization**: Implement similarity search metrics (e.g., cosine similarity), hybrid search (dense + sparse with RRF), and query expansion techniques.
6. **Generation Integration**: Connect the retriever with a generative model (e.g., GPT-4, BART) to synthesize context-aware responses.
7. **Evaluation & Troubleshooting**: Monitor system health, evaluate using metrics like RAGAS, and troubleshoot issues like hallucinations or high latency.
8. **Security & Governance**: Implement access controls, data encryption, and guardrails against prompt injection.

## Core Principles

- **Context Preservation**: Ensure chunking strategies maintain semantic coherence and context boundaries.
- **Retrieval Precision vs. Recall**: Balance the trade-off between finding the most relevant documents and finding all relevant documents.
- **Scalability**: Design vector indexing and retrieval mechanisms to handle large-scale corpora efficiently.
- **Security First**: Protect sensitive data through encryption, access controls, and PII redaction before embedding.
- **Continuous Evaluation**: Regularly assess retrieval and generation quality using established metrics and user feedback.

## Key References

- [Complete Reference Guide](./references/complete-reference.md)
- [Reading List](./references/reading-list.md)
