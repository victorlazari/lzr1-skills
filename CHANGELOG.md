# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Decision record `docs/decisions/0001-lerian-skill-scope.md`: no new
  Lerian-specific skills in this public MIT repo (they belong in the ring
  plugin); `lerian-helm` audited, no non-public material found.
- MIT `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md` and this changelog.
- Phase 2 (content freshness and routing). Decisions: keep all 86 skills and
  differentiate overlapping ones with descriptions and cross-references (no
  merges or deprecations); never invent model identifiers (current Claude
  family only, tier descriptions for other providers); thin-skill depth
  (`claude`, `go-lua`, `openclaw`) is deferred until a sourced content pass.
- Catalog linter: `stale-ref` is an ERROR (retired model and version
  identifiers), and `desc-trigger` is promoted from WARN to ERROR (every
  description needs `use when`, `use for` or `triggers`).

## [2.0.0]

### Added

- Hardened installer (`install.sh` VERSION 2.0.0) with ownership-marker
  validation and self-checks.
- Catalog of curated skills, including CodeRabbit, YAML and Hermes Agent.
