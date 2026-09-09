# Regulatory and RF Knowledge

## RF Regulatory Unlock

Status: accepted
Decided: 2026-08-29
Supersedes: direct country-code manipulation.

RF-sensitive configuration is applied from an exact, reviewed Certification Profile; it is not a generic `country` string change. Use credentials separate from normal OS administration and require a physical wired management path for deployment. The implementation must record the profile/evidence identity and fail closed.

The effective policy is the restrictive intersection of:

1. certificateDB evidence-derived constraints for the exact variant;
2. current jurisdictional requirements;
3. router-platform hardware and antenna capability;
4. immutable calibration/board-data limits; and
5. kernel and driver limits.

Any missing, stale, ambiguous, mismatched, or contradictory input disables TX. `verified` evidence and a certification number do not by themselves authorize transmission.

## Current AX23V JP profile

Status: evidence

`routerctl/examples/ax23v/regulatory/JP/certification-profile.yaml` is a review template with `evidenceStatus: incomplete`. It intentionally yields TX denial until the profile itself, calibration match, and all other consumer inputs are reviewed. The numerical constraints in that template are not a license to deploy RF settings independently.

This is deliberately distinct from the reviewed `certificateDB` record for
JP certification `201-230283`: that record can establish evidence identity
and evidence-derived input, but does not upgrade the routerctl template or
grant runtime transmission authority.

## Evidence handling

Status: accepted

Legal texts establish relevance and must be kept current, but do not identify a device or derive device-specific channel, bandwidth, antenna, or power limits. Store retrieved official material with identity, source URL, retrieval information, hash, locator, and review state. Keep private/raw device evidence out of public repositories and default RAG.
