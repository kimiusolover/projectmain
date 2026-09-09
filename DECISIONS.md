# Design Decisions

Last reviewed: 2026-09-08

## D-001: Evidence-gated AX23V support

Status: accepted
Decided: 2026-08-29
Reason: Similar devices can differ in port mapping, factory layout, and regulatory/calibration data. A plausible inherited value is not device proof.

`ax23v-v1` is an independent device definition, not an AX23 v1 alias. Its current state is `discovery`; unknown platform, partition, calibration, factory-image, and RF information must block the relevant action.

Related: `router-platform/devices/tplink/archer-ax23v-v1/`, [docs/knowledge/hardware.md](docs/knowledge/hardware.md).

## D-002: Fail closed for flashable images

Status: accepted
Decided: 2026-08-29
Reason: A deterministic fixture or third-party success report is not a safe write contract.

No AX23V image may be created or presented as flashable without verified partitions, bootloader-visible regions, image format/signing, source/toolchain inputs, and project-owned validation. Preserve U-Boot, its environment, factory/ART/device data, and TP-Link-reserved regions.

Related: [docs/knowledge/boot.md](docs/knowledge/boot.md), [docs/knowledge/storage.md](docs/knowledge/storage.md).

## D-003: RF Regulatory Unlock is a constrained profile application

Status: accepted
Decided: 2026-08-29
Reason: Country selection alone cannot prove exact equipment, calibration, current rules, or driver feasibility.
Supersedes: proposed direct country-code rewriting.

RF configuration uses a reviewed Certification Profile; it does not directly write a country string. Credentials for the RF-sensitive path are separate from ordinary OS management credentials, and deployment should require a physical wired management path. Evidence gaps, hardware mismatch, calibration failure, or contradictory limits result in `TX DENIED`.

Related: [docs/knowledge/regulatory.md](docs/knowledge/regulatory.md), `certificateDB/CONSUMER_CONTRACT.md`.

## D-004: Immutable, cache-only upstream intake

Status: accepted
Decided: 2026-08-29
Reason: Reproducibility and reviewability require stable, inspectable inputs.

Consumers accept only `status: locked` source records with immutable revision, exact archive filename, SHA-256, HTTPS provenance/retrieval evidence, and a matching local cache. They do not fetch, choose mirrors, resolve moving references, or use locally modified source trees as substitutes.

Related: [docs/knowledge/build.md](docs/knowledge/build.md).

## D-005: Host/CI builds; target applies verified artifacts

Status: accepted
Decided: 2026-08-29

Build, signing, and repository generation remain host/CI responsibilities. The router only verifies/applies target artifacts. Target toolchain, sysroot, ABI, kernel release/config/vermagic are explicit gates; host binaries never stand in for target artifacts.

Related: [docs/knowledge/build.md](docs/knowledge/build.md).

## D-006: x86 preview stays QEMU/UEFI-only

Status: accepted
Decided: 2026-09-01
Supersedes: treating GRUB/systemd-boot/physical PC paths as the initial shared target.

The first general-PC target is `x86_64-qemu-uefi-preview` under QEMU/OVMF with COW overlays/no host-disk writes. It is not a promise of physical-PC boot, USB installer, Secure Boot, or AX23V compatibility.

## D-007: Curated RAG over unfiltered chat history

Status: accepted
Decided: 2026-09-02
Reason: Conversations mix accepted decisions, tentative alternatives, and mistakes; status-aware curation prevents obsolete proposals from becoming instructions.

Index the current Markdown knowledge base and repository documentation as the primary local-LLM context. Keep raw ChatGPT discussions, if retained, outside the default RAG corpus and label them historical/untrusted discussion.

Related: [CONVENTIONS.md](CONVENTIONS.md).

## D-008: Source-lock state is not target readiness

Status: accepted
Decided: 2026-09-08
Reason: A target can have a valid locked component archive while its device target record, kernel ABI contract, or hardware evidence remains incomplete.

Record and retrieve source-lock status at the individual source/toolchain level, and target readiness separately. In particular, the locked OpenWrt MT7621 toolchain is usable only as a verified input; `ax23v-v1` remains `pending-verification` with cross-build, image, flash, and RF authorization set to false. Do not summarize this as either “all AX23V inputs are unlocked” or “the AX23V target is ready.”

Related: [docs/knowledge/build.md](docs/knowledge/build.md), `router-upstream/targets/ax23v-v1.yaml`.
