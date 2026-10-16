# Contributing

Thanks for helping improve lzr1-skills. The catalog is checked by
`scripts/lint_catalog.py`, which is the source of truth for the authoring
contract. Read its docstring and rules before opening a PR.

## The skill contract (summary)

- `skills/<name>/SKILL.md` exists, with frontmatter containing `name`
  (matching the directory) and `description`.
- The description must say when to use the skill: it has to contain `use when`, `use for` or `triggers` (case-insensitive), or the catalog linter fails with `desc-trigger`.
- Every file under `references/`, `scripts/`, `templates/` and `assets/` is
  named in `SKILL.md`, and every path `SKILL.md` names exists.
- Scripts (`.sh`, `.py`) are executable (`chmod +x`, then
  `git update-index --chmod=+x <path>` if needed).
- No symlinks inside skills.
- `skills-list.txt` matches the skill directories on disk exactly.

## Adding a skill

1. Create `skills/<name>/SKILL.md` (plus `references/`, `scripts/`,
   `templates/` as needed).
2. Add `<name>` to `skills-list.txt` in sorted order.
3. Bump the skill count in the places the linter checks:
   - `EXPECTED_SKILL_COUNT` in `install.sh`
   - the `skills-N-` badge in `README.md`
   - the "N curated AI skills" sentence in `README.md`
   - `EXPECTED` in `tests/test-installer.sh`, only if it is a literal; when it
     is derived from `skills-list.txt` it needs no edit.
4. Run the checks:

   ```bash
   python3 -I scripts/lint_catalog.py
   bash tests/test-catalog.sh
   bash tests/test-installer.sh
   bash tests/test-adversarial-remediations.sh
   ```

5. Add an entry under `## [Unreleased]` in `CHANGELOG.md`.

## Pull requests

Branch from `main`, keep commits focused, use conventional-commit messages
(`feat(skill): ...`, `fix(installer): ...`), and do not push to `main`
directly. By contributing you agree your work is licensed under the MIT
License in `LICENSE`.
