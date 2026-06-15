# NLP Systems

## Table of Contents
1. Text Processing Pipeline
2. Embeddings and Semantic Search
3. RAG Implementation
4. Conversational AI
5. Text Classification and NER
6. Evaluation

---

## 1. Text Processing Pipeline

### Standard NLP Pipeline

```
Raw Text → Cleaning → Tokenization → Normalization → Feature Extraction → Model → Post-processing
```

### Text Preprocessing

| Step | Purpose | Tools |
|---|---|---|
| Unicode normalization | Consistent encoding | unicodedata, ftfy |
| HTML/markup removal | Clean text extraction | BeautifulSoup, bleach |
| Tokenization | Split into tokens | Hugging Face tokenizers, spaCy |
| Lowercasing | Normalize case | Built-in (context-dependent) |
| Stopword removal | Remove noise | spaCy, NLTK (use cautiously) |
| Lemmatization | Normalize word forms | spaCy, stanza |
| Sentence segmentation | Split into sentences | spaCy, pySBD |

### Tokenization Strategies

| Method | Description | Use Case |
|---|---|---|
| BPE (Byte-Pair Encoding) | Iterative merge of frequent pairs | GPT models |
| WordPiece | Similar to BPE, likelihood-based | BERT models |
| SentencePiece | Language-agnostic, unigram/BPE | Multilingual models |
| Tiktoken | OpenAI's fast BPE implementation | OpenAI API token counting |

### Language Detection and Multilingual Processing

- Use langdetect or fasttext for language identification
- Consider multilingual models (mBERT, XLM-R) for cross-lingual tasks
- Handle mixed-language text with per-sentence language detection
- Be aware of tokenizer efficiency differences across languages

---

## 2. Embeddings and Semantic Search

### Embedding Model Selection

| Model | Dimensions | Strengths | Use Case |
|---|---|---|---|
| OpenAI text-embedding-3-large | 3072 | High quality, API | General purpose |
| OpenAI text-embedding-3-small | 1536 | Cost-effective, API | Budget-conscious |
| Cohere embed-v3 | 1024 | Multilingual, compression | Multilingual search |
| BGE-large-en-v1.5 | 1024 | Open-source, high quality | Self-hosted |
| E5-mistral-7b-instruct | 4096 | Instruction-following | Complex queries |
| all-MiniLM-L6-v2 | 384 | Fast, lightweight | Low-latency |
| Nomic embed-text | 768 | Long context (8192) | Long documents |

### Embedding Best Practices

- Normalize embeddings for cosine similarity (most models do this internally)
- Use instruction-prefixed embeddings when available (separate query/document prefixes)
- Benchmark on your specific domain before choosing a model
- Consider dimensionality reduction (Matryoshka embeddings) for storage optimization
- Cache embeddings; recompute only when source documents change
- Monitor embedding quality with retrieval benchmarks on your data

### Semantic Search Architecture

```
Query → Query Embedding → ANN Search → Top-K Results → Reranking → Final Results
```

**Approximate Nearest Neighbor (ANN) algorithms**:
- HNSW (Hierarchical Navigable Small World): Best recall/speed trade-off
- IVF (Inverted File Index): Good for large-scale, memory-efficient
- ScaNN: Google's optimized ANN library
- FAISS: Facebook's similarity search library (IVF, PQ, HNSW)

---

## 3. RAG Implementation

### Production RAG Architecture

```
Document Ingestion:
  Documents → Parsing → Chunking → Embedding → Vector Store + Metadata Store

Query Processing:
  User Query → Query Enhancement → Hybrid Retrieval → Reranking → Context Assembly → LLM Generation → Response
```

### Document Parsing

| Format | Parser | Notes |
|---|---|---|
| PDF | PyMuPDF, Unstructured, LlamaParse | Handle tables, images |
| HTML | BeautifulSoup, Trafilatura | Extract main content |
| DOCX | python-docx, Unstructured | Preserve structure |
| Markdown | markdown-it | Native structure |
| Code | tree-sitter | AST-aware chunking |

### Advanced RAG Techniques

**Query Enhancement**:
- Query decomposition: Break complex queries into sub-queries
- Query expansion: Add synonyms, related terms
- Step-back prompting: Ask a more general question first
- HyDE: Generate hypothetical answer, use as retrieval query

**Retrieval Enhancement**:
- Hybrid search: Combine BM25 (keyword) + dense (vector) retrieval
- Multi-index: Separate indexes for different document types
- Recursive retrieval: Retrieve summaries first, then drill into details
- Knowledge graph augmentation: Use entity relationships to expand context

