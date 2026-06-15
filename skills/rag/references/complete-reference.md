# Comprehensive Reference Guide for Retrieval-Augmented Generation (RAG)

## 1. Introduction to RAG Architecture

Retrieval-Augmented Generation (RAG) combines the strengths of pre-trained generative models with external knowledge retrieval systems. It addresses the limitations of standalone Large Language Models (LLMs), such as hallucinations and outdated knowledge, by dynamically accessing external data at inference time.

### 1.1 Core Components
- **Retriever**: Searches a large-scale knowledge base to find documents relevant to the input query using vector similarity search.
- **Generator**: A sequence-to-sequence model (e.g., BART, T5, GPT-4) that synthesizes the retrieved information to produce a contextually accurate response.

### 1.2 RAG Variants
- **RAG-Sequence**: Conditions the generator on the entire set of retrieved documents concatenated into a single input sequence.
- **RAG-Token**: Conditions the generator at each output token on a weighted combination of the retrieved documents' embeddings.
- **Modular RAG**: Introduces discrete, interchangeable components like query routing, query transformation, and post-retrieval processing (reranking).

## 2. Data Ingestion and Preprocessing

### 2.1 Document Sources
Documents can originate from internal knowledge bases, web crawled content, scientific literature, or proprietary databases.

### 2.2 Parsing and Cleaning
Raw documents must be cleaned by removing noise (headers, footers, HTML tags) and normalizing text (lowercasing, removing special characters).

### 2.3 Chunking Strategies
Large documents must be segmented into smaller chunks to fit within model token limits and improve retrieval granularity.
- **Fixed-Size Chunking**: Splitting text into fixed-length chunks (e.g., 512 tokens) with overlap (e.g., 50 tokens).
- **Semantic Chunking**: Using linguistic boundaries (sentences, paragraphs) to form chunks.
- **Sentence-Window Retrieval**: Indexing single sentences but retrieving the surrounding window of sentences.
- **Auto-merging Retrieval (Hierarchical Chunking)**: Creating a tree structure of chunks where child chunks are replaced by their parent chunk if enough are retrieved.

## 3. Embeddings and Vector Databases

### 3.1 Embedding Models
Embeddings transform text into dense vector representations.
- **Models**: Sentence-BERT, OpenAI embeddings (text-embedding-3-large), DPR.
- **Fine-Tuning**: Contrastive learning or Matryoshka Representation Learning (MRL) can optimize embeddings for specific domains.

### 3.2 Vector Databases
Specialized data stores optimized for high-dimensional embeddings.
- **Popular Solutions**: FAISS, Pinecone, Weaviate, Milvus.
- **Indexing Algorithms**: 
  - **Flat**: Exact search, brute force.
  - **IVF (Inverted File)**: Clusters vectors for faster approximate search.
  - **HNSW (Hierarchical Navigable Small World)**: Graph-based ANN search for low latency.
  - **PQ (Product Quantization)**: Compresses vectors for memory efficiency.

### 3.3 Similarity Search
- **Metrics**: Cosine similarity, Inner product, Euclidean distance.
- **Hybrid Search**: Combining dense retrieval (embeddings) with sparse retrieval (BM25) using Reciprocal Rank Fusion (RRF).

## 4. Advanced Architecture Patterns

### 4.1 Query Transformation
- **HyDE (Hypothetical Document Embeddings)**: Generating a hypothetical answer to embed and search against.
- **Query Rewriting**: Using an LLM to rewrite the user's query for better retrieval.

### 4.2 Post-Retrieval Processing
- **Reranking**: Using Cross-Encoders (e.g., Cohere Rerank) to re-score retrieved chunks based on relevance.
- **Context Compression**: Removing irrelevant tokens from retrieved chunks before passing them to the LLM (e.g., LLMLingua).

### 4.3 Graph RAG
Integrating Knowledge Graphs (KGs) with vector databases to handle complex queries requiring multi-hop reasoning.

## 5. Performance Tuning and Troubleshooting

### 5.1 Latency Reduction
- **Semantic Caching**: Caching previous queries and responses.
- **Streaming**: Streaming LLM tokens to the client.
- **Asynchronous Processing**: Decoupling retrieval and generation phases.

### 5.2 Common Issues and Solutions
- **Hallucinations**: Implement post-processing filters and confidence scoring.
- **Irrelevant Context**: Use query expansion and reranking.
- **Context Window Overflow**: Use sliding windows and summarization techniques.
- **"Lost in the Middle"**: Ensure strict reranking places the most relevant chunks at the beginning or end of the context prompt.

## 6. Security and Governance

### 6.1 Access Control
- **Early Binding (Pre-filtering)**: Storing Access Control Lists (ACLs) as metadata in the vector database and filtering before vector search.
- **Late Binding (Post-filtering)**: Retrieving all documents and filtering in the application layer.

### 6.2 Data Privacy
- Implement PII detection models (e.g., Presidio) to redact sensitive information before embedding.

### 6.3 Prompt Injection Mitigation
- Use Input/Output Guardrails (e.g., NeMo Guardrails, Llama Guard).
- Clearly delineate system instructions from retrieved context using XML tags.

## 7. Evaluation and Observability

### 7.1 RAG Triad Evaluation (RAGAS)
1. **Context Relevance**: Is the retrieved context relevant to the query?
2. **Groundedness (Faithfulness)**: Is the generated answer fully supported by the retrieved context?
3. **Answer Relevance**: Does the generated answer directly address the query?

### 7.2 Monitoring
- Log all queries, retrieved chunks, generated responses, and latency metrics.
- Use tools like Prometheus and Grafana for system health monitoring.
- Implement distributed tracing (e.g., Jaeger, OpenTelemetry) to diagnose performance bottlenecks.

## 8. RAG CLI Command Reference

The `rag` CLI manages RAG deployments:
- `rag init`: Initializes a new RAG project.
- `rag deploy [environment]`: Deploys the RAG to a specified environment.
- `rag status [environment]`: Displays the current status.
- `rag update [environment]`: Updates configuration or codebase.
- `rag rollback [environment]`: Rolls back to a previous state.
- `rag logs [environment]`: Fetches logs.
- `rag config`: Manages configuration settings.
- `rag cleanup [environment]`: Cleans up resources.

## 9. Configuration Schemas

RAG systems use YAML/JSON configurations for various components:
- **Vector Database**: Type, connection, index type (e.g., HNSW), storage path.
- **Embedding Model**: Model name, batch size, device (e.g., cuda).
- **Chunking**: Strategy (e.g., sentence), max length, overlap.
- **Retrieval**: Top_k, metric (e.g., cosine), filter criteria.
- **Generation**: Model name, max tokens, temperature, top_p.
- **Pipeline Orchestration**: Stages, parallelism, error handling (retries, backoff).
