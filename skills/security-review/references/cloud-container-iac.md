# Cloud, Container, and IaC Security Review

**Verified against upstream:** 2026-08-07

## Purpose and Boundaries

This reference governs the line-by-line security review of cloud infrastructure, containerized workloads, and Infrastructure as Code (IaC) definitions. It provides deterministic, evidence-driven checks for cloud IAM, network exposure, encryption, workload identity, serverless permissions, storage exposure, secrets management, IaC state files, container build/runtime configurations, Kubernetes Pod Security Standards, RBAC, admission policies, namespace multi-tenancy, network policies, service mesh, image provenance, backup/restore, drift, and cross-account trust.

This is defensive code-review guidance, not an exploitation manual. It does not guarantee the absence of vulnerabilities or certify compliance. Never instruct the agent to execute target code, upload proprietary material, expose secrets, or actively test production without explicit authorization. The primary goal is to identify misconfigurations and security weaknesses before they are deployed to production environments, ensuring that all infrastructure definitions adhere to established security best practices and organizational policies.

## Table of Contents

1. [Threat Assumptions](#threat-assumptions)
2. [Review Inputs](#review-inputs)
3. [Deterministic Review Procedure](#deterministic-review-procedure)
4. [Cloud and IaC Security Patterns](#cloud-and-iac-security-patterns)
5. [Container and Kubernetes Security Patterns](#container-and-kubernetes-security-patterns)
6. [False-Positive Controls and Validation](#false-positive-controls-and-validation)
7. [Finding Evidence Requirements](#finding-evidence-requirements)
8. [Stop and Escalation Rules](#stop-and-escalation-rules)
9. [Additional Context](#additional-context)
10. [References](#references)

## Threat Assumptions

The review operates under the assumption that the infrastructure is targeted by an active adversary capable of exploiting misconfigurations, exposed secrets, and overly permissive access controls. We assume that cloud metadata services are reachable and potentially vulnerable to Server-Side Request Forgery (SSRF) attacks, which could allow attackers to extract temporary credentials. Container images may contain known vulnerabilities, embedded secrets, or malicious payloads introduced through compromised supply chains.

Furthermore, IaC state files may expose sensitive information, such as database passwords or API keys, if not properly secured with encryption and strict access controls. Workloads running within the environment may attempt to escalate privileges or access unauthorized resources, necessitating robust isolation mechanisms. Network boundaries are considered porous, requiring the implementation of zero-trust principles and micro-segmentation to limit lateral movement in the event of a breach.

Adversaries are assumed to have access to public repositories and may leverage automated tools to scan for exposed credentials or misconfigured infrastructure. They may also attempt to exploit vulnerabilities in third-party dependencies or container base images. Therefore, the review must account for both internal and external threat vectors, ensuring that defense-in-depth strategies are effectively implemented across all layers of the infrastructure.

## Review Inputs

The agent requires specific inputs to perform the review effectively. These include IaC definitions such as Terraform (`.tf`), CloudFormation (`.yaml` or `.json`), or Pulumi scripts, which define the desired state of the infrastructure. Container build files, like Dockerfiles or Containerfiles, are necessary for evaluating image security, including base image selection and installed packages.

Kubernetes manifests, encompassing Deployments, Pods, Role-Based Access Control (RBAC) configurations, and NetworkPolicies, must be provided to assess cluster-level security. Cloud provider configuration files and Identity and Access Management (IAM) policies are required to evaluate access controls and resource permissions. Finally, application source code interacting with cloud services should be included to identify potential integration vulnerabilities, such as hardcoded credentials or insecure API usage.

In addition to these primary inputs, the agent may also require access to organizational security policies, compliance frameworks, and threat intelligence feeds to contextualize its findings. This supplementary information helps the agent prioritize vulnerabilities based on their potential impact and relevance to the specific environment being reviewed.

## Deterministic Review Procedure

The review must follow a systematic, line-by-line approach to ensure comprehensive coverage and minimize the risk of overlooking critical vulnerabilities.

First, identify all cloud resources, containers, and IaC definitions to create a detailed inventory and threat model. This involves mapping data flows, identifying trust boundaries, and understanding the interactions between different components.

Next, review all IAM policies, roles, and workload identities for adherence to the principle of least privilege. Ensure that no wildcard (`*`) permissions are granted unnecessarily and that access is restricted to the minimum required for the workload to function.

Analyze network configurations, security groups, and Kubernetes NetworkPolicies to verify that only required ports and protocols are exposed. Ensure that internal services are not accessible from the public internet and that communication between microservices is explicitly authorized.

Check for encryption at rest and in transit across all storage and communication channels. Ensure secrets are not hardcoded in IaC, container images, or application code, and verify that secure secret management practices, such as using AWS Secrets Manager or HashiCorp Vault, are implemented.

Evaluate container build and runtime configurations against Kubernetes Pod Security Standards and CIS Benchmarks. This includes checking for privileged containers, root user execution, and unnecessary capabilities.

Finally, review IaC state file storage and access controls, checking for mechanisms to detect and remediate configuration drift. Ensure that state files are encrypted and access is restricted to authorized personnel and CI/CD pipelines.

## Cloud and IaC Security Patterns

| Area | Normative Requirement | Anti-Pattern | Pattern |
|---|---|---|---|
| **Cloud IAM and Resource Policies** | Apply the principle of least privilege to all IAM roles and resource policies [1]. | Using overly permissive roles (e.g., `AdministratorAccess`) or wildcard actions (`s3:*`) for application workloads. | Define granular permissions scoped to specific resources and actions required by the workload. |
| **Network Exposure and Metadata Service Abuse** | Restrict network access to cloud resources and protect metadata services from SSRF attacks [2]. | Exposing databases or storage buckets directly to the internet. Using IMDSv1 without requiring session tokens. | Place resources in private subnets, use VPC endpoints, and enforce IMDSv2 (or equivalent) for metadata access. |
| **Encryption and Key Ownership** | Encrypt sensitive data at rest and in transit using customer-managed keys where appropriate [3]. | Storing sensitive data in plaintext or relying solely on default provider-managed keys for highly sensitive workloads. | Use KMS/HSM services to manage encryption keys and enforce TLS for all network communications. |
| **Serverless and Event Permissions** | Scope serverless function permissions to the specific events and resources they need to access [1]. | Granting a Lambda function broad access to all S3 buckets or DynamoDB tables. | Use event-specific IAM roles and resource-based policies to restrict access. |
| **Storage and Database Exposure** | Ensure storage buckets and databases are not publicly accessible unless explicitly required and authorized [3]. | Misconfiguring S3 bucket ACLs or database security groups to allow public read/write access. | Enable block public access settings and use private endpoints for database connections. |
| **IaC State and Plans** | Secure IaC state files and plans, as they may contain sensitive information and secrets [1]. | Storing Terraform state files in public or unencrypted S3 buckets. Committing state files to version control. | Use remote state backends with encryption, access controls, and state locking enabled. |
| **Cross-Account Trust** | Restrict cross-account trust relationships to authorized entities and enforce strict conditions [1]. | Allowing any account to assume a role or lacking external ID validation for third-party access. | Use explicit account IDs and require an ExternalId for all third-party cross-account role assumptions. |
| **Backup and Restore** | Implement automated backup and restore procedures for critical data and infrastructure [3]. | Relying on manual backups or failing to test restore procedures regularly. | Use cloud-native backup services with immutable storage and conduct periodic restore drills. |

## Container and Kubernetes Security Patterns

| Area | Normative Requirement | Anti-Pattern | Pattern |
|---|---|---|---|
| **Container Build and Runtime** | Build minimal container images and run them with the least privileges possible [4]. | Running containers as the `root` user. Including unnecessary tools (e.g., `curl`, `ssh`) in production images. | Use distroless or scratch images, specify a non-root user in the Dockerfile, and drop all unnecessary capabilities. |
| **Kubernetes Pod Security Standards** | Enforce the Baseline or Restricted Pod Security Standards to prevent privilege escalation and host access [5]. | Allowing privileged containers, host network access, or host path volumes. | Apply Pod Security Admission controllers to enforce the Restricted profile across all application namespaces. |
| **RBAC and Admission Policy** | Implement granular Role-Based Access Control (RBAC) and use admission controllers to enforce security policies [6]. | Granting `cluster-admin` privileges to service accounts or using default service accounts for workloads. | Create specific Roles and RoleBindings for each workload and use ValidatingAdmissionWebhooks to enforce organizational policies. |
| **Namespace Multi-Tenancy and Network Policies** | Isolate workloads using namespaces and restrict inter-pod communication using NetworkPolicies [6]. | Running all workloads in the `default` namespace without network segmentation. | Define default-deny NetworkPolicies and explicitly allow required traffic between specific pods and namespaces. |
| **Service Mesh and Image Provenance** | Use a service mesh for mutual TLS (mTLS) and verify the provenance and integrity of container images [4]. | Allowing unencrypted traffic between microservices or deploying unsigned/unverified images. | Enforce mTLS via a service mesh (e.g., Istio) and use admission controllers to verify image signatures (e.g., Sigstore) before deployment. |
| **Workload Identity** | Assign unique identities to workloads and avoid sharing credentials across services [2]. | Using long-lived static credentials or sharing a single service account across multiple deployments. | Use workload identity federation (e.g., IAM Roles for Service Accounts) to provide short-lived, scoped credentials. |

## False-Positive Controls and Validation

To minimize false positives, the agent must verify the context of the finding. For example, a permissive IAM policy might be acceptable in a dedicated sandbox environment but not in production. The agent should analyze the environment tags or naming conventions to determine the appropriate security posture.

Check for compensating controls, such as a publicly accessible storage bucket intended for hosting static website assets. In such cases, the bucket should be configured for read-only access, and sensitive data should not be present.

Validate findings against the specific cloud provider's documentation and best practices. Cloud providers frequently update their services and security recommendations, so the agent must ensure that its checks align with the latest guidance.

Prefer non-executing, local validation of declarative policy and syntax. Provider plans, policy simulators, cluster queries, role-assumption attempts, scanners, or any action that contacts a cloud account require explicit authorization for the exact account, identity, environment, and side effects. A provider-labelled “dry run” is not automatically safe: it may require credentials, disclose metadata, consume quota, write logs, or omit authorization semantics. When runtime confirmation is not authorized, preserve the finding as a candidate or confirmed static misconfiguration according to the available evidence and record the missing context as an uncertainty.

Furthermore, the agent should cross-reference findings with known vulnerability databases, such as the CISA Known Exploited Vulnerabilities (KEV) catalog or the Exploit Prediction Scoring System (EPSS), to prioritize remediation efforts based on real-world threat intelligence.

## Canonical finding evidence requirements

Every report must conform to `../templates/finding.schema.json`. The report root must contain `schema_version`, `review`, `findings`, `conflicts`, and `unknowns`. Every finding must contain `id`, `title`, `status`, `asset`, `locations`, `evidence`, `reasoning`, `preconditions`, `impact`, `taxonomy`, `confidence`, `remediation`, `validation`, `residual_risk`, and `conflicts`. Add optional `cvss_v4` or `live_context` only when supported by the finding; omission is valid. The `conflicts` array contains only top-level conflict IDs. `accepted_risk` is required when `status` is `accepted-risk` and forbidden for every other status; it contains `owner`, `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at`. In `asset`, `locations`, and `reasoning.narrative`, identify the affected account, cluster, namespace, workload, resource, image, module, or state artifact and distinguish policy reasoning from demonstrated runtime behavior.

For cloud and IaC findings, distinguish declared configuration, generated plan, currently observed runtime state, and organizational policy. Never claim that a repository declaration is deployed without evidence. Record provider, region, account or tenant boundary, inheritance, defaults, effective permissions, and source freshness when those facts affect the conclusion. A corrected snippet may be included in the remediation narrative when it is accurate and provider-current, but it is not a substitute for the canonical fields and must not expose account identifiers or secrets.

Unknown deployment state belongs in `confidence.uncertainties`. Put intentionally excluded resources and reasons in `review.scope.excluded`, and reconcile all inventoried resources through `review.coverage`. Contradictory policy or runtime observations belong in top-level conflict objects referenced by affected findings. Scanner output is tool evidence only and must be normalized, deduplicated, and reasoned about before final reporting.

## Stop and Escalation Rules

Stop the affected action and escalate to the coordinator or user-designated Phase 0 contact when obfuscated or generated material prevents safe analysis, a secret or regulated record appears, scope expansion is required, required context is unavailable, or validation would contact or mutate a real cloud, registry, cluster, CI, or production system without exact authorization. Record the resulting unknown, coverage gap, or incident signal rather than guessing.

A severe static finding does not authorize outreach to an assumed security team, credential use, secret validation, account access, or incident-response actions. Preserve redacted evidence, follow the user’s established notification path, and continue independent authorized read-only dimensions only when doing so remains safe.

## Additional Context

The cloud and container security landscape is constantly evolving, with new threats and vulnerabilities emerging regularly. It is crucial for security teams to stay informed about the latest developments and update their review procedures accordingly. This reference document serves as a foundational guide, but it should be supplemented with continuous learning and adaptation to address the dynamic nature of cloud-native environments.

Organizations should also consider implementing automated security scanning tools as part of their CI/CD pipelines to detect misconfigurations and vulnerabilities early in the development lifecycle. These tools can complement the manual review process outlined in this document, providing an additional layer of defense against potential threats.

Furthermore, fostering a culture of security awareness among developers and operations teams is essential for maintaining a robust security posture. Regular training and knowledge-sharing sessions can help ensure that everyone involved in the deployment and management of cloud infrastructure understands their role in protecting the organization's assets.

By combining deterministic review procedures, automated scanning tools, and a strong security culture, organizations can significantly reduce their risk exposure and build resilient, secure cloud-native applications.

The integration of security into the development lifecycle, often referred to as DevSecOps, is critical for modern software delivery. This approach ensures that security is not an afterthought but a fundamental component of the development process. By embedding security checks into the CI/CD pipeline, organizations can catch vulnerabilities early, reducing the cost and effort required to remediate them later.

Moreover, the use of Infrastructure as Code (IaC) allows organizations to define and manage their infrastructure in a declarative manner. This not only improves consistency and repeatability but also enables security teams to review and audit infrastructure configurations before they are deployed. By treating infrastructure as code, organizations can apply the same security practices used for application code, such as version control, peer review, and automated testing.

In conclusion, securing cloud and container environments requires a comprehensive and proactive approach. By adhering to the guidelines and best practices outlined in this reference document, organizations can build a strong security foundation and protect their critical assets from emerging threats.

Continuous monitoring and auditing of cloud environments are also vital to detect and respond to security incidents in real-time. Organizations should leverage cloud-native security tools, such as AWS Security Hub, Azure Security Center, or Google Cloud Security Command Center, to gain visibility into their security posture and identify potential vulnerabilities.

Additionally, implementing a robust incident response plan is essential for minimizing the impact of security breaches. This plan should outline the steps to be taken in the event of an incident, including containment, eradication, and recovery procedures. Regular tabletop exercises and simulations can help ensure that the incident response team is prepared to handle real-world scenarios effectively.

By adopting a holistic approach to cloud and container security, organizations can mitigate risks, protect sensitive data, and maintain the trust of their customers and stakeholders.

The importance of securing the software supply chain cannot be overstated. Attackers increasingly target the tools and processes used to build and deploy software, seeking to introduce vulnerabilities or malicious code before the software even reaches production. To mitigate this risk, organizations must implement strict controls over their build environments, verify the integrity of third-party dependencies, and use code signing to ensure the authenticity of their software artifacts.

Furthermore, the adoption of zero-trust architecture principles is becoming increasingly necessary in modern cloud environments. Zero trust assumes that no user or device should be trusted by default, regardless of their location on the network. By implementing strict access controls, continuous authentication, and micro-segmentation, organizations can significantly reduce the attack surface and limit the potential impact of a breach.

In summary, securing cloud and container environments is a complex and ongoing challenge that requires a multi-faceted approach. By combining deterministic review procedures, automated scanning tools, a strong security culture, and a commitment to continuous improvement, organizations can build resilient and secure cloud-native applications that protect their critical assets and maintain the trust of their customers.

## Authoritative references

The complete source-to-check and freshness matrix is `sources.md`. CIS Controls provide a cross-domain governance baseline; product-specific CIS Benchmarks must be selected and refreshed for the exact provider, service, operating system, container runtime, or Kubernetes release under review rather than inferred from the Controls document.

[1] CIS Critical Security Controls. Center for Internet Security. https://www.cisecurity.org/controls
[2] NIST SP 800-207 Zero Trust Architecture. National Institute of Standards and Technology. https://csrc.nist.gov/pubs/sp/800/207/final
[3] Cloud Security Alliance Cloud Controls Matrix. Cloud Security Alliance. https://cloudsecurityalliance.org/research/cloud-controls-matrix
[4] NIST SP 800-190 Application Container Security Guide. National Institute of Standards and Technology. https://www.nist.gov/publications/application-container-security-guide
[5] Kubernetes Pod Security Standards. Kubernetes. https://kubernetes.io/docs/concepts/security/pod-security-standards/
[6] Kubernetes Hardening Guide. NSA and CISA. https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF
[7] NIST SP 800-204 Security Strategies for Microservices-based Application Systems. National Institute of Standards and Technology. https://csrc.nist.gov/pubs/sp/800/204/final
