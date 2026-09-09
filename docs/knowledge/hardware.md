# Hardware Knowledge

## AX23V v1

Status: evidence
Last reviewed: 2026-09-08

Canonical data: `router-platform/devices/tplink/archer-ax23v-v1/`.

The device record identifies an Archer AX23V hardware revision 1.0, `mipsel`/MT7621DAT, with `ramips/mt7621` as the intended upstream target. Its overall status remains `discovery`, and `image.format`, signing, and layout remain unset. This summary must not be used to generate or flash an image.

The physical-capability record contains an integrity-referenced, private
read-only observation of 16 MiB SPI-NOR and top-level MTD registration, but
its verified media, physical boundaries, writability, bootloader visibility,
and RAM budget remain unset. It is evidence, not a partition contract.

### Directly observed or explicitly recorded

Status: evidence

- WPS is recorded as active-low GPIO 7 / `rfkill`, with pressed/released hotplug evidence.
- The recessed Reset control supports active-low GPIO 8 and observed short-press reboot behavior; its hotplug name was not directly observed.
- GPIO 19 is the MT7621 PCIe external-reset control, not the physical reset button.
- A private, integrity-referenced observation records 16 MiB SPI-NOR and top-level MTD names. Nested kernel/rootfs/rootfs_data regions must not be double-counted.

### Inherited or third-party information

Status: evidence

WAN mapping, SafeLoader parameters, NVMEM offsets, radio data, MAC increments, Wi-Fi details, boot behavior, and factory/sysupgrade reports include inherited AX23 v1 or third-party information. They remain inputs requiring AX23V project-owned confirmation. They cannot relax preservation or flash gates.

### Preservation boundary

Status: accepted

Never create, replace, bundle, or overwrite U-Boot, U-Boot environment, factory/ART/calibration data, MAC addresses, or TP-Link-reserved regions.

Related: [boot.md](boot.md), [storage.md](storage.md), [regulatory.md](regulatory.md).
