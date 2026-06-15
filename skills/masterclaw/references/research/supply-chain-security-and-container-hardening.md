# Supply Chain Security and Container Hardening (2024-2026)

## 1. Introduction
The landscape of software supply chain security and container hardening has evolved significantly between 2024 and 2026. Driven by high-profile supply chain attacks and the increasing complexity of cloud-native environments, organizations and regulatory bodies have established rigorous frameworks and best practices. This document synthesizes findings from top academic institutions, engineering organizations, and authoritative industry sources to provide a comprehensive overview of the current state of supply chain security and container hardening.

## 2. Key Frameworks and Guidelines

### 2.1 NIST Secure Software Development Framework (SSDF)
The NIST Secure Software Development Framework (SSDF), specifically SP 800-218, provides a core set of high-level secure software development practices. In late 2025, NIST released Draft SSDF 1.2 for comment, further refining these practices [1] [3]. The framework emphasizes the integration of security throughout the software development life cycle (SDLC), aiming to reduce the number of vulnerabilities in released software and mitigate the potential impact of the exploitation of undetected or unaddressed vulnerabilities.

### 2.2 CISA and NSA Kubernetes Hardening Guidance
The Cybersecurity and Infrastructure Security Agency (CISA) and the National Security Agency (NSA) have continuously updated their Kubernetes Hardening Guidance. The guidance details threats to Kubernetes environments and provides secure configuration recommendations to minimize risk [7] [8]. Primary actions include scanning containers and Pods for vulnerabilities, using strong authentication and authorization, and implementing network segmentation.

### 2.3 Google SLSA Framework
Supply-chain Levels for Software Artifacts (SLSA) is an end-to-end framework for ensuring the integrity of software artifacts throughout the software supply chain [16] [20]. Developed by Google and now an OpenSSF project, SLSA provides a checklist of standards and controls to prevent tampering, improve integrity, and secure packages and infrastructure. The framework is divided into levels, allowing organizations to incrementally adopt security practices based on their risk profile and maturity.

## 3. Container Hardening Best Practices

### 3.1 Distroless Images
"Distroless" images contain only the application and its runtime dependencies, omitting package managers, shells, and other unnecessary programs [31]. By stripping out these components, distroless images significantly reduce the potential attack surface for vulnerabilities [36]. However, it is crucial to understand that distroless images are not a silver bullet; they must be combined with other security measures, such as vulnerability scanning and runtime protection [32].

### 3.2 Rootless Containers
Running containers as a non-root user (rootless containers) is a fundamental security practice. Rootless containers prevent privilege escalation attacks by ensuring that even if a container is compromised, the attacker does not gain root access to the host system [35]. This approach aligns with the principle of least privilege and is increasingly supported by container runtimes and orchestration platforms.

### 3.3 Seccomp Profiles, AppArmor, and SELinux
Low-level container hardening involves restricting the capabilities of containerized processes using Linux kernel features:
- **Seccomp (Secure Computing Mode):** Restricts the system calls (syscalls) a process can invoke, reducing the attack surface by preventing containers from executing potentially dangerous syscalls [37].
- **AppArmor and SELinux:** Mandatory Access Control (MAC) systems that enforce security policies on processes, restricting their access to files, network resources, and other system components [38] [40].

## 4. Supply Chain Security Mechanisms

### 4.4 Software Bill of Materials (SBOM)
A Software Bill of Materials (SBOM) is a formal, machine-readable inventory of software components and dependencies. CISA and other organizations have emphasized the importance of SBOMs for vulnerability management, component tracking, and supply chain security [26] [28]. By providing transparency into the software supply chain, SBOMs enable organizations to quickly identify and remediate vulnerabilities in third-party components.

### 4.5 Container Image Signing with Sigstore and Cosign
Ensuring the integrity and authenticity of container images is critical. Sigstore, an OpenSSF project, provides a suite of tools for code signing and transparency. Cosign, a key component of Sigstore, is used to sign OCI containers and other artifacts [23] [25]. By signing container images, organizations can verify that the images have not been tampered with and originate from a trusted source.

