# Use-Case Flow Specification
## UC-03 — Approve Delivery & Release Funds

**Second-Hand Product Escrow Marketplace (Problem #39)**

---

### Use Case Overview
- **Goal:** The buyer confirms satisfaction with the delivered, certified product so that escrowed funds are released to the seller.
- **Primary Actor:** Buyer
- **Supporting Actors:** Inspection Agent, Payment/Settlement System
- **Preconditions:**
  1. The buyer has placed an order and the payment is locked in escrow (state = "Under Inspection").
  2. An inspection agent has submitted a **"Certified"** verdict (state = "Certified").
  3. The product has been physically delivered to the buyer.
- **Postconditions (success):**
  1. Escrowed funds are released to the seller.
  2. The platform service fee is deducted.
  3. A digital receipt is issued to the buyer.
  4. Order state transitions to "Completed" and is recorded in the audit log.
- **Postconditions (failure):** Funds remain locked in escrow; the order remains in "Certified" state and no fee is charged.

---

### Main Success Scenario
1. The Buyer opens the order and selects **"Approve Delivery & Release Funds"** on an order in "Certified" state.
2. The system displays an order summary: item, price, escrow service fee (5%), and the net amount to release to the seller.
3. The Buyer confirms the release.
4. The system verifies that **both** a "Certified" inspection verdict and the buyer sign-off exist.
5. The system includes **Process Escrow Release & Fee**:
   - 5a. Deducts the 5% service fee from the escrow balance.
   - 5b. Transfers the remaining funds to the seller's account.
6. The system sets the order state to "Completed".
7. The system generates and emails a digital receipt to the Buyer.
8. The system writes an append-only, hash-chained record of the release to the audit log.
9. The use case ends successfully; the Buyer sees a confirmation view.

---

### Alternate Flow
**4a. Inspection verdict is not "Certified" or buyer sign-off is missing**
- 4a1. The system prevents the release and displays a message indicating the required conditions are unmet (e.g., "Order awaiting buyer sign-off" or "Inspection has not been certified").
- 4a2. The escrow funds remain locked (no release, no fee deduction).
- 4a3. The Buyer may resolve the missing condition (e.g., complete sign-off or await inspection) and retry.
- 4a4. If the order is later disputed, the flow is redirected to **UC-04 Open Dispute** and the funds are frozen.

**5b1. Funds transfer to seller fails (settlement error / invalid account)**
- 5b1. The system rolls back the fee deduction and returns the order to "Certified" state with funds still in escrow.
- 5b2. The system notifies the Buyer and the Seller of the failure and retries the transfer up to 2 times before flagging the order for manual settlement.

---

### «include» / «extend» Relationships Used
- **«include» — Process Escrow Release & Fee:** Always executed as part of *Approve Delivery & Release Funds* (step 5) to enforce consistent fee handling and dual-verification.
- **«extend» — Reject Product & Raise Dispute:** The *Inspect & Certify Product* use case may, on a failed inspection, extend into a dispute flow (see UC-04), which is why a release can also be redirected to a dispute in Alternate Flow 4a4.
