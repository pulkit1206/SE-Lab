#!/usr/bin/env python3
"""Build the Lab 2 deliverable documents from the reflection content.

Run:  python3 build_lab2.py
Outputs:
  Reflection.docx              -- Word version of the reflection deliverable
  Reflection.pdf               -- PDF version of the reflection deliverable
  Lab2_Deliverables.pdf        -- cover + reflection + Jira screenshots (EPICs / sprint / burndown)

Requires: python-docx, reportlab (Pillow for image sizing).
"""
import os
from docx import Document
from docx.shared import Inches

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image, PageBreak)
from reportlab.lib import colors
from PIL import Image as PILImage

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "screenshots")

TITLE = "Lab 2 \u2014 Agile Backlog Creation & Sprint Simulation in Jira"
SUB = ("Software Engineering (UE24CS341A) \u2014 Semester 5, Section F\n"
       "PULKIT BHARDWAJ \u2014 USN PES1UG24CS346\n"
       "Scenario: Problem #39 \u2014 Second-Hand Product Escrow Marketplace")

SETUP = [
    ("Project", "SE Project \u2014 SCRUM (company-managed)"),
    ("Board", "SP board"),
    ("Epic", "Secure Escrow Transaction Flow"),
    ("Sprint", "Sprint 1 \u2014 11 Sep \u2013 13 Sep 2026 (1-week timebox)"),
    ("Estimation", "Planning Poker on the Fibonacci scale"),
    ("Prioritisation", "High / Medium / Low by user impact"),
]

STORIES = [
    ["Issue", "User story", "Traces to", "Status"],
    ["SP-7", "Story 1.1 \u2014 Lock Payment in Escrow", "FR-001", "In Progress"],
    ["SP-8", "Story 1.2 \u2014 Order State Transition", "FR-001", "To Do"],
    ["SP-9", "Story 1.3 \u2014 Inspector Sign-Off", "FR-002", "To Do"],
    ["SP-10", "Story 1.4 \u2014 Fund Release on Approval", "FR-003", "Done"],
    ["SP-11", "Story 1.5 \u2014 Dispute Freeze", "FR-005 / NFR-001", "Done"],
]

QA = [
    ("Q1. Did your estimations reflect the actual effort?",
     "Only partly. The estimates were derived from the happy path of each story, so the stories that "
     "looked conceptually simple were sized low. In practice the effort in the escrow domain lives in "
     "edge cases \u2014 dual-condition verification before release, rollback when settlement fails, and the "
     "tamper-evident audit write on every state change \u2014 none of which were visible when the cards were "
     "first estimated. Sprint 1 finished with only two of five stories in Done, with the core escrow "
     "locking story (SP-7) still In Progress. That is direct evidence that the money-handling stories "
     "were estimated optimistically; the gap was in unestimated edge-case work, not in the features "
     "themselves."),
    ("Q2. Was your backlog well-prioritized?",
     "At the epic level, yes. The Secure Escrow Transaction Flow epic sequences the stories in strict "
     "dependency order \u2014 lock funds \u2192 transition order state \u2192 inspector sign-off \u2192 release funds \u2192 "
     "dispute freeze \u2014 so no story depends on work scheduled later in the backlog, and the two stories "
     "tied to the hard NFRs (fund release, dispute freeze) were prioritised High. The weakness is "
     "housekeeping: the backlog still carried unused example/template items (the coffee-ordering "
     "\u201cStory 1.1 / 1.2\u201d cards first surfaced by the Jira tutorial) alongside the real escrow stories. "
     "They should have been deleted during grooming \u2014 leaving them in inflates the backlog and makes "
     "priority ordering ambiguous."),
    ("Q3. How did your simulated sprint align with your plan?",
     "The timebox and the sprint goal were respected: the sprint ran its fixed 1-week window and the "
     "goal (\u201cdeliver the escrow transaction flow incrementally\u201d) was clear and singular. Where plan and "
     "reality diverged was scope vs. capacity. The plan committed all five stories to Sprint 1, but the "
     "snapshot shows two completed, one in progress and two untouched. Progress did move through the "
     "correct flow (To Do \u2192 In Progress \u2192 Done) as work was simulated, so the board mechanics matched the "
     "plan; the velocity assumption did not. The realistic throughput was closer to two stories per "
     "sprint than five."),
    ("Q4. What insights did the burndown chart give about your team's capacity?",
     "The burndown line stayed almost flat early in the sprint and then dropped in discrete steps, "
     "rather than declining smoothly toward the grey ideal-progress guide. A stepped burndown means "
     "work is only recognised as done in batches (stories were closed together after review), and a "
     "line that sits above the guideline means the committed scope was larger than capacity. The "
     "actionable insight is that the team's sustainable velocity is below what Sprint 1 committed: the "
     "next sprint should pull fewer points than the raw backlog total and explicitly reserve capacity "
     "for the escrow stories that keep slipping, instead of assuming every high-priority story fits in "
     "one timebox."),
]

TRACE = [
    ["Lab 1 requirement", "Jira user story"],
    ["FR-001 Lock payment / state \u2014 Under Inspection", "SP-7, SP-8"],
    ["FR-002 Inspection certification (approve / reject)", "SP-9"],
    ["FR-003 Release funds on dual verification", "SP-10"],
    ["FR-004 Escrow service fee + digital receipt", "(carried to next sprint)"],
    ["FR-005 Buyer dispute freezes funds", "SP-11"],
    ["NFR-001 Immediate freeze / no withdrawals", "SP-11"],
    ["NFR-002 Tamper-evident audit log", "cross-cutting (SP-7\u2026SP-11)"],
]

