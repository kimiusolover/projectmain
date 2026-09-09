# Build, Source, and Software Stack

## Upstream Source Map v1

Status: accepted

`router-upstream` is the source map and lock authority. Each consumed source record identifies one artifact and requires a state (`pending-verification` or `locked`), canonical HTTPS upstream, immutable revision, cache filename, SHA-256, license, retrieval time, and provenance. A `locked` record is usable only when its exact archive is present in the local cache and its digest, revision, and provenance validate.

### Current lock/readiness separation

Status: evidence
Last reviewed: 2026-09-08

The OpenWrt 25.12.5 `ramips/mt7621` toolchain source record and the matching
`mipsel-24kc-musl` toolchain record are `locked`. They are usable only if the
exact declared cache archive is present and validates; neither record is a
board-support conclusion.
`router-upstream/targets/ax23v-v1.yaml` remains `pending-verification`: its
platform target, architecture/libc binding, kernel contract, and hardware
evidence fields are unset, and every authorization flag remains false.

Separately, the `router-firmware/sources/` component records for the planned
software stack remain `pending-verification`. Retrieval should report these
three layers independently: component lock, target readiness, and hardware /
image authorization.

Builds never retrieve missing inputs, select mirrors, use `latest`/moving branches, or substitute host/local source state. Automated sync can produce a review proposal only; it cannot change locks, build, sign, publish, flash, or alter RF settings.

## Software stack

Status: proposed

The declared minimal-layer policy covers systemd, Kea, Unbound, hostapd, Jool, and nftables. It selects only explicitly justified features. A missing, unset, false, or unknown requirement rejects a conditional feature; `excluded` features cannot be enabled from external inputs. The Tiny Plan is a proposed package configuration, not hardware/image/RF permission.

## Cross-build gate

Status: proposed

AX23V uses a dedicated MIPS/musl gate. Although a matching OpenWrt MT7621
toolchain input is locked, the AX23V target record is `pending-verification`;
no AX23V cross-build is authorized until the exact platform target, sysroot,
kernel source/release/config hash, vermagic, ABI, and hardware evidence are
locked and mutually consistent.

Related: [repositories.md](repositories.md), [hardware.md](hardware.md).
