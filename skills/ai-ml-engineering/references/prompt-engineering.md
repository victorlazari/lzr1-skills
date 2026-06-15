# Prompt Engineering

## Table of Contents
1. Prompt Design Principles
2. Advanced Techniques
3. Structured Output
4. Evaluation and Testing
5. Production Prompt Management
6. Model-Specific Optimization

---

## 1. Prompt Design Principles

### The CLEAR Framework

- **C**ontext: Provide relevant background information
- **L**ength: Be specific about output format and length
- **E**xamples: Include few-shot examples for complex tasks
- **A**ction: State clearly what the model should do
- **R**efinement: Iterate based on evaluation results

### Fundamental Principles

1. **Be specific and unambiguous** — Vague instructions produce inconsistent outputs
2. **Provide structure** — Use headers, numbered steps, XML tags to organize prompts
3. **Define the output format** — Show exactly what the response should look like
4. **Include constraints** — State what NOT to do as well as what to do
5. **Use delimiters** — Separate instructions from content with clear markers
6. **Order matters** — Place critical instructions at the beginning and end (primacy/recency)

### Prompt Structure Template

```
[System/Role Definition]
You are a [specific role] with expertise in [domain].

[Task Description]
Your task is to [specific action] given the following [input type].

[Constraints]
- Do NOT [constraint 1]
- Always [constraint 2]
- Output must be [format specification]

[Examples] (if few-shot)
Input: [example input]
Output: [example output]

[Input]
<input>
{actual_input}
</input>

[Output Instructions]
Respond with [format] containing [fields].
```

---

## 2. Advanced Techniques

### Chain-of-Thought (CoT) Prompting

Force the model to reason step-by-step before answering:
- **Zero-shot CoT**: Add "Let's think step by step" or "Think through this carefully"
- **Few-shot CoT**: Provide examples with explicit reasoning chains
- **Structured CoT**: Define specific reasoning steps to follow

### Tree of Thoughts (ToT)

For complex problems requiring exploration:
- Generate multiple reasoning paths
- Evaluate each path's promise
- Backtrack from dead ends
- Select the best complete solution

### Self-Consistency

- Generate multiple responses with temperature > 0
- Take the majority vote or most common answer
- Particularly effective for math and logic problems
- Trade-off: Higher cost for higher reliability

### Meta-Prompting

- Ask the model to generate or improve its own prompts
- Use the model to identify weaknesses in current prompts
- Implement prompt optimization loops

### Decomposition Strategies

| Strategy | Description | Use Case |
|---|---|---|
| Sequential decomposition | Break into ordered steps | Multi-step reasoning |
| Parallel decomposition | Independent sub-problems | Multi-aspect analysis |
| Recursive decomposition | Divide and conquer | Complex nested problems |
| Least-to-most | Solve simpler version first | Progressive complexity |

---

## 3. Structured Output

### JSON Output

```
Respond with a JSON object with the following schema:
{
  "field_name": "description of what goes here (type: string)",
  "numeric_field": "description (type: number, range: 0-100)",
  "array_field": ["description of each element"]
}
```

### XML Output

Use XML tags for complex nested structures:
```
<analysis>
  <summary>Brief overview</summary>
  <findings>
    <finding severity="high|medium|low">Description</finding>
  </findings>
  <recommendation>Action to take</recommendation>
</analysis>
```

### Function Calling / Tool Use

- Define tools with clear names, descriptions, and parameter schemas
- Include parameter constraints (required, enum values, ranges)
- Provide examples of when each tool should be used
- Handle cases where no tool is appropriate

### Output Validation

- Use JSON Schema validation for structured outputs
- Implement retry logic for malformed outputs
- Define fallback behavior for validation failures
- Log validation failures for prompt improvement

---

## 4. Evaluation and Testing

### Prompt Testing Framework

```
1. Define test cases (inputs + expected outputs)
2. Categorize: happy path, edge cases, adversarial, out-of-scope
3. Run prompts against test suite
4. Score with automated metrics + human review
5. Track metrics over prompt versions
6. Regression test on every change
```

### Evaluation Methods

| Method | Automation | Quality | Cost |
|---|---|---|---|
| Exact match | Full | Low (brittle) | Free |
| Regex/pattern match | Full | Medium | Free |
| LLM-as-judge | Full | High | Medium |
| Human evaluation | None | Highest | High |
| A/B testing | Full | High (production) | Medium |

### LLM-as-Judge Pattern

```
You are evaluating the quality of an AI response.

<criteria>
- Accuracy: Is the information factually correct? (1-5)
- Relevance: Does it address the user's question? (1-5)
- Completeness: Does it cover all aspects? (1-5)
- Clarity: Is it well-written and easy to understand? (1-5)
</criteria>

<user_query>{query}</user_query>
<ai_response>{response}</ai_response>

Evaluate the response against each criterion. Provide scores and brief justification.
```

### Red Teaming

Test prompts against adversarial inputs:
- Prompt injection attempts
- Jailbreak attempts
- Edge cases (empty input, very long input, special characters)
- Out-of-scope requests
- Contradictory instructions
- Social engineering attempts

---

## 5. Production Prompt Management

### Prompt Versioning

- Store prompts in version control (git)
- Use semantic versioning (major.minor.patch)
- Document changes and rationale for each version
- Maintain a changelog with performance metrics
- Tag prompts with associated model versions

### Prompt Architecture Patterns

| Pattern | Description | Use Case |
|---|---|---|
| Single prompt | One prompt does everything | Simple tasks |
| Chained prompts | Output of one feeds next | Multi-step workflows |
| Router + specialists | Classify then route to specialized prompts | Complex varied inputs |
| Template + variables | Base template with dynamic content | Personalization |
| Layered system prompt | Base + domain + task layers | Multi-tenant systems |

### Configuration Management

```yaml
# prompt_config.yaml
name: "customer_support_classifier"
version: "2.3.1"
model: "claude-sonnet-4-20250514"
temperature: 0.0
max_tokens: 500
system_prompt_file: "prompts/support_classifier_system.txt"
few_shot_examples_file: "prompts/support_classifier_examples.json"
evaluation_dataset: "eval/support_classifier_golden.json"
minimum_accuracy: 0.95
```

### Prompt Optimization Workflow

1. Establish baseline metrics on evaluation dataset
2. Identify failure modes through error analysis
3. Hypothesize improvements (more examples, clearer instructions, different structure)
4. A/B test changes against baseline
5. Deploy winning variant with monitoring
6. Continuously collect failure cases for next iteration

---

## 6. Model-Specific Optimization

### Claude (Anthropic)

- Use XML tags for structure (`<instructions>`, `<context>`, `<output>`)
- Place important instructions at the end of the prompt (recency bias)
- Use "think step by step" in a `<thinking>` tag for reasoning tasks
- Leverage extended thinking for complex analysis
- System prompts are strongly followed; use for persona and constraints

### GPT-4 / GPT-4o (OpenAI)

- System message is powerful for setting behavior
- JSON mode available for structured output
- Function calling for tool use (well-supported)
- Seed parameter for reproducibility
- Structured Outputs for guaranteed schema compliance

### Open-Source Models (Llama, Mistral)

- Follow model-specific chat templates exactly
- Shorter, more direct prompts often work better
- May need more explicit few-shot examples
- Test thoroughly; behavior varies more across versions
- Consider fine-tuning for consistent behavior on specific tasks

### General Cross-Model Tips

- Always test prompts on the specific model version you'll deploy
- Prompts that work on one model may fail on another
- Simpler prompts are more portable across models
- Document which model version each prompt was optimized for
- Re-evaluate prompts when upgrading model versions