## 5. Vulnerability Management and Remediation Workflows
Effective vulnerability management in containerized environments requires a continuous and automated approach. Key practices include:
- **Continuous Scanning:** Scanning base OS templates, static container images, and running containers for vulnerabilities [42] [45].
- **Risk-Driven Remediation:** Prioritizing vulnerabilities based on their severity, exploitability, and the context of the application [44].
- **Automated Workflows:** Integrating vulnerability scanning and remediation into CI/CD pipelines to ensure that vulnerabilities are addressed early in the development process [43].

## 6. Latest Developments (2024-2026)
- **Increased Adoption of SLSA:** Organizations are increasingly adopting the SLSA framework to secure their software supply chains, driven by regulatory requirements and the growing threat landscape [17] [18].
- **Advancements in SBOM Tooling:** The ecosystem of tools for generating, analyzing, and managing SBOMs has matured significantly, enabling more effective vulnerability management [29].
- **Focus on Usability in Code Signing:** Research has highlighted the importance of usability in identity-based software signing tools like Sigstore, leading to improvements in the developer experience [30].

## 7. Production-Grade Implementation Guidance
- **Implement SLSA Level 3:** Aim for SLSA Level 3 compliance by generating provenance for all build artifacts and ensuring that the build process is isolated and ephemeral.
- **Enforce Image Signing:** Require all container images deployed to production to be signed using Cosign and verified by an admission controller (e.g., Kyverno or OPA Gatekeeper).
- **Use Distroless Base Images:** Standardize on distroless base images for all applications to minimize the attack surface.
- **Apply Default Security Profiles:** Enforce default Seccomp, AppArmor, or SELinux profiles for all containers running in Kubernetes clusters.
- **Automate Vulnerability Remediation:** Integrate vulnerability scanning into the CI/CD pipeline and establish automated workflows for patching and updating container images.

## References

### Academic Papers and Research
[1] M. Tamanna et al., "Analyzing Challenges in Deployment of the SLSA Framework for Software Supply Chain Security," arXiv preprint arXiv:2409.05014, 2024.
[2] S. U. Lee et al., "Software Security Mapping Framework: Operationalization of Security Requirements," arXiv preprint arXiv:2506.11051, 2025.
[3] M. A. Rahman et al., "S3C2 Summit 2025-09: Industry Secure Supply Chain Summit," arXiv preprint arXiv:2605.29226, 2026.
[4] "Why Johnny Adopts Identity-Based Software Signing: A Usability Case Study of Sigstore," USENIX Security Symposium, 2026.
[5] "Why Johnny Signs with Next-Generation Tools: A Usability Case Study of Sigstore," arXiv preprint arXiv:2503.00271, 2025.
[6] "A Longitudinal Study of Usability in Identity-Based Software Signing," arXiv preprint arXiv:2603.17133, 2026.
[7] "Secure Supply Chain Management in DevOps: Addressing Software Bill of Materials (SBOM) Risks," International Journal of Engineering Research and Technology, 2024.
[8] "A landscape study of open-source tools for software bill of materials (SBOM) and supply chain security," IEEE Symposium on Security and Privacy, 2025.
[9] M. O. Patwary et al., "Securing the Future: Enhancing Cybersecurity and Resilience in Digital and Software Supply Chains," IGI Global, 2026.
[10] A. Biswas et al., "Securing the Future: Enhancing Cybersecurity," AI-Driven Cybersecurity, 2026.
[11] S. Hamer et al., "S3C2 Summit 2025-07: Government Secure Supply Chain Summit," arXiv preprint arXiv:2605.29140, 2026.
[12] I. Eleweke, "Fortifying AI Infrastructure: Securing Code, Configuration, and Integrity in National Systems," ResearchGate, 2025.
[13] A. S. M. Hassan, "Network Design Based on EU CRA Requirements for Automated Stacking Cranes (ASC)," Aalto University, 2025.
[14] D. Rajesh and R. Balasubramanian, "Assessing cyber-physical security standards and metrics for next-generation autonomous vessels," Journal of Internet Services and Information Security, 2025.
[15] S. M. Makoshi, "In-Depth Analysis of Cloud Security-Significance, Service Providers, and NIST Standards," Authorea Preprints, 2025.
[16] "Secure Development Methodology for Full Stack Web Applications: Proof of the Methodology Applied to Vue. js, Spring Boot and MySQL," EBSCOhost, 2024.
[17] "Simplifying Cloud-Native Infrastructure Provisioning," Western University, 2024.
[18] "Despliegue de arquitectura de microservicios en Kubernetes: Sistema de integración y delivery continuo," Universidad Nacional de La Plata, 2024.
[19] "A container security survey: Exploits, attacks, and defenses," ACM Computing Surveys, 2024.
[20] "A Security Benchmarking Framework for Empirical Evaluation of Container Confinement," Carleton University, 2024.
[21] "Toward end-to-end verifiable security for confidential container deployments," University of Queensland, 2024.
[22] "Intelligent Security Automation: Standard Continuous Process from Scan to Remediation for Vulnerability Management," IEEE Xplore, 2024.
[23] "Container Vulnerability Management in Telecommunication Network," University of Helsinki, 2024.

