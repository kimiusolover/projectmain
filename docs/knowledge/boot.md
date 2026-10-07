# Boot and Execution Targets

## Router UEFI Platform Architecture v1

Status: accepted
Decided: 2026-10-07
Related: [DECISIONS.md#d-009-router-uefi-platform-architecture-v1](../../DECISIONS.md#d-009-router-uefi-platform-architecture-v1)

The project architecture separates EDK II UEFI platform firmware, systemd-boot, UKI, and the Linux root filesystem.

For x86/x86_64, the intended boot chain is:

EDK II UEFI firmware
 -> FAT32 EFI System Partition (ESP)
 -> systemd-boot
 -> UKI (Unified Kernel Image)
 -> Linux
 -> Btrfs root filesystem

Key architectural rules:
- EDK II implementation belongs to the planned `router-edk2` repository.
- Upstream source locks and EDK II source revisions are owned by `router-upstream`.
- Physical device facts and partition preservation policies remain canonically owned by `router-platform`.
- OS image composition belongs to `router-firmware`.
- `x86_64-qemu-uefi-preview` remains a QEMU/OVMF preview target with COW overlays and no host-disk writes. Physical-PC boot, USB installer, or released x86 firmware are not claimed.
- Secure Boot is part of the future firmware security layer. Its presence in the architecture design does not mean that the current preview or any physical target is Secure-Boot verified.
- MIPS EDK II support remains a planned/research baseline. MIPS P0 accepted != MT7621 UEFI supported != Archer AX23 v1 UEFI supported != AX23V hardware verified.
- `ax23v-v1` remains in `discovery` and distinct from Archer AX23 v1.

## x86_64 QEMU/UEFI preview

Status: accepted
Decided: 2026-09-01

The initial general-PC execution target is `x86_64-qemu-uefi-preview` under QEMU/OVMF. It uses COW overlays and rejects host block-device input. Until its toolchain, rootfs, GPT/ESP layout, source locks, and QEMU E2E evidence are complete, it remains a preview design rather than a bootable/released image.

This does not cover physical PCs, USB media, Secure Boot, or AX23V.

## AX23V boot boundary

Status: accepted
Supersedes: conflating generic x86 bootloader discussions with AX23V MTD work.

AX23V uses an embedded-device/U-Boot path, not the QEMU/UEFI path. Existing information about console/boot behavior and factory formats is either inherited or evidence-gated; do not replace bootloader regions or treat an unflashable fixture as a vendor-acceptable image.
