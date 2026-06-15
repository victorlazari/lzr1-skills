# ML Engineering & Model Development

## Table of Contents
1. ML System Design
2. Feature Engineering
3. Model Training
4. Deep Learning Architectures
5. Experiment Tracking
6. Model Evaluation

---

## 1. ML System Design

### Problem Framing

Before building any ML system, answer these questions:
- What is the business metric this model optimizes?
- What is the baseline (rule-based, heuristic, or existing model)?
- What data is available and at what quality/freshness?
- What are latency, throughput, and cost constraints?
- How will the model be served (batch, real-time, edge)?

### ML System Architecture (from Chip Huyen's framework)

```
Data Stack → Feature Store → Training Pipeline → Model Registry → Serving Infrastructure → Monitoring
```

**Key Design Decisions**:

| Decision | Options | Trade-offs |
|---|---|---|
| Batch vs Real-time | Batch (cheaper, simpler) vs Real-time (fresher, complex) | Freshness vs Cost |
| Online vs Offline features | Online (real-time) vs Offline (precomputed) | Latency vs Complexity |
| Model complexity | Simple (interpretable) vs Complex (accurate) | Accuracy vs Debuggability |
| Single vs Ensemble | Single model vs Multiple models | Simplicity vs Performance |
| Retraining frequency | Daily, weekly, triggered | Freshness vs Compute cost |

### Data-Centric AI

Modern ML engineering prioritizes data quality over model complexity:
- Systematic error analysis to identify data issues
- Data augmentation strategies specific to the domain
- Active learning to efficiently label the most informative examples
- Data versioning (DVC, lakeFS) for reproducibility
- Data quality monitoring in production pipelines

---

## 2. Feature Engineering

### Feature Types and Transformations

| Feature Type | Transformations | Tools |
|---|---|---|
| Numerical | Normalization, binning, log transform, polynomial | scikit-learn, Pandas |
| Categorical | One-hot, target encoding, embedding | Category Encoders |
| Text | TF-IDF, embeddings, token counts | Hugging Face, spaCy |
| Temporal | Lag features, rolling stats, cyclical encoding | tsfresh, Featuretools |
| Geospatial | Distance, clustering, grid encoding | GeoPandas, H3 |

### Feature Store Architecture

A feature store provides:
- **Offline store**: Historical features for training (data warehouse/lake)
- **Online store**: Low-latency features for serving (Redis, DynamoDB)
- **Feature registry**: Metadata, lineage, documentation
- **Transformation engine**: Consistent feature computation for train and serve

**Popular Feature Stores**: Feast (open-source), Tecton, Databricks Feature Store, Vertex AI Feature Store

### Feature Engineering Best Practices

- Compute features consistently between training and serving (avoid training-serving skew)
- Log feature distributions and monitor for drift
- Document feature semantics, computation logic, and data sources
- Use feature importance to prune irrelevant features
- Implement feature validation (null checks, range checks, type checks)

---

## 3. Model Training

### Training Pipeline Design

```python
# Canonical training pipeline structure
1. Data ingestion and validation
2. Feature computation and selection
3. Train/validation/test split (time-based for temporal data)
4. Hyperparameter optimization
5. Model training with early stopping
6. Evaluation on held-out test set
7. Model registration and artifact storage
8. Automated quality gates before deployment
```

### Hyperparameter Optimization

| Method | Best For | Tools |
|---|---|---|
| Grid Search | Small search spaces (<20 configs) | scikit-learn |
| Random Search | Medium spaces, good baseline | scikit-learn |
| Bayesian Optimization | Expensive evaluations | Optuna, Ray Tune |
| Multi-fidelity (Hyperband) | Large spaces, early stopping | Ray Tune, BOHB |
| Population-based Training | Neural networks, RL | Ray Tune |

### Distributed Training

- **Data parallelism**: Same model on multiple GPUs, different data batches (most common)
- **Model parallelism**: Split model across GPUs (for models too large for one GPU)
- **Pipeline parallelism**: Split model layers across GPUs with micro-batching
- **ZeRO optimization**: Partition optimizer states, gradients, parameters across GPUs

**Frameworks**: PyTorch DDP, DeepSpeed, FSDP, Horovod, Ray Train

