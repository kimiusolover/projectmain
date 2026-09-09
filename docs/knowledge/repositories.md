# Repository Responsibilities

Status: accepted
Last reviewed: 2026-09-02

## Boundary map

### router-platform

Status: accepted

Canonical home for device identity, physical interfaces, GPIO/NVMEM/radio capability records, partition preservation policy, and evidence boundaries. For AX23V, the authoritative unit is `router-platform/devices/tplink/archer-ax23v-v1/`. Consumers must locate it explicitly and fail rather than falling back to old copied data.

### certificateDB

Status: accepted

Stores certification/evidence records and evidence-derived constraints. A reviewed/verified record is only an input. It neither produces runtime RF configuration nor grants permission to transmit.

### router-firmware

Status: accepted

Owns reproducible firmware composition: package selection, kernel/source locks as inputs, rootfs/image assembly, provenance, and planners. It must consume platform data without promoting its safety states. Its AX23V fixture is explicitly unflashable.

### routerctl

Status: accepted

Host-side CLI for manifest validation, planning, artifact resolution/verification, and evidence-aware orchestration. Its validation gates do not generate images or permit device writes/RF activity.

### router-upstream

Status: accepted

Owns source-lock records, immutable input policy, toolchain records, and proposal-only upstream sync/patch metadata. Build consumers may use only a matching local cache and an accepted lock.

### router-packages

Status: accepted

Owns recipes and package-level configuration. It consumes source locks from `router-upstream`, hardware facts from `router-platform`, and does not own either image assembly or regulatory authorization.

### router-infra

Status: accepted

Provides shared CI, release gating, SBOM/provenance, and policy integrations. It holds neither device definitions nor firmware inputs/secrets.
