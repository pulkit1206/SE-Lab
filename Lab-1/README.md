# Lab 1 — Requirements Engineering & UML Use-Case Modelling

**Problem Statement #39 — Second-Hand Product Escrow Marketplace (Retail, E-Commerce & Finance)**

A secure peer-to-peer trading marketplace where buyer payments are held in escrow, independent
third-party inspectors certify product condition, and funds release only upon buyer sign-off.

**Stakeholders / Actors:** Buyer, Inspection Agent (primary) · Admin — Dispute Resolution (supporting)

---

## Deliverables

This folder contains the Lab 1 submission inside the [`SE-Lab`](../) repository. All three required
deliverables are present:

| # | Deliverable | File |
|---|-------------|------|
| 1 | Complete Requirements Table — exactly 5 FRs (FR-001…FR-005) + 2 NFRs (NFR-001, NFR-002) with ID, Type, Description, Priority, Acceptance Criteria, Rationale | [`docs/Requirements_Table.md`](docs/Requirements_Table.md) |
| 2 | UML Use-Case Diagram — all actors, primary use cases, one «include» + one «extend» relationship | [`docs/Use_Case_Diagram.drawio`](docs/Use_Case_Diagram.drawio) |
| 3 | Use-Case Flow Specification — one-page for a core use case (Preconditions, Postconditions, Main Success Scenario, One Alternate Flow) | [`docs/Use_Case_Flow_UC03.md`](docs/Use_Case_Flow_UC03.md) |

---

## Repository layout

```
Lab-1-Requirements-Engineering/
├── README.md                         # this index / overview
└── docs/
    ├── Requirements_Table.md         # 5 FRs + 2 NFRs (SRS-style table)
    ├── Use_Case_Flow_UC03.md         # UC-03 Approve Delivery & Release Funds
    └── Use_Case_Diagram.drawio       # open in draw.io → export as PDF
```

## How to use the use-case diagram

1. Open [`docs/Use_Case_Diagram.drawio`](docs/Use_Case_Diagram.drawio) in [draw.io](https://app.diagrams.net) (File → Open).
2. Review the actors, use cases, and the `«include»` / `«extend»` relationships.
3. Export as PDF: File → Export as → PDF (ensure background is **not** transparent).

## Scenario summary

- **FR-001** Lock buyer payment in escrow → order state "Under Inspection".
- **FR-002** Inspection agent certification (approve / reject with report + photos).
- **FR-003** Release escrowed funds only on buyer sign-off **and** "Certified" verdict (dual verification).
- **FR-004** Auto-deduct 5% escrow service fee on release + issue digital receipt.
- **FR-005** Buyer opens dispute → escrowed funds frozen for investigation.

- **NFR-001** Dispute tickets freeze escrow immediately (< 500 ms under load), no withdrawals during investigation.
- **NFR-002** All escrow actions recorded in tamper-evident, hash-chained audit log, encrypted at rest.
