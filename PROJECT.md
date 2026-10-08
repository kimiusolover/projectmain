# Router OS Project Knowledge Base

Status: accepted
Last reviewed: 2026-10-07

This directory is the curated, Markdown-first knowledge base for the Router OS repositories. It is intended for people and local LLM/RAG tools. It is not a firmware source tree, evidence store, or deployment authority.

## Read this first

1. Read this file, [ARCHITECTURE.md](ARCHITECTURE.md), and [CONVENTIONS.md](CONVENTIONS.md).
2. For a design change, read [DECISIONS.md](DECISIONS.md) and the linked topic document under `docs/knowledge/`.
3. Treat each repository's tracked policy, schema, and implementation as the executable source of truth. This knowledge base is a navigable summary and must be corrected when it disagrees with them.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| `accepted` | Current project policy or responsibility boundary. |
| `proposed` | A reviewable design or plan; not implementation authority. |
| `rejected` | An approach deliberately not to use. |
| `historical` | Retained context that is not current policy. |
| `evidence` | A source, observation, or traceability record; it does not by itself authorize an action. |

Unknown, `unset`, `discovery`, `observed`, `unverified`, and `pending-verification` are meaningful safety states. Never promote them merely because this knowledge base is being summarized.

## Project purpose

Build an auditable Router OS ecosystem with reproducible host/CI builds, evidence-gated device support, safe update/recovery boundaries, and a fail-closed RF configuration path. The initial executable target is an `x86_64-qemu-uefi-preview`; AX23V work remains evidence-gated.

## Repository map

| Repository | Owns | Does not own |
| --- | --- | --- |
| `router-platform` | Device identity, interfaces, capability/evidence records, preservation policy | Package selection, images, releases |
| `certificateDB` | Certification/evidence records and derived-constraint inputs | RF transmission permission or runtime configuration |
| `router-firmware` | Reproducible composition, rootfs/image pipeline, storage/tiny planners | Platform facts or device data |
| `routerctl` | Host-side validation, planning, artifact and evidence orchestration | Firmware generation or permission to flash/transmit |
| `router-upstream` | Immutable source locks, toolchain records, patch/sync metadata | Network fetching during builds, board authorization |
| `router-packages` | Package recipes and package configuration | Source locks, device facts, image assembly |
| `router-infra` | Shared CI/release/SBOM/provenance controls | Firmware, device definitions, secrets |
| `router-edk2` | Planned: EDK II platform firmware implementation, architecture/SoC/board packages, firmware descriptions | Canonical hardware facts, source locks, OS image composition |

Related: [docs/knowledge/repositories.md](docs/knowledge/repositories.md).

## Current headline

Status: accepted

- QEMU/UEFI preview, cross-repository contracts, source-lock rules, and evidence-aware planners are foundations, not a released Router OS.
- `ax23v-v1` is distinct from Archer AX23 v1 and remains `discovery`.
- No project-owned AX23V flashable image, hardware E2E, or RF transmit authorization exists.
- The local LLM knowledge base should be indexed ahead of raw conversation archives. Archive conversations only as low-priority historical material.

Related: [TODO.md](TODO.md), [docs/knowledge/hardware.md](docs/knowledge/hardware.md).

Topic index: [repositories](docs/knowledge/repositories.md), [hardware](docs/knowledge/hardware.md), [boot](docs/knowledge/boot.md), [storage](docs/knowledge/storage.md), [networking](docs/knowledge/networking.md), [regulatory](docs/knowledge/regulatory.md), [build](docs/knowledge/build.md), and [history](docs/knowledge/history.md).

## Parent repository scope

Status: accepted
Decided: 2026-09-09

The parent repository tracks the five root knowledge documents,
`docs/knowledge/`, `.gitignore`, and the portable `.routerctl/components.json`
and `.routerctl/workspace.json` configuration files. The project currently has seven existing
component repositories; D-009 establishes `router-edk2` as a planned eighth component repository.
Each component repository keeps its own independent Git history and is ignored by this
parent repository; they are not submodules. Cloning the parent does not fetch
component repositories or pin their revisions. Obtain the component repositories
separately when following links into their source trees.

Downloaded archives under `router-source-cache/` and local scratch notes in
`tmp.md` remain outside this repository. Source hashes and provenance belong in
`router-upstream`. Other local `.routerctl/` files are ignored by default.
