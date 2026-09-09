# Networking Knowledge

## Service stack

Status: proposed

The current package-policy direction uses systemd/networkd with nftables, hostapd, Kea, Unbound, and Jool as separately declared components. Their presence in the Tiny Plan or recipe policy is not proof that they compile for a target, work together on a device, or are enabled in a released image.

## AX23V boundary

Status: evidence

AX23V port and radio details remain evidence-gated. Direct observations and inherited/third-party claims must remain distinguishable. In particular, do not copy AX23 v1 switch mappings into AX23V: the recorded AX23V hypothesis places WAN on dedicated GMAC1/PHY0 and LAN on DSA ports 1-4, but project-owned physical link testing remains required before a supported-device claim.

## Firewall and IPv6

Status: proposed

nftables and Jool are planned components, not a completed target networking profile. IPv6, NAT/firewall behavior, wireless enablement, DHCP/DNS behavior, and mesh/VHT/HE selection remain conditional on explicit feature inputs, target builds, and device/network E2E validation.

Related: [hardware.md](hardware.md), [build.md](build.md), [TODO.md](../../TODO.md).