### Authoritative Articles and Documentation
[24] NIST CSRC, "Secure Software Development Framework (SSDF)," https://csrc.nist.gov/projects/ssdf
[25] Cycode, "Emerging Software Supply Chain Security Best Practices," https://cycode.com/resources/google-slsa-nist-ssdf-best-practices/
[26] NIST CSRC, "Draft SSDF 1.2 Available for Comment," https://csrc.nist.gov/News/2025/draft-ssdf-version-1-2
[27] Anchore, "An Introduction to NIST's Secure Software Development Framework," https://anchore.com/blog/about-new-nist-ssdf/
[28] CISA, "NIST SP 800-218, Secure Software Development Framework V1.1," https://www.cisa.gov/resources-tools/resources/nist-sp-800-218-secure-software-development-framework-v11-recommendations-mitigating-risk-software
[29] ReversingLabs, "Software Supply Chain Security Report 2026: A guidance timeline," https://www.reversinglabs.com/blog/sscs-report-2026-guidance-timeline
[30] CISA, "Updated: Kubernetes Hardening Guide," https://www.cisa.gov/news-events/alerts/2022/03/15/updated-kubernetes-hardening-guide
[31] Kubernetes Blog, "A Closer Look at NSA/CISA Kubernetes Hardening Guidance," https://kubernetes.io/blog/2021/10/05/nsa-cisa-kubernetes-hardening-guidance/
[32] NSA, "NSA, CISA release Kubernetes Hardening Guidance," https://www.nsa.gov/Press-Room/News-Highlights/Article/Article/2716980/nsa-cisa-release-kubernetes-hardening-guidance/
[33] Rapid7, "ICS Supports the NSA/CISA Kubernetes Hardening Guide," https://www.rapid7.com/blog/post/2022/04/14/insightcloudsec-supports-the-recently-updated-nsa-cisa-kubernetes-hardening-guide/
[34] Anchore, "NIST SP 800-190: Overview & Compliance Checklist," https://anchore.com/compliance/nist/800-190/
[35] Red Hat, "Guide to NIST SP 800-190 compliance in container environments," https://www.redhat.com/en/resources/guide-nist-compliance-container-environments-detail
[36] Chainguard, "NIST Container Security Compliance Standards & Guidelines," https://www.chainguard.dev/unchained/understanding-nists-latest-updates-on-container-image-security
[37] SLSA, "SLSA • Supply-chain Levels for Software Artifacts," https://slsa.dev/
[38] Cycode, "Google SLSA Framework: Key Takeaways," https://cycode.com/blog/key-takeaways-from-google-slsa-cybersecurity-framework/
[39] Practical DevSecOps, "SLSA Framework Guide 2026 - Secure Your Software," https://www.practical-devsecops.com/slsa-framework-guide-software-supply-chain-security/
[40] Google Cloud Blog, "Google introduces SLSA framework," https://cloud.google.com/blog/products/application-development/google-introduces-slsa-framework
[41] Checkmarx, "SLSA Explained - Framework, Levels and Implementation," https://checkmarx.com/glossary/what-is-the-slsa-framework/
[42] Google Security Blog, "Introducing SLSA, an End-to-End Framework for Supply," https://security.googleblog.com/2021/06/introducing-slsa-end-to-end-framework.html
[43] Sigstore, "Signing Containers," https://docs.sigstore.dev/cosign/signing/signing_with_containers/
[44] OpenSSF, "Implementing Sigstore for Seamless Container Image Signing," https://openssf.org/blog/2024/02/16/scaling-up-supply-chain-security-implementing-sigstore-for-seamless-container-image-signing/
[45] GitHub, "sigstore/cosign: Code signing and transparency for containers and," https://github.com/sigstore/cosign
[46] Chainguard Academy, "How to Sign a Container with Cosign," https://edu.chainguard.dev/open-source/sigstore/cosign/how-to-sign-a-container-with-cosign/
[47] CISA, "Software Bill of Materials (SBOM)," https://www.cisa.gov/topics/information-communications-technology-supply-chain-security/sbom
[48] NSA, "NSA, CISA, and Others Release a Shared Vision of," https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/4292020/nsa-cisa-and-others-release-a-shared-vision-of-software-bill-of-materials-sbom/
[49] IBM, "What Is a Software Bill of Materials (SBOM)?," https://www.ibm.com/think/topics/sbom
[50] CMS, "New cybersecurity guidance from CISA for Software Bill," https://security.cms.gov/posts/new-cybersecurity-guidance-cisa-software-bill-materials-sbom
[51] GitHub, ""Distroless" Container Images," https://github.com/googlecontainertools/distroless
[52] Red Hat, "Why distroless containers aren't the security solution you," https://www.redhat.com/en/blog/why-distroless-containers-arent-security-solution-you-think-they-are
[53] BellSoft, "Distroless Docker Images: A Guide to Security, Size and," https://bell-sw.com/blog/distroless-containers-for-security-and-size/
[54] Docker, "Is Your Container Image Really Distroless?," https://www.docker.com/blog/is-your-container-image-really-distroless/
[55] Chainguard Academy, "Getting Started with Distroless Container Images," https://edu.chainguard.dev/chainguard/chainguard-images/about/getting-started-distroless/
[56] Medium, "Understanding Seccomp (and How It Compares to AppArmor) for," https://medium.com/@mughal.asim/understanding-seccomp-and-how-it-compares-to-apparmor-for-container-security-5317b3e9b1d6
[57] Datadog, "Container security fundamentals part 5: AppArmor and SELinux," https://securitylabs.datadoghq.com/articles/container-security-fundamentals-part-5/
[58] HardenedLinux, "Container Hardening Process," https://hardenedlinux.org/blog/2024-10-13-container-hardening-process/
[59] LinkedIn, "Kernel Hardening with App Armor and Seccomp: Must-know for the," https://www.linkedin.com/pulse/kernel-hardening-app-armor-seccomp-must-know-cks-exam-puru-tuladhar-li89f
[60] Anchore, "Container Vulnerability Management: Risks, Tips & Tools," https://anchore.com/container-security/container-vulnerability-management/
[61] Qualys, "Qualys & ServiceNow: Automating Risk-Driven Remediation for," https://blog.qualys.com/product-tech/2025/03/10/qualys-servicenow-automating-risk-driven-remediation-for-container-security
[62] SentinelOne, "Container Vulnerability Management: Securing in 2026," https://www.sentinelone.com/cybersecurity-101/cloud-security/container-vulnerability-management/
