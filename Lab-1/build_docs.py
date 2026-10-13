#!/usr/bin/env python3
"""Generate Word (.docx) versions of the Lab 1 deliverables from the markdown sources.

Run:  python3 build_docs.py
Output:  docs/Requirements_Table.docx  and  docs/Use_Case_Flow_UC03.docx
"""
import os
from docx import Document
from docx.shared import Inches
from docx.enum.table import WD_TABLE_ALIGNMENT

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "docs")


# ---------------- Requirements Table ----------------
def requirements_table():
    doc = Document()
    doc.add_heading("Requirements Table — Second-Hand Product Escrow Marketplace", 0)
    doc.add_paragraph("Scenario (Problem #39): A secure peer-to-peer trading marketplace where buyer "
                      "payments are held in escrow, independent third-party inspectors certify product "
                      "condition, and funds release only upon buyer sign-off.")
    p = doc.add_paragraph(); p.add_run("Actors: Buyer, Inspection Agent").bold = True

    doc.add_heading("Functional Requirements", level=1)
    fr = [
        ["FR-001", "Functional",
         'The system shall lock the buyer\'s payment in escrow on order placement and transition the order state to "Under Inspection" until an inspection agent submits a physical-verification sign-off.',
         "High",
         'Pass: Funds are held in escrow and the order shows state "Under Inspection" immediately after payment; Fail: Funds are released to the seller before dual verification.',
         "Core trust mechanism — guarantees neither party can act alone; prevents premature release of funds."],
        ["FR-002", "Functional",
         'The system shall allow an inspection agent to submit a certification verdict (approve or reject) with an optional report and photo evidence for a product under inspection.',
         "High",
         'Pass: On submission, the order state transitions to "Certified" (approve) or "Rejected/Disputed" (reject) and the report is stored; Fail: The verdict is accepted without a valid inspection agent session.',
         "Mandatory independent verification of product condition before funds move."],
        ["FR-003", "Functional",
         'The system shall automatically release escrowed funds to the seller only after the buyer confirms satisfaction (buyer sign-off) and the inspection verdict is "Certified".',
         "High",
         "Pass: Escrow release occurs exactly when both buyer sign-off AND certified verdict exist; Fail: Funds are released when either condition is missing.",
         "Implements the dual-verification (dual sign-off) rule central to escrow."],
        ["FR-004", "Functional",
         "The system shall compute and auto-deduct an escrow service fee (buyer-side, 5%) from the transaction on successful fund release and issue a digital receipt to the buyer.",
         "Medium",
         "Pass: Fee equals 5.0% of the sale price, deducted only on successful release, and a receipt is generated; Fail: Fee is deducted on failed/cancelled orders or amount is incorrect.",
         "Monetises the platform while keeping the fee predictable and auditable."],
        ["FR-005", "Functional",
         "The system shall allow the buyer to open a dispute ticket against an order at any point after inspection, freezing the escrowed funds for investigation.",
         "High",
         "Pass: A submitted dispute freezes the escrow balance and disables buyer/seller withdrawals; Fail: Funds remain movable during an active dispute.",
         "Buyer protection — ensures disputed funds are not drained pending resolution."],
    ]
    build_table(doc, fr)

    doc.add_heading("Non-Functional Requirements", level=1)
    nfr = [
        ["NFR-001", "Non-Functional (Performance & Security)",
         "Dispute resolution tickets shall freeze escrow funds immediately and prevent account withdrawals during an active investigation.",
         "High",
         "Pass: Benchmarking confirms escrow freeze is enforced in < 500 ms under simulated peak load and no withdrawal succeeds during investigation; Fail: Funds movement succeeds during an active dispute or freeze exceeds the latency target.",
         "Protects funds the instant a dispute opens; must hold up under load to avoid a race where funds are drained."],
        ["NFR-002", "Non-Functional (Security)",
         "All escrow transactions, sign-offs, and verdicts shall be recorded in an append-only, tamper-evident audit log and encrypted at rest.",
         "High",
         "Pass: Every escrow action is logged within 1 second with a hash-chained record, and a log-integrity check detects any unauthorised modification; Fail: An action is missing from the log or a modification goes undetected.",
         "Provides auditable proof for disputes and regulator trust; security is a core stakeholder concern."],
    ]
    build_table(doc, nfr)

    doc.add_heading("Actors & Use Cases", level=1)
    doc.add_paragraph("Actors: Buyer, Inspection Agent (primary stakeholders) \u00b7 Admin \u2014 Dispute Resolution (supporting actor)")
    doc.add_paragraph("Use Cases:")
    for uc in ["UC-01 — Place Order & Pay into Escrow",
               "UC-02 — Inspect & Certify Product (Inspection Agent)",
               "UC-03 — Approve Delivery & Release Funds (buyer sign-off)",
               "UC-04 — Open Dispute",
               "UC-05 — Resolve Dispute"]:
        doc.add_paragraph(uc, style="List Bullet")
    doc.add_paragraph("Relationships:")
    doc.add_paragraph('«include»: UC-03 Approve Delivery & Release Funds  →  Process Escrow Release & Fee', style="List Bullet")
    doc.add_paragraph('«extend»: UC-02 Inspect & Certify Product  →  Reject Product & Raise Dispute', style="List Bullet")

    path = os.path.join(DOCS, "Requirements_Table.docx")
    doc.save(path)
    print("Wrote", path)


