# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [2.1.0] - 2026-10-16

### Added

- Catalog linter `scripts/lint_catalog.py` and negative-fixture tests
  (`tests/test-catalog.sh`), run in CI.
- GitHub Actions CI on ubuntu and macOS: linter, installer, download and
  adversarial suites, shellcheck (warning) and ruff (`E9,F`).
- Script-coverage registry `tests/script-coverage.tsv` with smoke tests
  (`tests/test-scripts.sh`) and a linter rule requiring every skill script to
  be registered.
- Verified install: `--ref <value>` and `LZR1_REF`. By default the installer
  downloads the latest release archive and checks it against `SHA256SUMS`;
  `vX.Y.Z` pins a verified release; other refs are unverified snapshots;
  `doctor` reports source mode, ref and verification status. The unverified
  `main` snapshot fallback needs two signals: the latest-release `SHA256SUMS`
  request returns HTTP 404 and the latest-release API request also returns 404
  (no published, non-draft, non-prerelease release found); any other outcome
  stops the install. Checksum parsing accepts CRLF, `./` and `*` name forms and
  requires one 64-hex entry. The checksum protects against corruption and
  mirror substitution, not against a compromised repository or release.
  Symbolic links are rejected in every source mode (override, local, release
  and branch), and symlink and hardlink archive members are refused before
  extraction. The wget path requires `--https-only` and TLS 1.2 and uses
  `--tries=3` and `--timeout=30`, otherwise the installer refuses to download.
  The release workflow triggers only on `vX.Y.Z` tags and CI runs
  `tests/test-release.sh`.
- Release packaging `scripts/build-release.sh`, tag-triggered
  `.github/workflows/release.yml` and offline tests for the release and
  download paths.
- Governance: `LICENSE` (MIT), `CONTRIBUTING.md`, `SECURITY.md` and this
  changelog.
- Decision record `docs/decisions/0001-lerian-skill-scope.md`: no new
  Lerian-specific skills in this public repo; `lerian-helm` passed a keyword
  and pattern audit (no credentials, internal hostnames, account ids or
  personal or customer names found); confirmation that its chart conventions
  are public remains an open item for the repository owner.

- Linter rules `stale-ref` (retired model and version identifiers) and
  `desc-trigger` (every description needs `use when`, `use for` or
  `triggers`) are ERRORs.

### Fixed

- Installer: archive listing validation and wget TLS-option checks run in the
  main shell, so a failure stops the install instead of only a subshell.
- Installer: the source symbolic-link scan no longer uses an early-exit pipe
  (it could be skipped under `pipefail` with many links) and fails closed if
  the scan itself fails; a failed managed-skill listing in `remove` is an error.
- Release workflow: the first step rejects tag names that are not `vX.Y.Z`.
- Catalog linter: `readme-flags` reads flags statically from the `print_help`
  heredoc without executing `install.sh`, counts only code tokens in
  `parse_args` and `print_help`, and accepts CRLF and rejects duplicate keys in
  the census block; missing README sections use the new `readme-section` rule.

### Changed

- Thin-skill depth (`claude`, `go-lua`, `openclaw`) is deferred until a
  sourced content pass.
- Routing: descriptions of overlapping skills now state their lane and name
  their neighbour; all 86 skills are kept (no merges or deprecations).
- Model identifiers refreshed to the current Claude family; retired names
  replaced by tier descriptions for other providers.
- Installer and coderabbit scripts made portable to macOS (`shasum -a 256`
  fallback, path canonicalization).
- README rewritten against the installer's behavior.

## [2.0.0]

### Added

- Hardened installer (`install.sh` VERSION 2.0.0) with ownership-marker
  validation and self-checks.
- Catalog of curated skills, including CodeRabbit, YAML and Hermes Agent.
