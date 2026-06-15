# Secret & Credential Leakage Patterns

This reference document contains exhaustive regular expression patterns, entropy rules, and high-risk variable names to detect hardcoded secrets, API keys, tokens, and private keys in application source code. These patterns are compiled from leading secret scanners including **Gitleaks** [1] and **TruffleHog** [2].

## 1. Exhaustive Regex Pattern Table

When reviewing code line-by-line, check for strings matching the following regular expressions.

| Service / Token Type | Regular Expression Pattern | Severity |
| :--- | :--- | :--- |
| **AWS Access Key ID** | `\bAKIA[0-9A-Z]{16}\b` | **Critical** |
| **AWS Secret Access Key** | `(?i)aws_(?:secret|key|access)?_?(?:secret)?_?(?:access)?_?(?:key)?[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=\s*){1,2}[\x60'"\s=]{0,5}([A-Za-z0-9/+=]{40})(?:[\x60'"\s;]\|\\n\|$)` | **Critical** |
| **GitHub Personal Access Token** | `\bgh[pousr]_[A-Za-z0-9_]{36,255}\b` | **Critical** |
| **Google API Key** | `\bAIza[0-9A-Za-z\-_]{35}\b` | **High** |
| **Google OAuth Client ID** | `\b[0-9]+-[a-zA-Z0-9_]{32}\.apps\.googleusercontent\.com\b` | **Medium** |
| **Stripe Secret Key** | `\bsk_(?:live|test)_[0-9a-zA-Z]{24,}\b` | **Critical** |
| **Slack Bot Token** | `\bxoxb-[0-9]{10,13}-[a-zA-Z0-9]{24,}\b` | **Critical** |
| **Slack User Token** | `\bxoxp-[0-9]{10,13}-[a-zA-Z0-9]{24,}\b` | **Critical** |
| **OpenAI API Key** | `\bsk-[a-zA-Z0-9]{48,}\b` | **Critical** |
| **Anthropic API Key** | `\bsk-ant-api03-[a-zA-Z0-9_\-]{93}AA\b` | **Critical** |
| **JSON Web Token (JWT)** | `\beyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\b` | **High** |
| **Generic Password Assignment** | `(?i)(?:password|passwd|pass|pwd|secret|token|credential|auth_key|private_key)[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=\s*){1,2}[\x60'"\s=]{0,5}([a-zA-Z0-9_!@#$%^&*()\-+=]{8,})(?:[\x60'"\s;]\|\\n\|$)` | **High** |
| **SSH/Private Keys** | `-----BEGIN (?:RSA\|EC\|DSA\|OPENSSH\|PRIVATE) KEY-----` | **Critical** |

---

## 2. High-Risk Variable Names

Scan files for variable assignments that typically contain credentials. If these variables are assigned hardcoded string literals (e.g., `const DB_PASS = "admin123"`), they represent critical vulnerabilities.

- `password`, `passwd`, `pwd`, `pass`
- `secret`, `client_secret`, `app_secret`, `db_secret`
- `api_key`, `apikey`, `api_token`, `apitoken`
- `token`, `access_token`, `refresh_token`, `auth_token`
- `credential`, `credentials`
- `private_key`, `privatekey`, `ssh_key`
- `connection_string`, `conn_str`, `db_url`, `database_url`
- `salt`, `encryption_key`, `decryption_key`

---

## 3. Entropy-Based Detection Heuristics

Automated regex scanners can miss custom or proprietary API keys. To identify these, apply **Shannon Entropy** analysis [3] to any suspicious string literal in the code.

> **Shannon Entropy Formula:**
> $$H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$
> Where $P(x_i)$ is the probability of character $x_i$ appearing in the string.

### Entropy Thresholds for Code Review:
- **Base64 Strings (high-density characters)**: If a string has an entropy $> 4.5$ and length $> 20$, flag it as a potential key.
- **Hexadecimal Strings**: If a string has an entropy $> 3.0$ and length $> 32$ (e.g., MD5/SHA hashes or keys), flag it for verification.
- **High-Entropy Variable Assignments**: Any assignment of a high-entropy string to a variable with a name listed in the **High-Risk Variable Names** section is a **Critical** finding.

---

## 4. Remediating Leaked Credentials

If a hardcoded secret is discovered during the audit, you must recommend the following remediation steps immediately:

1. **Rotate the Secret**: Consider the compromised credential fully exposed. Revoke it at the provider level and generate a new key.
2. **Environment Variables**: Move the secret to an externalized environment variable or a `.env` file (which must be added to `.gitignore`).
3. **Secrets Manager**: For production deployments, recommend integrating dedicated secret vaults such as **HashiCorp Vault**, **AWS Secrets Manager**, **Azure Key Vault**, or **GCP Secret Manager**.
4. **Git History Purge**: If the secret was committed to Git, purging the current commit is insufficient. The entire repository history must be scrubbed using tools like `git-filter-repo` or `BFG Repo-Cleaner` [4].

---

## References

* [1] [Gitleaks Secret Scanner Configuration](https://github.com/gitleaks/gitleaks/blob/master/config/gitleaks.toml)
* [2] [TruffleHog Secret Scanner Repository](https://github.com/trufflesecurity/trufflehog)
* [3] [GitGuardian: Detecting Secrets in Source Code via Entropy](https://blog.gitguardian.com/secrets-in-source-code-episode-3-3-building-reliable-secrets-detection/)
* [4] [GitHub: Removing Sensitive Data from a Repository](https://docs.github.com/code-security/secret-scanning/about-secret-scanning)
