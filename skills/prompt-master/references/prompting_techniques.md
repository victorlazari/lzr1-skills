# Comprehensive Taxonomy of Prompting Techniques

This reference provides a structured, evidence-backed taxonomy of prompting techniques compiled from foundational literature and recent surveys [1] [2]. It covers the spectrum from basic single-turn inputs to complex, multi-agent cognitive architectures.

---

## 1. Taxonomic Classification of Prompting

According to the comprehensive survey *The Prompt Report* [1] and Springer's *Taxonomy of Prompt Engineering* [2], prompting techniques are classified into four core operational dimensions:

| Dimension | Description | Core Techniques |
| :--- | :--- | :--- |
| **Profile & Instruction** | Establishing role boundaries, task rules, and formatting constraints. | System Persona, Output Structuring, Negative Constraints. |
| **In-Context Knowledge** | Providing contextual groundings, source documents, or task examples. | Few-Shot Prompting, Dynamic Demonstration Retrieval. |
| **Reasoning & Planning** | Eliciting step-by-step cognitive processes and execution planning. | Chain of Thought (CoT), Tree of Thoughts (ToT), ReAct. |
| **Meta-Control** | Automating prompt refinement, verification, and state management. | Self-Consistency, Self-Critique, Automatic Prompt Optimization. |

---

## 2. Foundational & In-Context Knowledge Techniques

### A. Zero-Shot & Few-Shot Prompting
* **Zero-Shot:** Instructs the model to perform a task without providing any examples. It relies entirely on the model's pre-trained parametric knowledge.
* **Few-Shot (In-Context Learning):** Provides a set of canonical examples showing input-output pairs [1]. 
  * *Design Pattern:* Keep examples diverse and representative of complex edge cases rather than simple "happy paths."
  * *Ordering:* Place examples after system instructions but before specific task inputs to maximize prompt caching efficiency [3].

### B. Dynamic Few-Shot Selection
Instead of hardcoding a static set of examples, select examples dynamically from a database based on their semantic similarity to the user's current query. This keeps the bootstrap size small while providing highly relevant context.

---

## 3. Reasoning & Planning Architectures

Modern frontier models are capable of executing complex, multi-step cognitive plans. Prompt engineering has transitioned from linguistic tricks to **cognitive architecture design**.

```
[Standard Prompting] ──> Direct Input-Output
[Chain of Thought]   ──> Input ──> Step-by-Step Reasoning ──> Output
[Tree of Thoughts]   ──> Input ──> Multiple Branches ──> Evaluation ──> Selection ──> Output
[Graph of Thoughts]  ──> Input ──> Non-linear Nodes ──> Aggregation/Refinement ──> Output
```

### A. Chain of Thought (CoT)
Instructs the model to generate intermediate reasoning steps before producing a final answer [4].
* **Zero-Shot CoT:** Prepend the prompt with instructions like `"Think step-by-step before answering."`
* **Few-Shot CoT:** Provide examples that explicitly show the intermediate reasoning steps.
* *Systemic Shift:* Research indicates that with the emergence of native reasoning models (such as DeepSeek-R1 and the GPT-5 series), explicit CoT instructions in prompts are becoming less necessary, as the models execute reasoning natively in hidden thinking blocks [5].

### B. Tree of Thoughts (ToT) & Graph of Thoughts (GoT)
* **Tree of Thoughts:** Generalizes CoT by allowing the model to explore multiple reasoning paths (branches) as discrete thoughts, evaluate their progress, and backtrack or look ahead to find the optimal path [6].
* **Graph of Thoughts:** Extends ToT by modeling thoughts as a directed graph. This allows the model to combine multiple reasoning paths, loop back to refine previous thoughts, and aggregate distinct ideas into a unified solution [7].

### C. ReAct (Reason-Action-Act)
Combines reasoning and action by prompting the model to generate alternating cycles of **Thoughts**, **Actions** (calling external tools), and **Observations** (processing tool outputs) [8].
* *ReAct Template:*
  ```
  Task: [User Query]
  Thought 1: [Model reasons about what to do]
  Action 1: [Model calls tool]
  Observation 1: [Tool returns result]
  Thought 2: [Model reasons about the result]
  ...
  Final Answer: [Model delivers final result]
  ```

---

## 4. Meta-Control & Self-Correction

### A. Self-Consistency (Ensemble Decoding)
Generates multiple independent reasoning paths (using a high temperature or repeated sampling) and selects the final answer via majority vote [9]. This significantly improves accuracy on mathematical and logical tasks.

### B. Self-Critique & Verification (Chain of Verification)
Instructs the model to critique its own draft response before final output.
1. **Draft Generation:** Generate an initial draft answer.
2. **Fact-Checking Query:** Generate a list of verification questions based on the draft.
3. **Verification:** Answer the verification questions independently (ideally grounding them in retrieved context).
4. **Revision:** Edit the initial draft based on the verification answers to produce the final output [10].

---

## 5. Automated Prompt Optimization (APO)

Prompt engineering can be automated using LLMs as optimizers. This removes human trial-and-error.

### A. PromptQuine (Self-Replicating Prompts)
An evolutionary search framework that automatically searches for the optimal pruning and prompt strategies by framing prompt optimization as a self-replicating, open-ended search [11].

### B. PhaseEvo
A unified optimization framework that simultaneously optimizes the high-level system prompt instructions and the selection of in-context examples, preventing semantic drift in long-context applications [12].

---

## 6. References

* [1] Schulhoff, S., et al. (2024). The Prompt Report: A Systematic Survey of Prompting Techniques. *arXiv preprint arXiv:2406.06608*.
* [2] Springer Frontiers. (2025). A Comprehensive Taxonomy of Prompt Engineering Techniques. *Springer Frontiers of Computer Science*.
* [3] OpenAI. (2025). OpenAI Prompt Caching Developer Guide. *OpenAI Developer Documentation*.
* [4] Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS Proceedings*.
* [5] Wharton School. (2025). The Decreasing Value of Chain of Thought in Prompting. *Wharton Tech Report*.
* [6] Yao, S., et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. *arXiv preprint arXiv:2305.10601*.
* [7] Graph of Thoughts Authors. (2023). Graph of Thoughts: Solving Elaborate Problems with Large Language Models. *arXiv preprint arXiv:2308.09687*.
* [8] Yao, S., et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. *arXiv preprint arXiv:2210.03629*.
* [9] Wang, X., et al. (2022). Self-Consistency Elicits Coherent Reasoning in Large Language Models. *arXiv preprint arXiv:2203.11171*.
* [10] Facebook AI Research. (2023). Chain-of-Verification Reduces Hallucination in Large Language Models. *arXiv preprint arXiv:2309.11495*.
* [11] ICML Evolutionary Group. (2025). Evolving Prompts In-Context: An Open-ended, Self-replicating Perspective (PromptQuine). *arXiv preprint arXiv:2506.17930*.
* [12] PhaseEvo Team. (2025). PhaseEvo: Towards Unified Long-Context Prompt Optimization. *OpenReview / NeurIPS*.
