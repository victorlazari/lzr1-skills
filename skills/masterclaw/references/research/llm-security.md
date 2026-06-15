# LLM Security and Adversarial Defense (2024-2026)

## Executive Summary

The rapid deployment of Large Language Models (LLMs) and agentic AI systems has introduced unprecedented security challenges. As these models become more integrated into critical workflows, their vulnerability to adversarial attacks—such as prompt injection, jailbreaking, and data poisoning—has become a focal point for researchers and industry practitioners. This report synthesizes the latest research (2024-2026) from top academic institutions (Stanford, MIT, ETH Zurich, UC Berkeley) and leading AI labs (Anthropic, OpenAI, Google DeepMind). It explores key architectural patterns, emerging defense frameworks like NeMo Guardrails and Guardrails AI, and the OWASP LLM Top 10 vulnerabilities, providing actionable implementation guidance for production AI systems.

## 1. The Evolving Threat Landscape: Prompt Injection and Jailbreaks

The threat landscape for LLMs has evolved significantly, moving from simple prompt overrides to sophisticated social engineering attacks.

### 1.1 Direct and Indirect Prompt Injection

Prompt injection remains a primary vector for compromising LLM security. Direct prompt injection involves a user intentionally crafting inputs to alter the model's behavior, bypassing safety filters. Indirect prompt injection, however, is increasingly prevalent in agentic systems. In this scenario, malicious instructions are embedded within external data sources (e.g., websites, documents) that the LLM retrieves and processes [1] [2]. Google DeepMind highlights that indirect prompt injections are complex because the model struggles to differentiate between genuine user instructions and manipulative commands embedded in retrieved data [3].

### 1.2 Jailbreaking and Persona Prompts

Jailbreaking involves coercing an LLM to generate harmful or restricted content. Recent research from MIT demonstrates that attackers can systematically generate new jailbreaks by learning policies based on existing successful jailbreak prompts [4]. Furthermore, researchers have found that role-play or persona-based prompts can significantly enhance jailbreak attacks, raising fundamental questions about the relationship between persona adoption and model security [5] [6]. ETH Zurich researchers have even demonstrated the ability to embed universal jailbreak backdoors into models using poisoned human feedback during the RLHF (Reinforcement Learning from Human Feedback) phase [7].

## 2. Key Architectural Patterns and Defense Strategies

Defending against these evolving threats requires a shift from simple input filtering to comprehensive, system-level architectures.

### 2.1 The Social Engineering Lens and Source-Sink Analysis

OpenAI advocates viewing prompt injection through the lens of social engineering. They argue that defending against manipulation cannot rely solely on filtering inputs. Instead, systems must be designed so that the impact of manipulation is constrained, even if an attack succeeds [8]. This involves a source-sink analysis approach: identifying the source (untrusted external content) and the sink (a capability that becomes dangerous in the wrong context, such as transmitting data or executing code). OpenAI's *Safe Url* mitigation strategy exemplifies this by detecting and blocking (or requesting user confirmation) when an agent attempts to transmit sensitive information to a third party [8].

### 2.2 Model Hardening and Inherent Resilience

Google DeepMind emphasizes "model hardening" to build inherent resilience. This involves fine-tuning the LLM on a large dataset of realistic scenarios containing indirect prompt injections. By teaching the model to ignore malicious embedded instructions and follow the original user request, the model's intrinsic ability to recognize and disregard manipulative commands is enhanced [3]. Anthropic similarly uses reinforcement learning to build prompt injection robustness directly into Claude's capabilities, rewarding the model when it correctly identifies and refuses malicious instructions [9].

### 2.3 Defense-in-Depth and Multi-Agent Pipelines

A consensus across top AI labs is the necessity of a "defense-in-depth" approach. This strategy layers multiple protections, including model hardening, input/output classifiers, and system-level guardrails [3] [9]. Academic research also supports this, with proposals for multi-agent defense pipelines where different agents specialize in detecting and mitigating specific vulnerabilities [10].

## 3. Guardrails Frameworks and Output Sanitization

To implement defense-in-depth, the industry has developed robust guardrails frameworks that enforce input isolation and output sanitization.

### 3.1 NVIDIA NeMo Guardrails

