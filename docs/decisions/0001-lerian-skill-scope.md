# 0001. Lerian skill scope in this public repository

## Status

Accepted (2026-10-16), with one open item for the repository owner (see
Open items). Reversible by the repository owner.

## Context

This repository is public and MIT-licensed (`LICENSE`). Lerian products carry
different terms: Midaz (with Tracer) and Fetcher are source-available under
ELv2, the other products are closed source, and internal conventions are not
public. Content derived from those internals cannot be republished under MIT
unless the copyright holders decide to do so. This note is a scoping decision,
not legal advice.

The one Lerian-named skill already present, `skills/lerian-helm/`, was
audited with a keyword and pattern search for non-public material
(2026-10-16). Files read: `SKILL.md`,
`references/complete-reference.md`, `scripts/validate-security.sh`.

Grep patterns used (case-insensitive where marked `-i`), all run recursively
over `skills/lerian-helm/`:

- URLs: `https?://[^ )"`>]+` (-o). Found only `github.com/golang-migrate/migrate`,
  `helm.sh/docs/`, `kubernetes.io/docs/concepts/security/pod-security-standards/`.
- Internal domains: `[a-z0-9.-]+\.(internal|local|corp|lan|lerian\.(io|com|app|net|studio))\b` (-i). No matches.
- Registry and account ids: `\b[0-9]{12}\b|\.dkr\.ecr\.|\.amazonaws\.com`. No matches.
- Credentials: `(token|secret|password|api[_-]?key|bearer|ghp_|AKIA|xox[bp]-)` (-i). No matches.
- Git remotes other than LerianStudio: `github\.com/[^ )"]+|git@|ssh://` minus `LerianStudio`. Only the golang-migrate link.
- People and customers: `@[a-z0-9-]+\.[a-z]{2,}|gandalf|customer|cliente` (-i). No matches.
- Local paths and private IPs: `/Users/|/home/|10\.x|192\.168|172\.16-31`. No matches.

Result: the patterns above found no credentials, internal hostnames, account
ids, or personal or customer names; nothing was removed. The only registry
reference is the public `oci://registry-1.docker.io/bitnamicharts/postgresql`.
A pattern search cannot show that the chart conventions the skill describes are
public; that needs the owner's confirmation (see Open items).

## Decision

- No new Lerian-specific skills are added to this public repository.
- `lerian-helm` stays provisionally: the audit found no credentials or
  identifiers, and it is re-audited whenever it changes. Whether the
  conventions it documents are public is for the owner to confirm.
- Candidate Lerian skills belong in the separate ring plugin.
- Non-public Lerian material must not be submitted here (see `SECURITY.md`).

## Open items

- Repository owner: confirm that the Helm chart conventions described in
  `skills/lerian-helm/` are public and may be published under MIT. Until
  then the skill's status rests on the pattern audit only.

## Consequences

- The public catalog stays redistributable under MIT.
- Lerian-specific workflows are not discoverable through this installer.
- If audit findings ever surface, content is removed from the working tree;
  git history would still contain it, and any history rewrite is the owner's call.

## Alternatives considered

- Copy internals under MIT: rejected; it republishes ELv2 and closed-source
  material under terms the copyright holders have not chosen.
- Relicense the repository: rejected; it would affect every existing
  contributor and user for the benefit of a few skills.
- Separate private repository: viable for internal use, but does not serve
  public users and splits distribution; the ring plugin already fills this role.
- Ring plugin: chosen home for Lerian-specific skills.