### Fine-Tuning Strategies

| Method | Parameters Updated | Memory | Use Case |
|---|---|---|---|
| Full fine-tuning | All | Very high | Maximum quality, sufficient data |
| LoRA | Low-rank adapters | Low | Most common, good quality/cost |
| QLoRA | Quantized + LoRA | Very low | Limited GPU memory |
| Prefix tuning | Prefix tokens only | Low | Task-specific adaptation |
| Prompt tuning | Soft prompts only | Minimal | Simple task adaptation |
| RLHF/DPO | Reward model + policy | High | Alignment, preference learning |

---

## 4. Deep Learning Architectures

### Transformer Architecture (Foundation)

The Transformer (Vaswani et al., 2017) underpins modern AI:
- **Self-attention**: Captures relationships between all positions in a sequence
- **Multi-head attention**: Multiple attention patterns in parallel
- **Positional encoding**: Injects sequence order information
- **Layer normalization**: Stabilizes training
- **Feed-forward networks**: Non-linear transformations per position

### Architecture Selection Guide

| Architecture | Best For | Examples |
|---|---|---|
| Encoder-only | Classification, embeddings | BERT, RoBERTa |
| Decoder-only | Generation, reasoning | GPT, Llama, Claude |
| Encoder-decoder | Translation, summarization | T5, BART |
| Vision Transformer | Image classification | ViT, DINOv2 |
| Diffusion Models | Image/video generation | Stable Diffusion, DALL-E |
| State Space Models | Long sequences, efficiency | Mamba, S4 |
| Mixture of Experts | Scale with efficiency | Mixtral, Switch Transformer |

### Training Techniques

- **Mixed precision training** (FP16/BF16): 2x speedup, lower memory
- **Gradient accumulation**: Simulate larger batch sizes on limited memory
- **Gradient checkpointing**: Trade compute for memory
- **Learning rate scheduling**: Warmup + cosine decay or linear decay
- **Weight decay**: Regularization for transformers (typically 0.01-0.1)
- **Label smoothing**: Prevents overconfident predictions

---

## 5. Experiment Tracking

### What to Track

- Hyperparameters (all of them, including defaults)
- Training metrics (loss curves, validation metrics per epoch)
- Dataset version and split information
- Code version (git commit hash)
- Environment (Python version, package versions, hardware)
- Model artifacts (checkpoints, final weights)
- Evaluation results on standard benchmarks

### Tools

| Tool | Strengths | Best For |
|---|---|---|
| MLflow | Open-source, full lifecycle | Self-hosted, flexible |
| Weights & Biases | Visualization, collaboration | Teams, research |
| Neptune | Metadata management | Large-scale experiments |
| CometML | Real-time monitoring | Production experiments |
| DVC | Data versioning + experiments | Git-centric workflows |

### Experiment Organization

- Use consistent naming conventions for experiments
- Tag experiments by hypothesis, dataset, architecture
- Document failed experiments (what didn't work and why)
- Maintain a leaderboard of best configurations per task
- Automate experiment comparison reports

---

## 6. Model Evaluation

### Classification Metrics

| Metric | Use When | Formula |
|---|---|---|
| Accuracy | Balanced classes | (TP+TN) / Total |
| Precision | Cost of false positives high | TP / (TP+FP) |
| Recall | Cost of false negatives high | TP / (TP+FN) |
| F1 Score | Balance precision/recall | 2 * P*R / (P+R) |
| AUC-ROC | Threshold-independent ranking | Area under ROC curve |
| PR-AUC | Imbalanced datasets | Area under PR curve |

### Regression Metrics

| Metric | Use When | Properties |
|---|---|---|
| MAE | Robust to outliers | Linear penalty |
| RMSE | Penalize large errors | Quadratic penalty |
| MAPE | Percentage interpretation | Scale-independent |
| R² | Explained variance | 0-1 range |

### Evaluation Best Practices

- Always compare against a meaningful baseline (not just random)
- Use stratified splits for imbalanced data
- Report confidence intervals, not just point estimates
- Evaluate on multiple slices (demographics, time periods, edge cases)
- Use time-based splits for temporal data (never leak future information)
- Perform error analysis: categorize and understand failure modes
- Test for fairness across protected groups
