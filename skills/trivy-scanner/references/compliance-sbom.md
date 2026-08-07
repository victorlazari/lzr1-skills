# Trivy SBOM, Attestation, VEX, and Compliance Evidence

**Verified against upstream:** 2026-08-07

## Contents

1. [Evidence boundaries](#evidence-boundaries)
2. [Generate an SBOM](#generate-an-sbom)
3. [Validate and retain an SBOM](#validate-and-retain-an-sbom)
4. [Scan an existing SBOM](#scan-an-existing-sbom)
5. [Attest and verify](#attest-and-verify)
6. [Use VEX safely](#use-vex-safely)
7. [Compliance reports](#compliance-reports)
8. [Custom compliance specifications](#custom-compliance-specifications)
9. [Required output record](#required-output-record)
10. [Sources](#sources)

## Evidence boundaries

Trivy can produce technical security and inventory evidence. It does not by itself:

- prove that an SBOM is complete;
- prove that a VEX issuer is authoritative;
- certify compliance with a benchmark, regulation, or contract;
- make a legal license-compatibility decision;
- prove that an artifact is the one deployed;
- sign or verify an attestation's trust policy merely because it can parse its content.

Preserve target identity, scanner identity, configuration, data-source freshness, coverage warnings, and output hashes with every result.

## Generate an SBOM

Trivy can generate CycloneDX and SPDX output from supported targets. Confirm exact format names with the installed command:

```bash
trivy <target-command> --help
```

Representative patterns:

```bash
# Local project
trivy fs --format cyclonedx --output sbom.cdx.json /absolute/project
trivy fs --format spdx-json --output sbom.spdx.json /absolute/project

# Immutable container target
trivy image --format cyclonedx --output image.sbom.cdx.json \
  registry.example/app@sha256:<digest>
```

Use an immutable target identity where available. Do not assume two formats or two generators have identical component coverage, relationship data, license evidence, or properties.

For each SBOM record:

| Field | Requirement |
|---|---|
| Target | Canonical path plus commit, image digest/platform, VM hash, or equivalent immutable identity |
| Generator | Trivy version plus executable hash/image digest/action SHA |
| Invocation | Redacted command, configuration hash, selected scanners/options |
| Format | CycloneDX/SPDX serialization and declared spec version |
| Time | RFC 3339 generation timestamp |
| Data | Database/check metadata when vulnerability content is requested |
| File | Path, byte size, and SHA-256 digest |
| Coverage | Detected ecosystems, warnings, unsupported/skipped content |

SBOM output may include Trivy-specific properties such as image/repository/layer/source-package metadata. Preserve them unless a documented consumer requires a transformed copy. Do not silently replace the canonical output with a lossy conversion.

## Validate and retain an SBOM

Before use:

1. verify the file is non-empty and parses in its serialization;
2. confirm the top-level format/spec version and generator identity;
3. bind it to the intended subject digest or commit;
4. validate against the appropriate CycloneDX or SPDX schema/tooling when required;
5. inspect component identifiers, versions, PURLs/CPEs, relationships, and root component;
6. record warnings and unsupported ecosystems from the generation log;
7. compute and retain a SHA-256 digest;
8. store it with access control, retention, and confidentiality appropriate to the package inventory.

An SBOM can expose internal package names, repository structure, image provenance, and vulnerable components. Do not publish it by default.

## Scan an existing SBOM

Use the SBOM target to reassess represented components against current Trivy data:

```bash
trivy sbom --format json --output sbom-scan.json /absolute/sbom.cdx.json
```

Before interpreting results:

- hash and identify the input SBOM;
- record its original generator and subject;
- verify that Trivy recognizes the format;
- retain parse and unsupported-field warnings;
- record the current vulnerability database metadata;
- state that results cannot exceed the input SBOM's completeness.

Rescanning an SBOM is useful for changing vulnerability intelligence, but it does not discover components omitted by the original generator.

## Attest and verify

Trivy documentation describes wrapping SBOMs in in-toto attestations and using Cosign-related workflows. Signing or publishing may upload material to an OCI registry or transparency service and is therefore a state-changing external action. Obtain explicit authorization for the identity, subject, destination, visibility, and keyless/key-backed signing method before performing it.

Verification must enforce a policy, not merely report that a cryptographic signature exists. Check:

- expected subject name and immutable digest;
- expected predicate type and SBOM format;
- signer identity or approved public key;
- OIDC issuer and certificate constraints for keyless signing;
- transparency-log inclusion/integrated time when policy requires it;
- signature/provenance verification result;
- timestamp and validity/revocation conditions;
- that the SBOM hash/content matches the attested predicate.

Scanning an attestation's payload is not equivalent to verifying its signer or subject binding. Verify first, then scan the extracted/verified predicate according to current official guidance.

## Use VEX safely

The official Trivy VEX documentation described the feature as experimental at the verification date. VEX inputs can come from repositories, local files, OCI attestations, or documents referenced by an SBOM; precedence can matter when multiple sources are enabled.

Before applying VEX, validate:

| Check | Requirement |
|---|---|
| Syntax | Supported VEX format and schema parse successfully |
| Product | Product/component identifier matches the exact target or SBOM component |
| Vulnerability | Identifier matches a reported vulnerability |
| Authority | Issuer is authorized to make statements for the product |
| Status | Supported status with required justification/impact statement |
| Freshness | Creation/update time and product version are current |
| Integrity | Signature, provenance, digest, and source verified where available |
| Scope | No unintended products, versions, or components are covered |
| Evidence | Pre-VEX and post-VEX result counts and document hash retained |

A `not_affected` status is a product assertion, not a general claim that the CVE is harmless. Reject mismatched, stale, unauthoritative, unverified when verification is required, or overly broad statements. Keep the underlying finding and VEX decision trace in the evidence bundle.

## Compliance reports

Trivy includes built-in and custom compliance-report capabilities for supported targets. Available profile identifiers, target compatibility, control content, and maturity can change. Discover them from the current official documentation and installed command rather than freezing an old list:

```bash
trivy <target-command> --help
```

Before running a profile:

1. identify the exact profile ID, title, source benchmark, version, and Trivy release;
2. confirm the target type and environment match the profile;
3. record which checks/controls are implemented, not implemented, skipped, or not applicable;
4. preserve both a machine-readable full report and a human summary;
5. map technical checks to the organization's control owners separately;
6. state that results are evidence, not certification or legal/regulatory advice.

Representative shape—verify all flags and the profile ID first:

```bash
trivy <supported-target-command> --compliance <current-profile-id> \
  --report all --format json --output compliance.json <target>
```

A pass can still be incomplete when permissions, unsupported resources, or collection settings prevent evaluation. A failed check may require contextual validation rather than blind remediation.

## Custom compliance specifications

Treat a custom specification as governed policy code. Use the schema and examples from the **installed release's** current documentation. Do not rely on copied field names or control IDs without validation.

Required lifecycle:

1. define scope, benchmark source/version, target platform, owners, and approval;
2. map each control to current Trivy check IDs and document gaps;
3. validate YAML/schema with the installed Trivy release;
4. add positive, negative, and not-applicable test fixtures;
5. pin/hash the spec and any custom checks/data;
6. review changes independently;
7. run on a non-production fixture before a live target;
8. version the evidence and record superseded controls;
9. set a periodic source/check refresh date.

Do not label an internally assembled profile as an official CIS, NIST, NSA/CISA, vendor, or regulatory certification unless the applicable owner authorizes that claim.

## Required output record

```yaml
supply_chain_evidence:
  target:
    type: "fs|repo|image|vm|k8s|sbom"
    immutable_identity: "commit, digest, or sha256"
  trivy:
    version: "runtime value"
    immutable_identity: "executable hash, image digest, or action SHA"
  sbom:
    format: "CycloneDX or SPDX serialization"
    spec_version: "parsed value"
    sha256: "digest"
    validation: "tool/schema and result"
  attestation:
    subject_digest: "expected digest"
    predicate_type: "expected type"
    signer_policy: "identity/key and issuer constraints"
    verification: "pass|fail|not-performed"
  vex:
    sources: []
    document_hashes: []
    pre_vex_findings: 0
    post_vex_findings: 0
    validation: "result and limitations"
  compliance:
    profile_id: "runtime-discovered ID"
    source_version: "benchmark/profile version"
    evaluated: 0
    passed: 0
    failed: 0
    skipped_or_unknown: 0
    limitations: []
```

## Sources

- [Trivy SBOM generation and discovery](https://trivy.dev/docs/latest/supply-chain/sbom/)
- [Trivy SBOM attestations](https://trivy.dev/docs/latest/supply-chain/attestation/sbom/)
- [Trivy VEX overview](https://trivy.dev/docs/latest/supply-chain/vex/)
- [Trivy SBOM target](https://trivy.dev/docs/latest/target/sbom/)
- [Trivy built-in compliance](https://trivy.dev/docs/latest/compliance/)
- [Trivy custom compliance](https://trivy.dev/docs/latest/compliance/custom/)
- [CycloneDX specifications](https://cyclonedx.org/specification/overview/)
- [SPDX specifications](https://spdx.dev/specifications/)
- [Sigstore Cosign verification](https://docs.sigstore.dev/cosign/verifying/verify/)

Recheck current Trivy output formats, profile IDs, VEX status, and attestation procedures before execution.