NVIDIA's NeMo Guardrails is an open-source toolkit designed to add programmable guardrails to LLM-based conversational systems [11]. It provides a comprehensive framework for input isolation and output sanitization through five main types of rails:
- **Input rails:** Reject or alter user input (e.g., masking sensitive data).
- **Dialog rails:** Influence how the LLM is prompted based on canonical forms.
- **Retrieval rails:** Reject or alter retrieved chunks in Retrieval-Augmented Generation (RAG) scenarios.
- **Execution rails:** Applied to the input and output of custom actions or tools.
- **Output rails:** Reject or alter the final output generated by the LLM before it reaches the user [11].

### 3.2 Guardrails AI and TrueFoundry

Guardrails AI provides an open-source Python framework that acts as a policy specification layer, validating LLM inputs and outputs against defined rules (e.g., PII detection, toxicity, profanity) [12]. Platforms like TrueFoundry integrate these guardrails into AI Gateways, sitting between the application and the LLM (or MCP tool) to inspect, block, or rewrite data. This ensures strict input isolation (checking prompts going in) and output sanitization (checking responses coming out), preventing scenarios like a coding agent executing malicious shell commands [12].

## 4. The OWASP LLM Top 10 (2025)

The Open Worldwide Application Security Project (OWASP) has updated its Top 10 vulnerabilities for LLM applications, providing a critical framework for security assessment [13].

The 2025 OWASP LLM Top 10 includes:
1. **LLM01: Prompt Injection:** Both direct and indirect manipulation of model behavior.
2. **LLM02: Sensitive Information Disclosure:** Leaking PII, financial, or proprietary data.
3. **LLM03: Supply Chain Vulnerabilities:** Risks from compromised third-party models or datasets.
4. **LLM04: Data and Model Poisoning:** Manipulating training data to introduce vulnerabilities.
5. **LLM05: Improper Output Handling:** Failing to validate and sanitize outputs, leading to cross-site scripting (XSS) or code injection.
6. **LLM06: Excessive Agency:** Granting LLMs too much autonomy or control over functions and systems.
7. **LLM07: System Prompt Leakage:** Inadvertent exposure of sensitive instructions or secrets.
8. **LLM08: Vector and Embedding Weaknesses:** Risks associated with RAG implementations.
9. **LLM09: Misinformation:** Generation of false or misleading content (hallucinations).
10. **LLM10: Unbounded Consumption:** Resource exhaustion and denial-of-service (DoS) attacks [13].

Addressing LLM05 (Improper Output Handling) is particularly critical. Outputs must be treated as untrusted user input and subjected to rigorous validation and sanitization to prevent malicious content (e.g., `<script>` tags) from executing in downstream systems [13].

## 5. Implementation Guidance for Production AI Agents

Based on the synthesized research, the following best practices should be implemented for production AI agent systems:

1. **Implement a Defense-in-Depth Architecture:** Do not rely on a single security measure. Combine model hardening (using fine-tuned models resilient to injection), input/output classifiers, and programmable guardrails (like NeMo Guardrails or Guardrails AI).
2. **Enforce Strict Input Isolation:** Treat all external data (user prompts, retrieved documents, web pages) as untrusted. Use input rails to scan for known injection patterns and mask sensitive information before it reaches the LLM context window.
3. **Mandate Output Sanitization:** Never pass LLM outputs directly to downstream systems or users without validation. Implement output rails to sanitize responses, ensuring they conform to expected formats and do not contain executable code or leaked system prompts.
4. **Apply the Principle of Least Privilege (Mitigate Excessive Agency):** Limit the actions an AI agent can take. Use execution rails to validate the arguments passed to tools and APIs. Require human-in-the-loop confirmation for high-risk actions (e.g., transmitting sensitive data, executing destructive commands), as recommended by OpenAI's source-sink analysis.
5. **Conduct Continuous Red Teaming:** Automated and manual red teaming is essential. Use frameworks like Promptfoo to systematically test against the OWASP LLM Top 10, evaluating the system's resilience to adaptive attacks and evolving jailbreak techniques.

## References

