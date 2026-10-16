# Security Policy

## Reporting a vulnerability

Please report privately using GitHub private vulnerability reporting: open the
repository's **Security** tab and choose **Report a vulnerability**. Do not
open a public issue for security problems.

> Maintainer manual step: enable "Private vulnerability reporting" under
> Settings > Code security and analysis in the repository.

## Scope

In scope:

- Installer integrity: `install.sh` (path handling, ownership markers,
  overwrite/removal safety, source verification). The verification model is:
  - Checksum: the release archive is checked against `SHA256SUMS` before
    extraction. This protects against corruption and mirror or proxy
    substitution; it does not protect against a compromised repository or
    release (both files come from the same place and releases are not signed),
    nor against a network position that can forge HTTPS. Non-release refs and
    the `main` fallback are unverified snapshots.
  - Two-signal fallback: the unverified `main` snapshot is used only when the
    `SHA256SUMS` request returns 404 **and** the latest-release API request
    also returns 404 (no published, non-draft, non-prerelease release found).
    Any other outcome stops the install.
  - Transport: `curl` uses `--proto '=https' --tlsv1.2` with retries and
    timeouts; the `wget` path requires `--https-only` and TLS 1.2 plus
    `--tries=3` and `--timeout=30`, or the installer refuses to download.
  - Symbolic links in the skills tree are rejected in every source mode;
    symlink and hardlink archive members are refused before extraction.
- Scripts shipped inside skills (`skills/*/scripts/`).

Out of scope: the advice or opinions inside skill prose, and third-party tools
the skills reference.

Do not submit non-public Lerian material to this repository.

## Supported versions

Only the latest release on `main` receives fixes.
