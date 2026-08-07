# AI Testing

**Verified against upstream: 2026-08-07**
**Normative Guidance**: ISO/IEC/IEEE 29119-11

## Table of Contents
1. AI Testing Challenges
2. Testing Machine Learning Models
3. Testing Generative AI (LLMs)
4. AI Quality Characteristics

---

## 1. AI Testing Challenges

Testing AI-based systems differs significantly from traditional software testing due to non-determinism, data dependency, and complex internal logic.

| Challenge | Description | Mitigation |
|---|---|---|
| Non-determinism | Same input may yield different outputs | Use statistical testing, define acceptable variance |
| Oracle problem | Difficult to determine the "correct" output | Metamorphic testing, A/B testing, expert review |
| Data dependency | Model quality depends entirely on training data | Data validation, bias detection, data drift monitoring |
| Black box nature | Internal decision process is opaque | Explainable AI (XAI) techniques, feature importance |

---

## 2. Testing Machine Learning Models

### ML Testing Lifecycle

| Phase | Testing Focus | Techniques |
|---|---|---|
| Data Preparation | Data quality, completeness, bias | Exploratory Data Analysis (EDA), schema validation |
| Model Training | Convergence, overfitting, underfitting | Cross-validation, learning curves |
| Model Evaluation | Accuracy, precision, recall, F1-score | Confusion matrix, ROC/AUC |
| Deployment | Performance, latency, integration | Shadow deployment, canary releases |
| Monitoring | Data drift, concept drift, degradation | Continuous monitoring, feedback loops |

### Metamorphic Testing

Used when a true oracle is unavailable. Tests relations between inputs and outputs.

```
Example: Sentiment Analysis Model
Relation: Adding a neutral sentence should not change the overall sentiment.
Input A: "The product is great." -> Output: Positive
Input B: "The product is great. It arrived on Tuesday." -> Output: Positive
```

---

## 3. Testing Generative AI (LLMs)

### LLM Evaluation Metrics

| Metric | Description | Tool/Approach |
|---|---|---|
| Perplexity | How well the model predicts a sample | Statistical calculation |
| BLEU/ROUGE | N-gram overlap with reference text | Translation/Summarization tasks |
| Factuality | Accuracy of factual claims | Retrieval-Augmented Generation (RAG) evaluation |
| Toxicity/Bias | Presence of harmful or biased content | Perspective API, RealToxicityPrompts |
| Prompt Injection | Resistance to malicious prompts | Adversarial testing, red teaming |

### Red Teaming LLMs

Simulate adversarial attacks to identify vulnerabilities in generative models.

- **Jailbreaking**: Bypassing safety filters to generate restricted content.
- **Prompt Injection**: Overriding system instructions with user input.
- **Data Extraction**: Tricking the model into revealing training data or PII.

---

## 4. AI Quality Characteristics (ISO/IEC 25059)

| Characteristic | Description | Testing Approach |
|---|---|---|
| Functional Suitability | Does it perform the intended task? | Benchmark datasets, domain-specific tests |
| Reliability | Does it handle edge cases and noise? | Robustness testing, adversarial perturbations |
| Usability | Is the output understandable? | Explainability evaluation, user studies |
| Security | Is it resistant to attacks? | Red teaming, model inversion tests |
| Safety | Does it avoid causing harm? | Hazard analysis, safety constraints testing |
| Fairness | Is it free from unacceptable bias? | Demographic parity, equal opportunity metrics |
