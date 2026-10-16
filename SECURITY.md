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
  overwrite/removal safety, source verification).
- Scripts shipped inside skills (`skills/*/scripts/`).

Out of scope: the advice or opinions inside skill prose, and third-party tools
the skills reference.

## Supported versions

Only the latest release on `main` receives fixes.