[1] Aguilera-Martínez, F., & Berzal, F. (2025). Llm security: Vulnerabilities, attacks, defenses, and countermeasures. arXiv preprint arXiv:2505.01177. https://arxiv.org/abs/2505.01177
[2] Benjamin, V., et al. (2024). Systematically analyzing prompt injection vulnerabilities in diverse LLM architectures. arXiv preprint arXiv:2410.23308. https://arxiv.org/abs/2410.23308
[3] Google DeepMind. (2025). Advancing Gemini's security safeguards. https://deepmind.google/blog/advancing-geminis-security-safeguards/
[4] MIT. (2024). Adversarial Prompt Transformation for Systematic Jailbreaks of LLMs. https://dspace.mit.edu/handle/1721.1/157167
[5] MIT. (2024). Generation, Detection, and Evaluation of Role-play based Jailbreak attacks in Large Language Models. https://dspace.mit.edu/handle/1721.1/156989
[6] arXiv. (2026). Enhancing Jailbreak Attacks on LLMs via Persona Prompts. https://arxiv.org/html/2507.22171v3
[7] ETH Zurich. (2024). Universal jailbreak backdoors from poisoned human feedback. https://www.research-collection.ethz.ch/entities/publication/7be148ad-62c2-41be-997d-aa6f994c9be5
[8] OpenAI. (2026). Designing AI agents to resist prompt injection. https://openai.com/index/designing-agents-to-resist-prompt-injection/
[9] Anthropic. (2025). Mitigating the risk of prompt injections in browser use. https://www.anthropic.com/research/prompt-injection-defenses
[10] arXiv. (2025). A Multi-Agent LLM Defense Pipeline Against Prompt Injection Attacks. https://arxiv.org/html/2509.14285v1
[11] NVIDIA. (2024-2026). NeMo Guardrails Library. https://github.com/NVIDIA-NeMo/Guardrails
[12] TrueFoundry / Guardrails AI. (2024-2026). Guardrails Overview. https://www.truefoundry.com/docs/ai-gateway/guardrails-overview
[13] Promptfoo / OWASP. (2025). OWASP LLM Top 10. https://www.promptfoo.dev/docs/red-team/owasp-llm-top-10/
[14] Stanford University. (2025). Catch Me If You DAN: Outsmarting Prompt Injections and Jailbreak. https://web.stanford.edu/class/cs224n/final-reports/256732118.pdf
[15] UC Berkeley. (2024). Security & Guardrails - Scalable AI. http://scalable-ai.eecs.berkeley.edu/assets/lecture_slides/lecture_23.pdf
[16] MIT. (2024). Provably secure LLMs. https://cap.csail.mit.edu/sites/default/files/resource-pdfs/Boris.pdf
[17] arXiv. (2025). A Systematic Evaluation of Prompt Injection and Jailbreak Vulnerabilities in LLMs. https://arxiv.org/html/2505.04806v1
[18] arXiv. (2025). Evolving Security in LLMs: A Study of Jailbreak Attacks and Defenses. https://arxiv.org/html/2504.02080v1
[19] arXiv. (2025). Multimodal Prompt Injection Attacks: Risks and Defenses for Modern LLMs. https://arxiv.org/html/2509.05883v1
[20] arXiv. (2024). SQL Injection Jailbreak: a structural disaster of large language models. https://arxiv.org/html/2411.01565v1
[21] arXiv. (2025). Progent: Programmable Privilege Control for LLM Agents. https://arxiv.org/html/2504.11703v2
[22] arXiv. (2025). CAPTURE: Context-Aware Prompt Injection Testing and Robustness. https://arxiv.org/html/2505.12368v1
[23] arXiv. (2024). Pathseeker: Exploring llm security vulnerabilities with a reinforcement learning-based jailbreak approach. https://arxiv.org/abs/2409.14177
[24] arXiv. (2025). Meta secalign: A secure foundation llm against prompt injection attacks. https://arxiv.org/abs/2507.02735
[25] arXiv. (2026). The Art of the Jailbreak: Formulating Jailbreak Attacks for LLM Security Beyond Binary Scoring. https://arxiv.org/abs/2605.09225
[26] arXiv. (2026). Which Defense Closes Which Threat? Attributing OWASP-LLM-Top-10 Coverage and Its Brittleness Under Paraphrasing. https://arxiv.org/abs/2606.02822
