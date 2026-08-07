# CLI and NLP Tools for French Text Processing

This reference outlines tools for analyzing French texts, useful for assessing readability, vocabulary frequency, and grammatical complexity.

## CLI Tools

Standard Unix tools can be used for basic text processing.

- **grep:** Search for specific words or patterns (e.g., finding all instances of the subjunctive).
  ```bash
  grep -iE '\b(que je sois|qu'\''il fasse)\b' text.txt
  ```
- **sed:** Stream editor for text substitution.
- **awk:** Text processing and data extraction.
- **wc:** Count words, lines, and characters to assess text length.

## NLP Libraries (Python)

For deeper linguistic analysis, use Python NLP libraries.

### spaCy
spaCy provides robust models for French (`fr_core_news_sm`, `fr_core_news_md`, `fr_core_news_lg`).

- **Capabilities:** Tokenization, Part-of-Speech (POS) tagging, dependency parsing, Named Entity Recognition (NER), and lemmatization.
- **Use Case:** Analyzing the grammatical complexity of a text by examining dependency trees or counting specific POS tags (e.g., frequency of adjectives vs. verbs).

### NLTK (Natural Language Toolkit)
NLTK offers basic tools for French, including tokenizers and stemmers (e.g., SnowballStemmer for French).

- **Capabilities:** Tokenization, stemming, frequency distributions.
- **Use Case:** Generating vocabulary frequency lists to determine if a text is suitable for a specific CEFR level.

### CamemBERT
CamemBERT is a state-of-the-art language model for French based on the RoBERTa architecture.

- **Capabilities:** Contextual embeddings, masked language modeling, fine-tuning for downstream tasks (e.g., text classification, sentiment analysis).
- **Use Case:** Advanced semantic analysis or building custom classifiers for CEFR level prediction.
