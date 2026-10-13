# Deliverables — Lab 1

These files together form the three deliverables required by the assignment:

| Deliverable | File(s) |
|-------------|---------|
| 1. Complete Requirements Table | `Requirements_Table.md` / `Requirements_Table.docx` |
| 2. UML Use-Case Diagram | `Use_Case_Diagram.drawio` (open in draw.io → export as PDF) |
| 3. Use-Case Flow (one page) | `Use_Case_Flow_UC03.md` / `Use_Case_Flow_UC03.docx` |

## Regenerating the Word documents

The `.docx` files are generated from the markdown sources:

```bash
python3 ../build_docs.py
```

Requires `python-docx` (`pip install python-docx`).

## Use-case diagram export

1. Open `Use_Case_Diagram.drawio` in [draw.io](https://app.diagrams.net).
2. File → Export as → PDF (background must be **not** transparent).

## Scenario (Problem #39)

Second-Hand Product Escrow Marketplace — a secure P2P marketplace where buyer payments are held in
escrow, third-party inspectors certify product condition, and funds release only on buyer sign-off.

- **Actors:** Buyer, Inspection Agent (primary) · Admin — Dispute Resolution (supporting)
- **Use cases:** UC-01 Place Order & Pay into Escrow; UC-02 Inspect & Certify Product; UC-03 Approve
  Delivery & Release Funds; UC-04 Open Dispute; UC-05 Resolve Dispute
- **Relationships:** `UC-03 «include» Process Escrow Release & Fee`; `UC-02 «extend» Reject Product & Raise Dispute`
