# YAML Language and Parser Semantics

## Declare the Contract Before Parsing

YAML syntax, scalar resolution, application schema, and consumer behavior are separate contracts. This package uses **YAML 1.2**, the **Core Schema**, duplicate-key rejection, safe construction, and bounded inputs for its own utilities. A target repository may use another profile only when it names the parser, version, schema, and consumer that require it. YAML 1.2.2 clarifies YAML 1.2 without normative changes.[1]

| Contract dimension | Required evidence | Unsafe shortcut |
|---|---|---|
| Language revision | `1.2.2` or explicitly justified alternative | “valid YAML” without a revision |
| Resolution schema | Core, JSON, failsafe, or implementation profile | Assuming all parsers type scalars identically |
| Duplicate keys | Rejected before application validation | Last-key-wins parsing |
| Construction mode | Safe or round-trip safe loader; no custom object constructors | Generic or unsafe object loading |
| Consumer | Helm, Kubernetes, CI engine, application, or library and exact version | Treating parser acceptance as consumer acceptance |
| Resource bounds | Bytes, documents, aliases, nodes, depth, files, and diagnostics | Parsing unbounded untrusted input |

## Scalar Resolution and Cross-Parser Hazards

YAML 1.1 and YAML 1.2 differ in several implicit scalar forms. Tokens such as `yes`, `no`, `on`, `off`, leading-zero numerals, timestamp-like text, and implementation-specific numeric forms can change type across parsers. Quote an identifier when its lexical form matters, use canonical booleans (`true` and `false`), and test the actual consumer parser rather than relying on a generic linter.[1]

| Intended value | Portable form | Review note |
|---|---|---|
| Boolean | `enabled: true` | Do not use `yes`, `on`, or single-letter variants |
| String that resembles a boolean | `mode: "off"` | Quoting preserves string intent |
| Version or tag | `appVersion: "1.2"` | Prevent numeric coercion and loss of lexical form |
| Date-like identifier | `releaseDate: "2026-08-07"` | Test applications that construct timestamps |
| Leading-zero identifier | `code: "00123"` | Never depend on numeric interpretation |
| Null | `value: null` | Use a schema to distinguish absent, null, and empty string |

The package’s portability warning is deliberately narrower than a style rule. It flags common YAML 1.1/1.2 disagreements, while a repository’s schema still determines whether the resulting value is semantically acceptable.

## Mappings, Sequences, and Keys

Configuration contracts should use string mapping keys when values flow into JSON Schema, Helm values, Kubernetes objects, or JSON-producing APIs. Complex keys, tagged keys, and non-string keys are valid in parts of YAML’s representation model but fall outside the JSON data model and many consumer implementations.[1][2]

| Construct | Default disposition | Reason |
|---|---|---|
| Duplicate mapping key | Error | Ambiguous overwrite and policy-shadowing risk |
| Merge key `<<` | Reject in portable contracts | Not part of YAML 1.2 Core Schema and unevenly supported |
| Anchor or alias | Warn and test consumer | Identity, expansion, and implementation behavior vary |
| Custom tag | Reject by default | Can trigger unsupported or unsafe construction |
| Complex/non-string key | Reject for JSON-compatible consumers | Outside the JSON object model |
| Flow mapping/sequence | Permit only if project style and consumers support it | Harder review and comment attachment |

## Safe Construction and Untrusted Inputs

A parser must not instantiate arbitrary application or Python objects from untrusted tags. PyYAML’s own documentation warns that unrestricted `yaml.load` is as powerful as pickle loading.[3] This package therefore uses `ruamel.yaml` with a safe round-trip profile, never registers arbitrary constructors, rejects duplicate keys, and recreates parser instances per input. Its current tested dependency is recorded in `scripts/requirements.txt` and must not be auto-installed.[4]

> Parser safety is not only about code execution. Alias expansion, deep nesting, large document streams, huge scalars, excessive diagnostics, remote schema references, and symlinked paths can exhaust resources or escape the intended review boundary.

| Bound | Package default | Change rule |
|---|---:|---|
| Input file size | 2 MiB per analyzer input | Increase explicitly and record why |
| YAML documents | 100 | Increase only for an identified manifest bundle |
| Parsed depth | 80 | Treat deeper input as adversarial until reviewed |
| Parsed nodes | 200,000 | Preserve deterministic memory ceilings |
| Anchor/alias tokens | 1,000 | Lower for untrusted public input where practical |
| Diagnostics | Tool-specific bounded output | Preserve total counts when truncating details |

## Multi-Document Streams

A YAML stream can contain zero, one, or multiple documents. A values contract generally requires exactly one root mapping; rendered Kubernetes evidence may legitimately contain many documents. Validators must preserve document indexes, reject non-object Kubernetes documents, and never stop after the first successful document.

| Input type | Expected shape | Evidence requirement |
|---|---|---|
| `values.yaml` | One mapping document | Exact parser profile and duplicate-key policy |
| `Chart.yaml` | One mapping document | Helm chart schema and field semantics |
| Rendered manifests | Multi-document mapping stream | Document/object counts and per-object identity |
| Arbitrary YAML bundle | Declared by caller | Per-document type and validation outcome |

## Comments, Round Trips, and Mutation

Comments are not part of the YAML representation graph and disappear in many load/dump workflows. Use a round-trip-capable parser when comments, quoting, key order, or local metadata conventions must survive. Even then, preview the exact diff because emitters can normalize indentation, flow style, directives, anchors, quoting, or line endings.

The skill never rewrites a target file during discovery or validation. A user-authorized edit is created as a reviewed change set, applied to a clean or explicitly acknowledged worktree, validated against all declared consumers, and rolled back if output semantics or compatibility change unexpectedly.

## Minimal Decision Procedure

| Question | Decision |
|---|---|
| Is the target consumer known? | Record its exact version and parser profile before editing |
| Are duplicate keys present? | Stop; resolve intent before any schema validation |
| Does a scalar’s lexical form matter? | Quote it and constrain it with application schema |
| Does the document use custom tags, merges, or complex keys? | Treat as non-portable and obtain consumer-specific evidence |
| Is the input untrusted or large? | Enforce bounds and safe construction before analysis |
| Will formatting or comments be changed? | Use round-trip parsing, preview the diff, and test every consumer |

[1]: https://yaml.org/spec/1.2.2/
[2]: https://json-schema.org/draft/2020-12/json-schema-core
[3]: https://pyyaml.org/wiki/PyYAMLDocumentation
[4]: https://yaml.dev/doc/ruamel.yaml/api/
