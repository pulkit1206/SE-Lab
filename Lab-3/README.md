# Lab 3: Component Modelling & Architectural Pattern Selection

**Course:** Software Engineering (UE24CS341A) &mdash; Semester 5, Section F
**Student:** PULKIT BHARDWAJ &mdash; USN `PES1UG24CS346`
**Scenario:** Problem #39 — Second-Hand Product Escrow Marketplace (Lab 1 requirements)
**Date:** 11 September 2026

---

## Deliverables

| # | Deliverable | File |
| --- | --- | --- |
| 1 | UML Component Diagram (microservices, with provided/required interfaces) | [`Component_Diagram.pdf`](Component_Diagram.pdf) |
| 2 | Architecture Selection & Justification | [`Architecture_Justification.pdf`](Architecture_Justification.pdf) |

---

## Summary

- **Architectural style chosen:** Microservices.
- **Six independently deployable services:** API Gateway, Order & Escrow Service, Inspection Service,
  Payment Service, Dispute Resolution Service, Audit Log Service.
- **Justification drivers:** independent scaling and fault isolation for the money-flow services
  (FR-001/FR-003, NFR-001), independent deployability matching the distinct Buyer and Inspection-Agent
  workflows, and security isolation of the tamper-evident audit log (NFR-002).
- **Trade-offs considered:** higher operational complexity vs. a layered monolith — accepted in
  exchange for the hard security and latency guarantees around escrow funds.
