# Router OS Open Work

Last reviewed: 2026-09-08

Items are intentionally incomplete. They are not authorization to bypass the linked gates.

## AX23V hardware and flash

Status: proposed

- Capture/redact `/proc/mtd` and serial/bootloader partition listings; verify offsets, erase sizes, writability, owners, and bootloader-visible regions.
- Confirm WAN and LAN1-4 by physical link test; validate remaining LEDs.
- Compare redacted base/interface/radio MAC relationships and calibration offset/length without committing raw device data.
- Validate Wi-Fi bring-up, cold boot, reboot, factory upgrade, sysupgrade, and recovery on project-owned hardware.
- Establish exact image format/signing and release/recovery evidence before changing AX23V image status.

## Regulatory

Status: proposed

- Obtain and review official, exact-variant certification records/reports; retain identity, retrieval, hash, and review traceability.
- Verify current jurisdictional rules and tie them to the exact hardware, antenna, calibration, and driver limits.
- Implement an audited RF-profile application path only after the inputs can produce a restrictive compatible configuration.

## Build and packages

Status: proposed

- Complete immutable source locks for required components and cache archives.
- Lock/review the MIPS toolchain, sysroot, ABI, kernel release/config/vermagic, and AX23V target record before enabling cross-build entry points.
- Bind the already locked MT7621 toolchain/source archive to the AX23V target only after the target record's platform, ABI, kernel, and hardware-evidence fields are independently verified.
- Produce real target package artifacts and provenance; do not substitute host builds.

## x86 preview

Status: proposed

- Complete locked toolchain/rootfs/GPT/ESP layout and source inputs.
- Run QEMU/OVMF E2E through serial login before claiming a bootable preview.
- Consider USB/physical-PC work only in a later, separately evidenced phase.

## Knowledge maintenance

Status: accepted

- Update the affected topic and decision record in the same review as a material policy change.
- Periodically re-check RAG ingestion excludes private evidence and raw discussions.