def build_table(doc, rows):
    tbl = doc.add_table(rows=1, cols=6)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(["Req ID", "Type", "Description", "Priority", "Acceptance Criteria", "Rationale"]):
        c = tbl.rows[0].cells[i]; c.text = h
        c.paragraphs[0].runs[0].bold = True
    for row in rows:
        cells = tbl.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    widths = [0.6, 1.1, 2.6, 0.7, 2.6, 2.0]
    for r in tbl.rows:
        for idx, w in enumerate(widths):
            if idx < len(r.cells):
                r.cells[idx].width = Inches(w)


# ---------------- Use-Case Flow ----------------
def use_case_flow():
    doc = Document()
    doc.add_heading("Use-Case Flow Specification", 0)
    doc.add_heading("UC-03 — Approve Delivery & Release Funds", level=1)
    doc.add_paragraph("Second-Hand Product Escrow Marketplace (Problem #39)")

    doc.add_heading("Use Case Overview", level=2)
    doc.add_paragraph("Goal: The buyer confirms satisfaction with the delivered, certified product so that escrowed funds are released to the seller.")
    doc.add_paragraph("Primary Actor: Buyer")
    doc.add_paragraph("Supporting Actors: Inspection Agent, Payment/Settlement System")

    doc.add_heading("Preconditions", level=2)
    for s in ['1. The buyer has placed an order and the payment is locked in escrow (state = "Under Inspection").',
              '2. An inspection agent has submitted a "Certified" verdict (state = "Certified").',
              "3. The product has been physically delivered to the buyer."]:
        doc.add_paragraph(s)

    doc.add_heading("Postconditions", level=2)
    doc.add_paragraph("Success:")
    doc.add_paragraph("1. Escrowed funds are released to the seller.")
    doc.add_paragraph("2. The platform service fee is deducted.")
    doc.add_paragraph("3. A digital receipt is issued to the buyer.")
    doc.add_paragraph('4. Order state transitions to "Completed" and is recorded in the audit log.')
    doc.add_paragraph('Failure: Funds remain locked in escrow; the order remains in "Certified" state and no fee is charged.')

    doc.add_heading("Main Success Scenario", level=2)
    steps = [
        '1. The Buyer opens the order and selects "Approve Delivery & Release Funds" on an order in "Certified" state.',
        "2. The system displays an order summary: item, price, escrow service fee (5%), and the net amount to release to the seller.",
        "3. The Buyer confirms the release.",
        '4. The system verifies that both a "Certified" inspection verdict and the buyer sign-off exist.',
        "5. The system includes Process Escrow Release & Fee:",
        "    5a. Deducts the 5% service fee from the escrow balance.",
        "    5b. Transfers the remaining funds to the seller's account.",
        '6. The system sets the order state to "Completed".',
        "7. The system generates and emails a digital receipt to the Buyer.",
        "8. The system writes an append-only, hash-chained record of the release to the audit log.",
        "9. The use case ends successfully; the Buyer sees a confirmation view.",
    ]
    for s in steps:
        doc.add_paragraph(s)

    doc.add_heading("Alternate Flow", level=2)
    doc.add_paragraph('4a. Inspection verdict is not "Certified" or buyer sign-off is missing')
    for s in ['4a1. The system prevents the release and displays a message indicating the required conditions are unmet.',
              "4a2. The escrow funds remain locked (no release, no fee deduction).",
              "4a3. The Buyer may resolve the missing condition (e.g., complete sign-off or await inspection) and retry.",
              "4a4. If the order is later disputed, the flow is redirected to UC-04 Open Dispute and the funds are frozen."]:
        doc.add_paragraph(s, style="List Bullet")
    doc.add_paragraph("5b1. Funds transfer to seller fails (settlement error / invalid account)")
    for s in ['5b1. The system rolls back the fee deduction and returns the order to "Certified" state with funds still in escrow.',
              "5b2. The system notifies the Buyer and the Seller and retries the transfer up to 2 times before flagging the order for manual settlement."]:
        doc.add_paragraph(s, style="List Bullet")

    doc.add_heading("«include» / «extend» Relationships Used", level=2)
    doc.add_paragraph("«include» — Process Escrow Release & Fee: Always executed as part of Approve Delivery & Release Funds (step 5) to enforce consistent fee handling and dual-verification.")
    doc.add_paragraph("«extend» — Reject Product & Raise Dispute: The Inspect & Certify Product use case may, on a failed inspection, extend into a dispute flow (see UC-04).")

    path = os.path.join(DOCS, "Use_Case_Flow_UC03.docx")
    doc.save(path)
    print("Wrote", path)


if __name__ == "__main__":
    requirements_table()
    use_case_flow()
