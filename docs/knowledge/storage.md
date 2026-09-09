# Storage Layout Knowledge

## Logical storage model

Status: accepted

Classes are `BOOT`, `DEVICE_DATA`, `SYSTEM`, `CONFIG`, `STATE`, `LOG`, `CACHE`, and `RECOVERY`. `BOOT`, `DEVICE_DATA`, `RECOVERY`, `SYSTEM`, and `CONFIG` are protected from reclaim; pressure reclaim order is `CACHE -> LOG -> STATE`. LOG/CACHE require quotas and an OOM reserve. CONFIG requires validate-before-write atomic updates with a previous-known-good reserve.

The logical model is device-independent policy, not a physical partition map.

## AX23V planner state

Status: proposed

The planner may report a `proposed` layout, always `flashable: false`, to explain missing evidence. It cannot produce a final layout while physical media, MTD boundaries, bootloader-visible regions, RAM budget, or capacity allocations are unverified/unset. A final layout also remains conditional on image format, signing, and release validation.

Observed MTD names/sizes are evidence records only. They include nested regions under `firmware`; they are not an offset-verified partition contract and must not be double-counted.

Related: `router-firmware/docs/storage-specification.yaml`, `router-firmware/docs/layout-planner-specification.yaml`.
