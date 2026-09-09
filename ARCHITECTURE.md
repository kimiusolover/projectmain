# Router OS Architecture

Status: accepted
Last reviewed: 2026-09-02

## Trust and build flow

```text
primary sources / device observations
        -> certificateDB + router-platform (evidence and capability records)
        -> router-upstream (immutable source locks and toolchain records)
        -> router-packages (recipes and package policy)
        -> router-firmware (composition, planners, image pipeline)
        -> routerctl (host validation and orchestration)
        -> reviewed release path in router-infra
```

Each arrow transfers bounded input, not authorization. A successful build, planner, schema check, or certificate lookup does not authorize flash or RF operation.

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