SHOT_CAPTIONS = [
    ("01_burndown_chart.png", "Sprint 1 Burndown Chart (Story Points vs. time)"),
    ("02_active_sprint_board.png", "Active Sprint board \u2014 Done 2 / In Progress 1 / To Do 2"),
    ("03_backlog_epics_stories.png", "Backlog \u2014 Epic + user stories (SP-7 \u2026 SP-11) and story points"),
]


# --------------------------------------------------------------------------- #
# Word
# --------------------------------------------------------------------------- #
def build_docx():
    doc = Document()
    doc.add_heading(TITLE, 0)
    for line in SUB.split("\n"):
        p = doc.add_paragraph(line)
        p.runs[0].bold = line.startswith("PULKIT")

    doc.add_heading("1. Jira setup", level=1)
    t = doc.add_table(rows=0, cols=2)
    for k, v in SETUP:
        cells = t.add_row().cells
        cells[0].text = k
        cells[1].text = v
    doc.add_paragraph()
    doc.add_paragraph("User stories created from the Lab 1 functional requirements "
                      "(status at the mid-sprint snapshot):")
    st = doc.add_table(rows=len(STORIES), cols=4)
    for r, row in enumerate(STORIES):
        for c, val in enumerate(row):
            st.rows[r].cells[c].text = val
            if r == 0:
                st.rows[r].cells[c].paragraphs[0].runs[0].bold = True

    doc.add_heading("2. Reflection questions", level=1)
    for q, a in QA:
        doc.add_heading(q, level=2)
        doc.add_paragraph(a)

    doc.add_heading("3. Traceability to Lab 1", level=1)
    tt = doc.add_table(rows=len(TRACE), cols=2)
    for r, row in enumerate(TRACE):
        for c, val in enumerate(row):
            tt.rows[r].cells[c].text = val
            if r == 0:
                tt.rows[r].cells[c].paragraphs[0].runs[0].bold = True

    doc.add_heading("4. Evidence (screenshots)", level=1)
    for fname, cap in SHOT_CAPTIONS:
        doc.add_paragraph(cap, style="List Bullet")
        doc.add_picture(os.path.join(SHOTS, fname), width=Inches(6.0))

    out = os.path.join(HERE, "Reflection.docx")
    doc.save(out)
    print("Wrote", out)


# --------------------------------------------------------------------------- #
# PDF helpers
# --------------------------------------------------------------------------- #
def styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle("Center", parent=ss["Normal"], alignment=TA_CENTER))
    ss.add(ParagraphStyle("H1x", parent=ss["Heading1"], spaceBefore=14, spaceAfter=6))
    ss.add(ParagraphStyle("H2x", parent=ss["Heading2"], spaceBefore=10, spaceAfter=4,
                          textColor=colors.HexColor("#1a3d6d")))
    return ss


def grid(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3d6d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9bb3cc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef3f9")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def reflection_flow(ss):
    fl = [Paragraph(TITLE, ss["Title"]), Spacer(1, 6)]
    for line in SUB.split("\n"):
        fl.append(Paragraph(line, ss["Center"]))
    fl.append(Spacer(1, 14))

    fl.append(Paragraph("1. Jira setup", ss["H1x"]))
    fl.append(grid([[k, v] for k, v in SETUP], [4 * cm, 12 * cm]))
    fl.append(Spacer(1, 8))
    fl.append(Paragraph("User stories created from the Lab 1 functional requirements "
                        "(status at the mid-sprint snapshot):", ss["Normal"]))
    fl.append(Spacer(1, 4))
    fl.append(grid(STORIES, [1.6 * cm, 7.6 * cm, 3.4 * cm, 2.6 * cm]))

    fl.append(Paragraph("2. Reflection questions", ss["H1x"]))
    for q, a in QA:
        fl.append(Paragraph(q, ss["H2x"]))
        fl.append(Paragraph(a, ss["Normal"]))

    fl.append(Paragraph("3. Traceability to Lab 1", ss["H1x"]))
    fl.append(grid(TRACE, [9 * cm, 6 * cm]))
    return fl


def build_reflection_pdf():
    ss = styles()
    doc = SimpleDocTemplate(os.path.join(HERE, "Reflection.pdf"), pagesize=A4,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                            title="Lab 2 Reflection")
    doc.build(reflection_flow(ss))
    print("Wrote", os.path.join(HERE, "Reflection.pdf"))


def build_deliverables_pdf():
    ss = styles()
    doc = SimpleDocTemplate(os.path.join(HERE, "Lab2_Deliverables.pdf"), pagesize=A4,
                            leftMargin=1.6 * cm, rightMargin=1.6 * cm,
                            topMargin=1.6 * cm, bottomMargin=1.6 * cm,
                            title="Lab 2 Deliverables")
    fl = reflection_flow(ss)
    fl.append(PageBreak())
    fl.append(Paragraph("4. Evidence (screenshots)", ss["H1x"]))
    avail = A4[0] - 3.2 * cm
    for fname, cap in SHOT_CAPTIONS:
        p = os.path.join(SHOTS, fname)
        iw, ih = PILImage.open(p).size
        w = min(avail, 26 * cm)
        h = w * ih / iw
        if h > A4[1] - 6 * cm:
            h = A4[1] - 6 * cm
            w = h * iw / ih
        fl.append(Paragraph(cap, ss["H2x"]))
        fl.append(Image(p, width=w, height=h))
        fl.append(Spacer(1, 10))
    doc.build(fl)
    print("Wrote", os.path.join(HERE, "Lab2_Deliverables.pdf"))


if __name__ == "__main__":
    build_docx()
    build_reflection_pdf()
    build_deliverables_pdf()
