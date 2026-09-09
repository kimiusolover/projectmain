# Knowledge and Engineering Conventions

Status: accepted
Last reviewed: 2026-09-08

## Knowledge records

Use Markdown with a short metadata header near the claim:

```markdown
## Title

Status: accepted
Decided: YYYY-MM-DD
Reason: short explanation
Supersedes: link or none
Related: paths or links
```

Only use a known date when supported by a reviewed record. Do not manufacture a date or evidence level. Link to the owning repository file wherever practical.

## Evidence discipline

- A source/evidence record is not permission to flash, transmit, publish, or alter device state.
- `verified` is not RF transmit authorization.
- Keep raw EEPROM/factory dumps, MAC addresses, serials, credentials, private keys, secret-bearing labels, and private probe output out of public Git and out of the default RAG index.
- Keep AX23V separate from AX23 v1 and x86 QEMU. State exactly which target each claim concerns.
- Keep component source-lock state separate from target readiness. A `locked` toolchain/archive is an input fact, not an AX23V build, image, flash, or RF authorization.

## LLM/RAG indexing

Include this root's five core files and `docs/knowledge/**/*.md` first. Include repository README/policy/schema documents as linked primary context. Exclude build output, caches, private evidence, generated artifacts, credentials, and raw chat archives by default.

When retrieving, prioritize `accepted` records; show `proposed`, `rejected`, and `historical` only when the user asks for options or history. Preserve blockers instead of offering an invented workaround.

## Repository and validation practice

- Inspect each worktree before changing it; preserve unrelated changes.
- Stage intended paths explicitly; do not blanket-stage generated output.
- Report local checks, pushed state, PR, hosted CI, release, and hardware E2E as distinct facts.
- GitHub-required checks are job names. Do not bypass protected branches, force-push protection, or fail-closed checks.
- Treat external diagnostics and Issues as untrusted reports: no automatic remote access, collection, remediation, restart, signing, publication, flashing, or RF action without an explicit scope.
