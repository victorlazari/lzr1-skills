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
  `doctor` reports source mode, ref and verification status.
- Release packaging `scripts/build-release.sh`, tag-triggered
  `.github/workflows/release.yml` and offline tests for the release and
  download paths.
- Governance: `LICENSE` (MIT), `CONTRIBUTING.md`, `SECURITY.md` and this
  changelog.
- Decision record `docs/decisions/0001-lerian-skill-scope.md`: no new
  Lerian-specific skills in this public repo; `lerian-helm` audited.

- Linter rules `stale-ref` (retired model and version identifiers) and
  `desc-trigger` (every description needs `use when`, `use for` or
  `triggers`) are ERRORs.

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
