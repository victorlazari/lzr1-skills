# Advanced Retrieval-Augmented Generation (RAG) Engineering

This reference covers production-grade Retrieval-Augmented Generation (RAG) architectures, GraphRAG, Agentic RAG, and multi-modal grounding strategies compiled from recent research [1] [2].

---

## 1. The Evolution of RAG Architectures

RAG has transitioned from simple vector-search chunk retrieval (Naive RAG) to highly dynamic, agentic, and structured knowledge graphs (Advanced & Agentic RAG).

```
[Naive RAG]    ──> Query ──> Dense Vector Search ──> Chunk Retrieval ──> Generation
[Advanced RAG] ──> Query ──> Query Expansion ──> Dense/Sparse Retrieval ──> Reranking ──> Generation
[Agentic RAG]  ──> Query ──> Agentic Planning ──> Tool Execution ──> Reflection ──> Revision ──> Generation
```

| Generation | Core Characteristics | Retrieval Methods | Primary Strengths |
| :--- | :--- | :--- | :--- |
| **Naive RAG** | Single-turn, flat text chunking. | Dense vector similarity. | Simple to implement, low latency. |
| **Advanced RAG** | Pre-retrieval (query rewrite) & post-retrieval (reranking). | Hybrid (Dense + Sparse BM25) [3]. | Higher precision, fewer irrelevant chunks. |
| **GraphRAG** | Grounded in structured Knowledge Graphs (KG). | Entity/Relationship traversal [4]. | Outstanding on global, multi-hop, relational QA. |
| **Agentic RAG** | Multi-turn loops, tool-use, self-reflection. | Dynamic, iterative tool calling [5]. | High flexibility, handles ambiguous/complex tasks. |

---

## 2. Advanced Retrieval & Indexing Strategies

### A. Hybrid Search (Dense + Sparse)
Dense vector embeddings capture semantic meaning, but often fail on exact keyword matches (part numbers, product IDs, names). 
* **Sparse Search (BM25):** Performs exact keyword matching.
* **Dense Search:** Performs semantic concept matching.
* **Reciprocal Rank Fusion (RRF):** Combines the ranks of dense and sparse retrieval to produce a unified, optimal set of retrieved documents [3].

### B. GraphRAG & NodeRAG
Traditional RAG breaks documents into flat chunks, losing global relationships. GraphRAG constructs a knowledge graph of entities and relations.
* **NodeRAG (Heterogeneous Nodes):** Unifies entities, text chunks, events, and summaries as heterogeneous nodes in a single graph [6]. This allows seamless traversal and reduces indexing time compared to static graphs.
* **CatRAG (Context-Aware Traversal):** Implements dynamic, query-aware edge weighting during graph traversal to prevent semantic drift across multi-hop paths [7].

### C. LatentRAG & Latent Abstraction
Instead of passing full text chunks to the LLM (which consumes token budget and introduces noise), **LatentRAG** and **Latent Abstraction** retrieve and compress information directly in the continuous latent space of the model, reducing latency by up to 90% while maintaining accuracy [8] [9].

---

## 3. Agentic RAG Design Patterns

Agentic RAG integrates autonomous AI agents into the retrieval pipeline, turning retrieval into a dynamic tool-calling process.

### A. Hierarchical Retrieval Interfaces (A-RAG)
Provide the agent with a suite of retrieval tools of varying granularities (e.g., `keyword_search`, `semantic_search`, `read_chunk_range`) [10]. The agent dynamically chooses the most cost-efficient tool based on the complexity of the query.

### B. Failure-Aware Repair (Doctor-RAG)
Agentic loops can get stuck in loops or retrieve incorrect documents. **Doctor-RAG** implements a diagnostic layer that detects broken retrieval trajectories and applies targeted repairs to recover coherent reasoning [11].

### C. Cognitive-Inspired Memory (ComoRAG)
Mimics human cognitive memory by structuring RAG around a dual-system setup: a fast, long-range model generates draft answers and guides retrieval, while a stateful memory workspace consolidates facts before final output [12].

---

## 4. Input Processing & Multimodal Grounding

### A. Vision-Guided Chunking
Instead of parsing PDFs into raw, unstructured plain text (which destroys tables, structures, and charts), use Large Multimodal Models (LMMs) to perform visual page chunking [13]. This preserves multi-page tables and embedded figures in their correct spatial layout.

### B. Region-Level Retrieval (RegionRAG)
For visual document understanding, **RegionRAG** shifts from document-level image retrieval to region-level visual cropping [14]. This uses up to 71% fewer visual tokens while significantly improving QA accuracy.

---

## 5. RAG Evaluation Metrics

To build reliable RAG systems, evaluate them quantitatively across three core dimensions (the RAG Triad):

1. **Context Relevance:** Is the retrieved context relevant to the user query? (Evaluates the Retriever).
2. **Groundedness (Faithfulness):** Is the generated response fully supported *only* by the retrieved context? (Evaluates Hallucination).
3. **Answer Relevance:** Does the generated response directly answer the user's query? (Evaluates the Generator).

---

## 6. References

* [1] Singh, A., et al. (2025). Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG. *arXiv preprint arXiv:2501.09136*.
* [2] Schulhoff, S., et al. (2026). SoK: Agentic Retrieval-Augmented Generation (RAG). *arXiv preprint arXiv:2603.07379*.
* [3] Scientific AI Lab. (2026). SAGE: Benchmarking and Improving Retrieval for Deep Research Agents. *arXiv preprint arXiv:2602.05975*.
* [4] UW Benchmark Team. (2026). WildGraphBench: Benchmarking GraphRAG with Wild-Source Corpora. *arXiv preprint arXiv:2602.02053*.
* [5] Li, Y., et al. (2025). Towards Agentic RAG with Deep Reasoning. *arXiv preprint arXiv:2507.09477*.
* [6] Peking University. (2025). NodeRAG: Structuring Graph-based RAG with Heterogeneous Nodes. *arXiv preprint arXiv:2504.11544*.
* [7] CatRAG Team. (2026). Breaking the Static Graph: Context-Aware Traversal for Robust RAG. *arXiv preprint arXiv:2602.01965*.
* [8] Wang, J., et al. (2026). LatentRAG: Latent Reasoning and Retrieval for Efficient Agentic RAG. *arXiv preprint arXiv:2605.06285*.
* [9] Liu, H., et al. (2026). Latent Abstraction for Retrieval-Augmented Generation. *arXiv preprint arXiv:2604.17866*.
* [10] Zhang, L., et al. (2026). A-RAG: Scaling Agentic RAG via Hierarchical Retrieval Interfaces. *arXiv preprint arXiv:2602.03442*.
* [11] Chen, Y., et al. (2026). Doctor-RAG: Failure-Aware Repair for Agentic RAG. *arXiv preprint arXiv:2604.00865*.
* [12] ComoRAG Team. (2025). ComoRAG: Cognitive-Inspired Memory-Organized RAG. *arXiv preprint arXiv:2508.10419*.
* [13] Purdue LMM Group. (2025). Vision-Guided Chunking Is All You Need. *arXiv preprint arXiv:2506.16035*.
* [14] Cornell Multimodal AI Lab. (2025). RegionRAG: Region-level RAG for Visual Document Understanding. *arXiv preprint arXiv:2510.27261*.
