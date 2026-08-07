# Supply Chain and Build Security Review Reference

**Verified against upstream:** 2026-08-07

## Purpose and Boundaries

This reference document provides deterministic, evidence-driven guidance for reviewing software supply chain and build configurations. It is designed to support a bounded specialist agent in a parallel security-review protocol. This is defensive code-review guidance, not an exploitation manual. It does not guarantee the absence of vulnerabilities or certify compliance. The agent must not execute target code, upload proprietary material, expose secrets, or actively test production without explicit authorization. Scanner output is considered evidence, not proof.

## Table of Contents

1. [Threat Assumptions](#threat-assumptions)
2. [Review Inputs](#review-inputs)
3. [Deterministic Review Procedure](#deterministic-review-procedure)
4. [Patterns and Anti-Patterns](#patterns-and-anti-patterns)
5. [False-Positive Controls](#false-positive-controls)
6. [Validation and Regression Checks](#validation-and-regression-checks)
7. [Finding Evidence Requirements](#finding-evidence-requirements)
8. [Stop and Escalation Rules](#stop-and-escalation-rules)
9. [References](#references)

## Threat Assumptions

Modern software development relies heavily on third-party components and automated build pipelines, creating a broad attack surface. Attackers frequently target upstream dependencies to inject malicious code, exploiting techniques such as typosquatting and dependency confusion. Malicious maintainers or compromised accounts can introduce backdoors into widely used open-source packages, affecting thousands of downstream users.

Build environments themselves are prime targets. If compromised, attackers can alter artifacts or inject malicious code during the build process, bypassing source code controls. They may also attempt to bypass or manipulate provenance and attestation mechanisms to pass off malicious artifacts as legitimate. Furthermore, CI/CD pipelines often possess excessive permissions, allowing unauthorized modifications or the exfiltration of sensitive secrets. The emerging use of AI/ML models introduces additional risks, as model and data supply chains can be poisoned or manipulated to produce incorrect or harmful outputs. Finally, build infrastructure may lack sufficient isolation, allowing lateral movement or cross-tenant contamination.

## Review Inputs

The review process requires access to specific configuration files and manifests that define the supply chain and build process. These inputs provide the necessary context for identifying vulnerabilities and misconfigurations.

| Input Category | Examples | Description |
| :--- | :--- | :--- |
| **Dependency Manifests** | `package.json`, `requirements.txt`, `go.mod`, `pom.xml` | Define the direct and transitive dependencies required by the application. |
| **Lockfiles** | `package-lock.json`, `Pipfile.lock`, `go.sum` | Ensure deterministic dependency resolution by pinning exact versions and hashes. |
| **CI/CD Configurations** | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` | Define the automated build, test, and deployment pipelines. |
| **Build Scripts** | Makefiles, custom orchestration scripts | Detail the specific commands and steps executed during the build process. |
| **IaC Manifests** | Dockerfiles, Kubernetes manifests, Terraform | Define the infrastructure and environments used for building and running the application. |
| **SBOMs and VEX** | SPDX, CycloneDX documents | Provide a comprehensive inventory of components and their vulnerability status. |
| **Provenance Records** | SLSA provenance, in-toto attestations | Cryptographically verify the origin and build process of artifacts. |
| **Registry Configurations** | `.npmrc`, `pip.conf`, `settings.xml` | Configure access to public and private package registries. |

## Deterministic Review Procedure

### 1. Dependency Management and Registry Trust

The foundation of supply chain security lies in robust dependency management. Reviewers must verify that lockfiles are present, committed to version control, and strictly enforced during the build process using commands like `npm ci` or `pip install --require-hashes`. This ensures reproducible builds and prevents unexpected dependency updates.

Dependency confusion is a critical risk. Reviewers must check for private packages that lack explicit registry scoping or configuration preventing fallback to public registries. Internal package names should be claimed on public registries, or registry routing must be strictly configured. Typosquatting is another common attack vector; dependencies must be inspected for names that closely resemble popular packages but are not the official ones, looking for common misspellings or variations.

Lifecycle scripts, such as `preinstall`, `install`, and `postinstall`, pose a significant risk as they execute arbitrary code during dependency installation. These scripts must be reviewed for suspicious or unauthorized actions. If possible, lifecycle scripts should be disabled globally. Finally, reviewers must monitor for malicious maintainers by checking for sudden changes in maintainership, suspicious commits in critical dependencies, or packages that have been deprecated or abandoned.

### 2. Build Isolation and Reproducibility

Build environments must be secure and deterministic. Reviewers must ensure builds are executed in ephemeral, isolated environments, such as containers or virtual machines, without unnecessary network access. Build environments should be torn down and recreated for each build to prevent contamination.

Reproducibility is essential for verifying the integrity of the build process. Reviewers must verify that builds are deterministic and reproducible from the same source code and dependencies. This involves checking for the use of fixed timestamps, sorted file lists, and consistent build toolchains. Furthermore, build environments must have restricted outbound network access, allowing connections only to approved package registries and necessary services.

### 3. CI/CD Pipeline Security

CI/CD pipelines often hold the keys to the kingdom. Reviewers must audit pipeline permissions, ensuring the principle of least privilege is applied to service accounts and tokens. Tokens must have limited scopes and short expiration times.

Action pinning is a crucial defense against upstream compromises. Reviewers must verify that third-party CI/CD actions or plugins are pinned to specific commit SHAs rather than mutable tags like `v1` or `latest`. This prevents upstream changes from silently altering the build process. Additionally, secrets must never be hardcoded in pipeline configurations or build scripts. Reviewers must verify that secrets are injected securely using a dedicated secret management solution and masked in logs.

### 4. Provenance, Attestation, and Verification

Cryptographic verification provides assurance of artifact integrity. Reviewers must check for the generation and verification of build provenance, such as using the SLSA framework. Provenance records must include details about the source code, dependencies, and build environment.

Downloaded artifacts and dependencies must be verified against cryptographic signatures using tools like Sigstore or in-toto. Reviewers must ensure that signature verification is enforced before execution or deployment. Furthermore, the generation and consumption of SBOMs (SPDX, CycloneDX) and VEX documents must be verified to track components and vulnerabilities. SBOMs should be generated at build time and stored securely.

### 5. AI/ML Model and Data Supply Chains

The integration of AI/ML models introduces novel supply chain risks. Reviewers must verify the source and integrity of AI/ML models and datasets. Models must be downloaded from trusted sources and verified using cryptographic hashes or signatures.

Data poisoning is a significant threat to AI/ML systems. Reviewers must check for controls against data poisoning and manipulation in training pipelines, ensuring that training data is validated and sanitized before use. Finally, models must be serialized using secure formats, such as Safetensors, rather than formats that allow arbitrary code execution, such as Pickle.

### 6. Incident Containment

Despite preventative measures, compromises may occur. Reviewers must evaluate the potential impact of a compromised dependency or build step and ensure adequate containment measures are in place. Build environments must be isolated from production environments to limit the blast radius.

Continuous monitoring is essential. Reviewers must ensure that dependencies and container images are scanned for known vulnerabilities regularly, and that critical vulnerabilities are addressed promptly.

## Patterns and Anti-Patterns

| Category | Pattern (Secure) | Anti-Pattern (Insecure) |
| :--- | :--- | :--- |
| **Dependency Resolution** | Explicitly scoping private packages to a private registry (e.g., `@myorg/private-pkg`). | Relying on default registry resolution for private packages, risking dependency confusion. |
| **Action Pinning** | Resolve the intended current release from the official repository, review its provenance and change history, then pin the workflow to that immutable full commit SHA while retaining the reviewed release in a comment. | Using mutable tags or copying an old SHA from documentation without verifying the action, version, commit, and input contract at review time. |
| **Build Environment** | Running builds in isolated, ephemeral containers with restricted network access. | Running builds on persistent, shared runners with broad network access and excessive permissions. |
| **Artifact Verification** | Verifying signatures of downloaded binaries using Sigstore or GPG before execution. | Downloading and executing binaries directly from the internet without verification (e.g., `curl \| bash`). |
| **Lockfiles** | Committing lockfiles to version control and using strict installation commands (e.g., `npm ci`). | Ignoring lockfiles or using commands that update dependencies implicitly (e.g., `npm install`). |
| **Secrets** | Injecting secrets securely using a secret manager and masking them in logs. | Hardcoding secrets in build scripts or printing them to standard output. |

## False-Positive Controls

Reviewers must exercise judgment to minimize false positives. It is important to differentiate between development/test dependencies and production dependencies. Vulnerabilities in development dependencies may have a lower risk profile, although they can still be exploited during the build process.

When a dependency vulnerability is reported, assess whether the component is present, used in the affected form, reachable, exposed, and covered by a trustworthy VEX statement or equivalent contextual evidence. A scanner result may be recorded as a `candidate` without a second evidence source when its provenance, freshness, artifact identity, target scope, and detection semantics are clear; confirmation and prioritization must state what was and was not corroborated. Do not treat missing reachability evidence as proof of non-exploitability, and do not treat a VEX assertion as authoritative unless its issuer, product identity, status, justification, timestamp, and signature or distribution trust are appropriate.

## Validation and Regression Checks

Security is an ongoing process. Reviewers must ensure that updates to dependencies or build configurations do not introduce regressions or break reproducible builds. CI/CD pipeline changes must be validated to ensure they do not inadvertently grant excessive permissions or expose secrets.

The list of approved package registries and trusted sources must be regularly reviewed and updated. Reviewers must also monitor for new vulnerabilities and emerging threats in the software supply chain to ensure defenses remain effective.

## Finding evidence requirements

Emit reports through [`../templates/finding.schema.json`](../templates/finding.schema.json). The report root must contain `schema_version`, `review`, `findings`, `conflicts`, and `unknowns`. Every finding must contain `id`, `title`, `status`, `asset`, `locations`, `evidence`, `reasoning`, `preconditions`, `impact`, `taxonomy`, `confidence`, `remediation`, `validation`, `residual_risk`, and `conflicts`. Add optional `cvss_v4` or `live_context` only when supported by the finding; omission is valid. The `conflicts` array contains only top-level conflict IDs. `accepted_risk` is required when `status` is `accepted-risk` and forbidden for every other status; it contains `owner`, `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at`. For dependencies and build artifacts, record ecosystem, package or artifact name, version or digest, source, lockfile or manifest path, and the relevant advisory, attestation, SBOM, signature, or VEX identity when known.

Distinguish verified absence, not observed, not assessed, and unknown. Preserve unresolved version, reachability, provenance, build-system, runner, registry, or deployment context as uncertainty. When specialists disagree about artifact identity, exploitability, signature meaning, or workflow exposure, create a conflict object, link the finding IDs, preserve both evidence paths, and use `disputed` while material conflict remains.

## Stop and escalation rules

Stop the affected path when it would require executing untrusted code, installing dependencies, pulling or running an image, contacting registries or CI systems, uploading proprietary material, accessing production, using a credential, changing a workflow, or publishing an artifact without explicit authorization. Suspected malicious dependencies, compromised build infrastructure, unexpected release signatures, exposed high-privilege CI credentials, or active exploitation also trigger a stop for that path.

Minimize and redact evidence, preserve safe metadata, and notify the coordinator or the Phase 0 user-designated contact. Do not assume a security team exists. Do not revoke credentials, quarantine runners, contact a maintainer, delete artifacts, or modify pipelines without authorization. Independent safe, read-only review may continue.

## References

[1] [OWASP Top 10:2025 - A03 Software Supply Chain Failures](https://owasp.org/Top10/2025/en/)
[2] [CISA Software Bill of Materials (SBOM) Guidance](https://www.cisa.gov/sbom)
[3] [Supply-chain Levels for Software Artifacts (SLSA)](https://slsa.dev/spec/)
[4] [Sigstore Documentation](https://docs.sigstore.dev/)
[5] [in-toto Attestation Framework](https://github.com/in-toto/attestation)
[6] [System Package Data Exchange (SPDX) Specification](https://spdx.dev/specifications/)
[7] [CycloneDX Bill of Materials Specification](https://cyclonedx.org/)
[8] [OpenSSF Scorecard](https://scorecard.dev/)
[9] [NIST SP 800-218 Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
[10] [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### Additional Context on Emerging Threats

The landscape of supply chain attacks is constantly evolving. Attackers are increasingly targeting the build infrastructure itself, seeking to compromise CI/CD runners or inject malicious code during the build process. This highlights the critical importance of build isolation and the principle of least privilege.

Furthermore, the rise of AI/ML models introduces new complexities. These models are often treated as black boxes, making it difficult to verify their integrity or detect malicious modifications. Securing the AI/ML supply chain requires a comprehensive approach that encompasses data provenance, model verification, and secure deployment practices.

### The Role of Automation

Automation plays a vital role in securing the software supply chain. Automated tools can continuously scan dependencies for vulnerabilities, verify signatures, and enforce security policies. However, automation must be implemented carefully to avoid introducing new risks. For example, automated dependency updates can inadvertently introduce malicious packages if not properly vetted.

Therefore, a balanced approach is required, combining automated scanning with manual review and robust security policies. This ensures that vulnerabilities are identified and addressed promptly while minimizing the risk of false positives and unintended consequences.

### Continuous Improvement

Supply chain security is not a one-time effort but an ongoing process of continuous improvement. Organizations must regularly review and update their security practices to adapt to emerging threats and evolving technologies. This includes staying informed about the latest vulnerabilities, participating in information-sharing communities, and conducting regular security assessments.

By adopting a proactive and comprehensive approach to supply chain security, organizations can significantly reduce their risk of compromise and ensure the integrity of their software products.