**Generation Enhancement**:
- Chain-of-note: Generate retrieval notes before final answer
- Self-RAG: Model decides when to retrieve and self-evaluates
- CRAG (Corrective RAG): Evaluate retrieval quality, search web if insufficient
- Contextual compression: Remove irrelevant parts of retrieved passages

### Chunking Implementation

```python
# Recommended chunking parameters
CHUNK_SIZE = 512  # tokens (adjust based on model context and document type)
CHUNK_OVERLAP = 50  # tokens (10-20% of chunk size)
SEPARATORS = ["\n\n", "\n", ". ", " "]  # hierarchical splitting

# For code: use AST-aware chunking (functions, classes as natural boundaries)
# For tables: keep tables as single chunks with metadata
# For conversations: chunk by turn or topic
```

---

## 4. Conversational AI

### Conversation Architecture

```
User Input → Intent Detection → Slot Filling → Dialog Management → Response Generation → Output
```

### Dialog Management Patterns

| Pattern | Complexity | Use Case |
|---|---|---|
| Single-turn Q&A | Low | FAQ bots, search |
| Multi-turn with memory | Medium | Customer support |
| Task-oriented dialog | High | Booking, ordering |
| Open-domain chat | High | Companions, assistants |
| Agent-based | Very high | Complex workflows |

### Context Management

- **Sliding window**: Keep last N turns (simple, loses early context)
- **Summarization**: Summarize older turns, keep recent verbatim
- **Retrieval-based**: Store all turns, retrieve relevant ones per query
- **Hierarchical**: Session summary + recent turns + retrieved history

### Conversation Quality

- Maintain consistent persona and tone across turns
- Handle topic switches gracefully
- Implement clarification requests for ambiguous inputs
- Track conversation state explicitly (slots, intents, entities)
- Implement graceful fallbacks for out-of-scope queries
- Log conversations for quality analysis and improvement

---

## 5. Text Classification and NER

### Classification Approaches

| Approach | Data Needed | Quality | Speed |
|---|---|---|---|
| Zero-shot (LLM) | None | Good | Slow |
| Few-shot (LLM) | 5-20 examples | Better | Slow |
| Fine-tuned BERT | 1000+ examples | Best | Fast |
| SetFit | 8-64 examples | Very good | Fast |
| Traditional ML (TF-IDF + SVM) | 100+ examples | Good | Very fast |

### Named Entity Recognition

**Approaches**:
- **SpaCy NER**: Fast, pre-trained for common entities (PERSON, ORG, GPE, DATE)
- **Hugging Face token classification**: Fine-tune BERT/RoBERTa for custom entities
- **LLM extraction**: Zero/few-shot entity extraction with structured output
- **GLiNER**: Generalist NER model for any entity type without fine-tuning

**Best Practices**:
- Define clear entity boundaries and annotation guidelines
- Handle nested entities (e.g., "Bank of America" contains "America")
- Use BIO/BILOU tagging schemes for sequence labeling
- Evaluate with entity-level F1 (not token-level)
- Consider entity linking (mapping to knowledge base IDs)

---

## 6. Evaluation

### NLP-Specific Metrics

| Task | Metrics | Tools |
|---|---|---|
| Classification | F1, Precision, Recall, AUC | scikit-learn |
| NER | Entity-level F1, Span F1 | seqeval |
| Generation | BLEU, ROUGE, BERTScore, METEOR | evaluate (HF) |
| Retrieval | MRR, NDCG, Recall@K | ranx, pytrec_eval |
| Summarization | ROUGE-L, BERTScore, factual consistency | evaluate (HF) |
| Translation | BLEU, chrF, COMET | sacrebleu, COMET |
| Semantic similarity | Spearman correlation, Pearson | scipy |

### LLM Output Evaluation

- **Faithfulness**: Is the output grounded in the provided context?
- **Relevance**: Does the output address the user's question?
- **Coherence**: Is the output logically structured and readable?
- **Harmlessness**: Does the output avoid toxic or biased content?
- **Helpfulness**: Does the output provide actionable, useful information?

### Evaluation Frameworks

| Framework | Focus | Approach |
|---|---|---|
| RAGAS | RAG evaluation | Automated metrics for RAG |
| DeepEval | LLM evaluation | Multiple metrics, unit test style |
| LangSmith | Tracing + evaluation | End-to-end LLM app evaluation |
| Promptfoo | Prompt testing | CI/CD for prompts |
| Braintrust | LLM evaluation | Logging, scoring, comparison |
