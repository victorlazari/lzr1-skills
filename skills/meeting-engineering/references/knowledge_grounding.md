# Real-Time Knowledge Grounding (RAG)

A live meeting assistant must provide the *right* comment at the *right* moment, grounded in an authoritative knowledge base (KB) repository. This reference covers how to collect information in real time during the meeting and retrieve relevant context fast enough to fit within the conversational latency budget.

## Architecture: Two Parallel Loops

The assistant runs two loops concurrently over the same transcript stream:

1.  **Fast Response Loop (synchronous, <1s)**: Triggered by turn detection when the bot is directly addressed or must respond. Uses pre-fetched context plus a fast retrieval pass.
2.  **Ambient Comprehension Loop (asynchronous, continuous)**: Continuously consumes committed transcript segments, extracts entities and topics, and *speculatively pre-fetches* relevant KB documents into a hot cache. This is the key to low-latency grounded answers: by the time the bot is asked a question, the relevant documents are usually already in memory.

## Knowledge Base Repository Design

Structure the KB as a versioned repository (e.g., Git) of Markdown/text documents, ingested into a vector store at deploy time or on webhook-triggered re-index.

*   **Chunking**: Split documents into 256–512 token chunks with 10–15% overlap. Preserve heading hierarchy in chunk metadata (`doc_path`, `section`, `updated_at`).
*   **Embeddings**: Use a fast embedding model. Cache embeddings keyed by content hash so re-indexing only processes changed chunks.
*   **Storage**: For sub-50ms retrieval, use `pgvector` in the existing PostgreSQL instance (HNSW index) or an in-memory index for small KBs (<50k chunks). Valkey/Redis can serve as the hot cache for pre-fetched chunks with a meeting-scoped TTL.
*   **Hybrid Search**: Combine vector similarity with keyword/BM25 search. Meeting speech contains exact identifiers (ticket numbers, product names, version strings) that pure semantic search misses.

## Real-Time Context Assembly

For every LLM call, assemble the prompt from layered context, ordered by stability (stable first to maximize prompt-cache hits):

| Layer | Content | Refresh Rate |
| --- | --- | --- |
| System persona | Bot identity, speaking style, meeting etiquette rules | Static |
| Meeting metadata | Title, agenda, participants (from Calendar event) | Once at join |
| KB retrieved chunks | Top 3–6 chunks from hybrid search over recent transcript | Per turn |
| Rolling summary | Compressed summary of older transcript | Every ~2 min |
| Recent transcript | Verbatim last ~15–20 turns with speaker labels | Per turn |
| Trigger utterance | The committed transcript that triggered the response | Per turn |

Keep the assembled prompt small (target <4k tokens) — prompt size directly affects time-to-first-token on the LLM.

## Retrieval Triggers and Relevance Gating

Not every utterance deserves a comment. Implement a lightweight relevance gate before generating speech:

*   **Direct address**: Wake words / bot name detected in the transcript → always respond.
*   **Question detection**: Interrogative utterances about topics matching KB content above a similarity threshold → respond with grounded answer.
*   **Correction opportunities**: A factual claim contradicting a high-confidence KB chunk → optionally interject (configurable; default off to avoid being annoying).
*   **Silence otherwise**: The default behavior is to stay silent. A meeting bot that comments too often gets removed.

The gate can be a cheap classifier call (single fast-LLM call returning `respond` / `stay_silent` / `log_only`) running on the ambient loop, or rule-based (name regex + question heuristics) for zero added latency.

## Rolling Summarization and Memory

Long meetings overflow any context window. Maintain per-meeting segregated memory:

*   Every N committed segments (or ~2 minutes), an async worker compresses the oldest transcript turns into a rolling summary (decisions, action items, open questions, who said what).
*   Persist segments, summaries, and extracted action items to PostgreSQL keyed by `meeting_id` so post-meeting artifacts (minutes, Slack summary) are generated from structured data, not a re-read of raw audio.
*   Each meeting/user gets isolated memory — never leak context between concurrent meetings handled by the same fleet.

## Latency Discipline for Retrieval

Retrieval must fit inside the response budget. Practical targets: embedding of the query <30ms (cache common queries), vector + keyword search <50ms, re-ranking (optional, only if needed) <100ms. If retrieval exceeds ~150ms, skip re-ranking and use raw hybrid results. When the ambient loop pre-fetched relevant chunks, retrieval at response time becomes a Valkey cache read (<5ms).
