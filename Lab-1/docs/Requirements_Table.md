# Requirements Table — Second-Hand Product Escrow Marketplace

**Scenario (Problem #39):** A secure peer-to-peer trading marketplace where buyer payments are held in escrow, independent third-party inspectors certify product condition, and funds release only upon buyer sign-off.
**Actors:** Buyer, Inspection Agent

---

## Functional Requirements (FR)

| Req ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|--------|------|-------------|----------|---------------------|-----------|
| FR-001 | Functional | The system shall lock the buyer's payment in escrow on order placement and transition the order state to "Under Inspection" until an inspection agent submits a physical-verification sign-off. | High | Pass: Funds are held in escrow and the order shows state "Under Inspection" immediately after payment; Fail: Funds are released to the seller before dual verification. | Core trust mechanism — guarantees neither party can act alone; prevents premature release of funds. |
| FR-002 | Functional | The system shall allow an inspection agent to submit a certification verdict (approve or reject) with an optional report and photo evidence for a product under inspection. | High | Pass: On submission, the order state transitions to "Certified" (approve) or "Rejected/Disputed" (reject) and the report is stored; Fail: The verdict is accepted without a valid inspection agent session. | Mandatory independent verification of product condition before funds move. |
| FR-003 | Functional | The system shall automatically release escrowed funds to the seller only after the buyer confirms satisfaction (buyer sign-off) and the inspection verdict is "Certified". | High | Pass: Escrow release occurs exactly when both buyer sign-off AND certified verdict exist; Fail: Funds are released when either condition is missing. | Implements the dual-verification (dual sign-off) rule central to escrow. |
| FR-004 | Functional | The system shall compute and auto-deduct an escrow service fee (buyer-side, 5%) from the transaction on successful fund release and issue a digital receipt to the buyer. | Medium | Pass: Fee equals 5.0% of the sale price, deducted only on successful release, and a receipt is generated; Fail: Fee is deducted on failed/cancelled orders or amount is incorrect. | Monetises the platform while keeping the fee predictable and auditable. |
| FR-005 | Functional | The system shall allow the buyer to open a dispute ticket against an order at any point after inspection, freezing the escrowed funds for investigation. | High | Pass: A submitted dispute freezes the escrow balance and disables buyer/seller withdrawals; Fail: Funds remain movable during an active dispute. | Buyer protection — ensures disputed funds are not drained pending resolution. |

---

## Non-Functional Requirements (NFR)

| Req ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|--------|------|-------------|----------|---------------------|-----------|
| NFR-001 | Non-Functional (Performance & Security) | Dispute resolution tickets shall freeze escrow funds immediately and prevent account withdrawals during an active investigation. | High | Pass: Benchmarking confirms escrow freeze is enforced in < 500 ms under simulated peak load and no withdrawal succeeds during investigation; Fail: Funds movement succeeds during an active dispute or freeze exceeds the latency target. | Protects funds the instant a dispute opens; must hold up under load to avoid a race where funds are drained. |
| NFR-002 | Non-Functional (Security) | All escrow transactions, sign-offs, and verdicts shall be recorded in an append-only, tamper-evident audit log and encrypted at rest. | High | Pass: Every escrow action is logged within 1 second with a hash-chained record, and a log-integrity check detects any unauthorised modification; Fail: An action is missing from the log or a modification goes undetected. | Provides auditable proof for disputes and regulator trust; security is a core stakeholder concern. |

---

## Actors & Use Cases (for the Use-Case Diagram)

**Actors:** Buyer, Inspection Agent (primary stakeholders) · Admin — Dispute Resolution (supporting actor)

**Use Cases (UC-01 … UC-05):**
- **UC-01 — Place Order & Pay into Escrow**
- **UC-02 — Inspect & Certify Product** (performed by Inspection Agent)
- **UC-03 — Approve Delivery & Release Funds** (buyer sign-off)
- **UC-04 — Open Dispute**
- **UC-05 — Resolve Dispute**

**Relationships:**
- `UC-03 Approve Delivery & Release Funds` **«include»** → `Process Escrow Release & Fee` (always performed before funds move)
- `UC-02 Inspect & Certify Product` **«extend»** → `Reject Product & Raise Dispute` (optional branch when the inspection fails)
