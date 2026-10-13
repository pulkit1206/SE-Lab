# Lab 2: Agile Backlog Creation & Sprint Simulation in Jira

**Course:** Software Engineering (UE24CS341A) &mdash; Semester 5, Section F
**Student:** PULKIT BHARDWAJ &mdash; USN `PES1UG24CS346`
**Tool:** Jira (SCRUM, company-managed) &mdash; `SE Project` / `SP board`
**Scenario:** Problem #39 — Second-Hand Product Escrow Marketplace (Lab 1 requirements)
**Date:** 16 September 2026

---

## Deliverables

| # | Deliverable (per handout) | Location |
| --- | --- | --- |
| a | Jira backlog with Epics and User Stories | `screenshots/03_backlog_epics_stories.png` |
| b | Story point assignments | `screenshots/02_active_sprint_board.png`, `screenshots/03_backlog_epics_stories.png` |
| c | Sprint board (Active Sprint view) | `screenshots/02_active_sprint_board.png` |
| d | Burndown Chart | `screenshots/01_burndown_chart.png` |
| e | Brief document answering the reflection questions | [`Reflection.md`](Reflection.md) · `.docx` · `.pdf` |
| — | Combined PDF deliverable (EPICs + sprint + burndown + reflection) | [`Lab2_Deliverables.pdf`](Lab2_Deliverables.pdf) |

---

## What was built

- **Epic:** *Secure Escrow Transaction Flow*.
- **User stories** derived from the Lab 1 functional requirements:

  | Issue | User story | Traces to | Status |
  |-------|-----------|-----------|--------|
  | SP-7 | Story 1.1 — Lock Payment in Escrow | FR-001 | In Progress |
  | SP-8 | Story 1.2 — Order State Transition | FR-001 | To Do |
  | SP-9 | Story 1.3 — Inspector Sign-Off | FR-002 | To Do |
  | SP-10 | Story 1.4 — Fund Release on Approval | FR-003 | Done |
  | SP-11 | Story 1.5 — Dispute Freeze | FR-005 / NFR-001 | Done |

- **Sprint 1** (11–13 Sep 2026, 1-week timebox): five work items pulled from the backlog, progressed
  `To Do → In Progress → Done`, and tracked on the Burndown Chart.
- **Estimation:** Planning Poker on the Fibonacci scale; **prioritisation** High/Medium/Low by user impact.

## Reflection

See [`Reflection.md`](Reflection.md) for the answers to the four reflection questions. Rebuild the
Word/PDF versions with `python3 build_lab2.py`.
