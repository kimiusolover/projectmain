# Boot and Execution Targets

## x86_64 QEMU/UEFI preview

Status: accepted
Decided: 2026-09-01

The initial general-PC execution target is `x86_64-qemu-uefi-preview` under QEMU/OVMF. It uses COW overlays and rejects host block-device input. Until its toolchain, rootfs, GPT/ESP layout, source locks, and QEMU E2E evidence are complete, it remains a preview design rather than a bootable/released image.

This does not cover physical PCs, USB media, Secure Boot, or AX23V.

## AX23V boot boundary

Status: accepted
Supersedes: conflating generic x86 bootloader discussions with AX23V MTD work.

AX23V uses an embedded-device/U-Boot path, not the QEMU/UEFI path. Existing information about console/boot behavior and factory formats is either inherited or evidence-gated; do not replace bootloader regions or treat an unflashable fixture as a vendor-acceptable image.
