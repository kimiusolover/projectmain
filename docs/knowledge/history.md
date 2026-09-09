# Historical and Rejected Context

This file retains only context that helps prevent a past discussion from being
mistaken for current instructions. It is not a work queue or an implementation
specification. Default RAG retrieval should rank it below `accepted` records.

## Direct country-code rewriting

Status: rejected
Decided: 2026-08-29
Reason: A country string cannot establish the exact equipment identity,
calibration limits, current jurisdictional rules, or kernel/driver feasibility.
Supersedes: none
Related: [regulatory.md](regulatory.md), [../../DECISIONS.md](../../DECISIONS.md)

Do not implement RF enablement by directly changing a country code. The current
policy is a reviewed Certification Profile whose incomplete, mismatched, or
contradictory inputs result in TX denial.

## Treating AX23V as an AX23 v1 alias

Status: rejected
Decided: 2026-08-29
Reason: Similar model names and upstream compatibility references do not prove
identical port mapping, factory data, partitions, calibration, or image format.
Supersedes: none
Related: [hardware.md](hardware.md), [networking.md](networking.md), [../../DECISIONS.md](../../DECISIONS.md)

Archer AX23 v1 remains an explicitly labeled reference/base device only. It
must never silently supply AX23V facts, a flash layout, or RF settings.

## Raw ChatGPT conversation archives

Status: historical
Decided: 2026-09-02
Reason: Conversations can contain alternatives, provisional diagnoses, and
superseded information without durable evidence links.
Supersedes: none
Related: [../../CONVENTIONS.md](../../CONVENTIONS.md), [../../DECISIONS.md](../../DECISIONS.md)

If retained, archive transcripts outside the default corpus and label them as
untrusted historical discussion. Extract an item into this knowledge base only
after checking the owning repository or primary evidence and assigning a status.
