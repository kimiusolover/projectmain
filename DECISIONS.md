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

No AX23V image may be created or presented as flashable without verified partitions, bootloader-visible regions, image format/signing, source/toolchain inputs, and project-owned validation. Preserve regions classified by the canonical router-platform storage contract (including U-Boot, its environment, factory/ART/device data, and TP-Link-reserved regions).

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

## D-009: Router UEFI Platform Architecture v1

Status: accepted
Decided: 2026-10-07
Reason: Formalize UEFI platform firmware boundaries, logical layering, component ownership, and boot chain separation across multiple architectures without creating or modifying component repositories in this PR.

The Router OS project adopts EDK II as its UEFI platform firmware implementation architecture across multiple targets.

Key decisions and repository ownership:
1. `kimiusolover/router-edk2` is designated as a planned eighth component repository. The repository itself is not created in this change. EDK II firmware implementation must not be placed in any existing repository (e.g. `router-platform/edk2/`, `router-firmware/edk2/`, `router-packages/edk2/`, `router-upstream/platform/`).
2. Component ownership:
   - `router-platform`: canonical owner of hardware facts, device identity, physical topology, pinouts, MTD/NVMEM boundaries, MAC/calibration locations, and partition preservation policies.
   - `router-upstream`: canonical owner of immutable upstream source identity, source locks, EDK II source revisions, archives, SHA-256 hashes, and toolchain provenance.
   - `router-edk2`: planned owner of EDK II implementation, architecture-specific support, silicon/SoC support packages, board/platform firmware packages, and firmware image descriptions.
   - `router-packages`: owner of Linux/runtime packages and package configuration.
   - `router-firmware`: owner of OS/image composition, kernel/rootfs/package selection, image pipeline, planners, and final OS artifact assembly.
   - `routerctl`: host-side validation, orchestration, and artifact verification.
   - `router-infra`: CI/release gating, SBOM, provenance, and policy integrations.
   - `certificateDB`: regulatory/certification evidence.

3. Firmware logical layering:
   - Logical hierarchy: Common UEFI -> Architecture (X64, AARCH64, MIPS32) -> SoC / Silicon (e.g. MT7621) -> Platform / Board (e.g. TP-Link Archer AX23 v1) -> Firmware Image.
   - Board-specific physical facts must not be embedded in SoC layers. Physical storage parameters, calibration locations, and partition preservation are owned canonically by `router-platform`.

4. Boot architecture (x86/x86_64):
   - Boot chain: EDK II UEFI firmware -> EFI System Partition (FAT32) -> systemd-boot (UEFI boot manager) -> UKI (Unified Kernel Image) -> Linux -> Btrfs root filesystem.
   - EDK II is the UEFI firmware implementation, distinct from systemd-boot (the boot manager). The ESP is FAT32, distinct from the Btrfs root filesystem.

5. Target readiness and safety state preservation:
   - `x86_64-qemu-uefi-preview` remains a QEMU/OVMF preview target with COW overlays and no host-disk writes. Physical PC boot, USB installer, and released firmware are not claimed.
   - Secure Boot is a planned future firmware security layer; its inclusion in the architecture does not mean that the current preview or any physical target is Secure-Boot verified.
   - MIPS EDK II support remains a planned research baseline. MIPS P0 accepted != MT7621 UEFI supported != Archer AX23 v1 UEFI supported != AX23V hardware verified.
   - `ax23v-v1` remains in `discovery` and distinct from Archer AX23 v1. No alias or hardware equivalence is introduced.
   - Btrfs root is an OS filesystem policy, while SPI NOR / eMMC / NVMe / MTD layouts remain target-specific physical storage contracts owned canonically by `router-platform`.

Related: [ARCHITECTURE.md](ARCHITECTURE.md), [docs/knowledge/repositories.md](docs/knowledge/repositories.md), [docs/knowledge/boot.md](docs/knowledge/boot.md), [docs/knowledge/edk2-mips-p0.md](docs/knowledge/edk2-mips-p0.md).
