# Router OS Architecture

Status: accepted
Last reviewed: 2026-10-07

## Trust and build flow

```text
primary sources / device observations
        -> certificateDB + router-platform (evidence and capability records)
        -> router-upstream (immutable source locks and toolchain records)
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
 router-edk2 (planned)               router-packages
 (UEFI firmware implementation)      (recipes and package policy)
        │                                   │
        └─────────────────┬─────────────────┘
                          │
                          ▼
                   router-firmware
                   (composition, planners, image pipeline)
                          │
                          ▼
                      routerctl
                      (host validation and orchestration)
                          │
                          ▼
                   reviewed release path in router-infra
```

Each arrow transfers bounded input, not authorization. A successful build, planner, schema check, or certificate lookup does not authorize flash or RF operation.

## Component responsibilities and firmware flow

Status: accepted
Decided: 2026-10-07
Related: [DECISIONS.md#d-009-router-uefi-platform-architecture-v1](DECISIONS.md#d-009-router-uefi-platform-architecture-v1)

Firmware implementation and OS image composition are separate concerns:
- **`router-platform`**: Owns hardware facts, device identity, physical topology, pinouts, MTD/NVMEM boundaries, MAC/calibration locations, and partition preservation policies.
- **`router-upstream`**: Owns immutable upstream source identity, source locks, EDK II source revisions, archives, SHA-256 hashes, and toolchain provenance.
- **`router-edk2`**: Planned repository owning EDK II firmware implementation, architecture support, silicon/SoC packages, board/platform packages, and firmware image descriptions.
- **`router-packages`**: Owns Linux runtime package recipes and package configurations.
- **`router-firmware`**: Owns final OS/image composition, kernel/rootfs/package selection, planners, and image pipeline assembly.

### Firmware logical layering

`router-edk2` uses a strict logical layering contract:

```text
Common UEFI
   ↓
Architecture (X64, AARCH64, MIPS32)
   ↓
SoC / Silicon (e.g., MT7621)
   ↓
Platform / Board (e.g., TP-Link Archer AX23 v1)
   ↓
Firmware Image
```

Board-specific physical facts (e.g. SPI-NOR size, radio partition, calibration offset) must never be embedded in the SoC/Silicon layer. Physical facts remain canonically owned by `router-platform`.

### x86/x86_64 boot chain architecture

```text
EDK II UEFI firmware
        ↓
EFI System Partition (FAT32)
        ↓
systemd-boot (UEFI Boot Manager)
        ↓
UKI (Unified Kernel Image)
        ↓
Linux
        ↓
Btrfs root filesystem
```

- **EDK II**: UEFI platform firmware implementation.
- **systemd-boot**: UEFI boot manager operating on the ESP.
- **UKI**: Unified Kernel Image combining Linux kernel, initrd, and command line into a single EFI executable.
- **ESP**: FAT32 filesystem holding boot artifacts.
- **Btrfs**: Operating system root filesystem policy. Btrfs is an OS filesystem choice and does not override target-specific physical storage contracts owned by `router-platform`.

## Execution environments

### Host and CI

Status: accepted

Compilation, source intake, package-repository generation, signing, and release creation happen on a controlled host/CI path. Inputs are cache-backed and immutable. Target architecture, ABI/sysroot, source revision, archive SHA-256, and signature/provenance are attached to artifacts. A locked component input does not make an otherwise incomplete target buildable or authorize an image.

### Target device

Status: accepted

The router verifies and applies prepared target artifacts. It must not compile, sign, generate repositories, or resolve arbitrary network dependencies. Device artifacts and the x86 QEMU preview are separate targets with no host-binary fallback.

## Target separation

| Target | State | Boundary |
| --- | --- | --- |
| `x86_64-qemu-uefi-preview` | preview | QEMU/OVMF only; COW overlay/no host-disk write; no physical-PC, USB, or Secure Boot claim |
| `ax23v-v1` | discovery | MT7621/MIPS device definition; no image assembly, flash, or RF authorization until project-owned evidence closes all gates |
| Archer AX23 v1 | historical/base reference | Not an alias for AX23V; use only as explicitly marked inherited/reference data |

## RF configuration flow

Status: accepted

```text
exact certificateDB evidence
 + current jurisdictional rules
 + router-platform hardware/antenna capability
 + immutable calibration/board data
 + kernel/driver-reported limits
 -> most restrictive compatible configuration
 -> otherwise TX denied
```

The generated runtime configuration belongs to its consumer and is not stored as a certificateDB fact. See [docs/knowledge/regulatory.md](docs/knowledge/regulatory.md).

## Storage flow

Status: accepted

Logical classes and policy are intentionally separate from physical facts. The planner can emit a proposed layout with explanations, but only verified media, boundaries, bootloader-visible regions, RAM budget, allocations, image format, signing, and release validation can ever lead to an eligible final layout. A planner output alone is never permission to write a device.
