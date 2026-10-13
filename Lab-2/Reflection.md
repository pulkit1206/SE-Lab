# Lab 2 — Agile Backlog Creation & Sprint Simulation in Jira

## Reflection

**Course:** Software Engineering (UE24CS341A) &mdash; Semester 5, Section F
**Student:** PULKIT BHARDWAJ &mdash; USN `PES1UG24CS346`
**Scenario:** Problem #39 — Second-Hand Product Escrow Marketplace (Lab 1 requirements)

---

### 1. Jira setup

| Item | Value |
|------|-------|
| Project | `SE Project` — SCRUM (company-managed) |
| Board | `SP board` |
| Epic | **Secure Escrow Transaction Flow** |
| Sprint | **Sprint 1** — 11 Sep – 13 Sep 2026 (1-week timebox) |
| Estimation | Planning Poker on the Fibonacci scale |
| Prioritisation | High / Medium / Low by user impact |

**User stories created from the Lab 1 functional requirements** (status shown as captured at the
mid-sprint snapshot):

| Issue | User story | Traces to | Status |
|-------|-----------|-----------|--------|
| SP-7 | Story 1.1 — Lock Payment in Escrow | FR-001 | In Progress |
| SP-8 | Story 1.2 — Order State Transition | FR-001 | To Do |
| SP-9 | Story 1.3 — Inspector Sign-Off | FR-002 | To Do |
| SP-10 | Story 1.4 — Fund Release on Approval | FR-003 | Done |
| SP-11 | Story 1.5 — Dispute Freeze | FR-005 / NFR-001 | Done |

At the snapshot the Active Sprint board read **Done 2 · In Progress 1 · To Do 2**, and the burndown
chart was tracking the remaining story points for Sprint 1.

---

### 2. Reflection questions

**Q1. Did your estimations reflect the actual effort?**

Only partly. The estimates were derived from the *happy path* of each story, so the stories that
looked conceptually simple were sized low. In practice the effort in the escrow domain lives in edge
cases — dual-condition verification before release, rollback when settlement fails, and the
tamper-evident audit write on every state change — none of which were visible when the cards were
first estimated. Sprint 1 finished with only two of five stories in **Done**, with the core escrow
locking story (SP-7) still **In Progress**. That is direct evidence that the money-handling stories
were estimated optimistically; the gap was in unestimated edge-case work, not in the features
themselves.

**Q2. Was your backlog well-prioritized?**

At the epic level, yes. The **Secure Escrow Transaction Flow** epic sequences the stories in strict
dependency order — lock funds → transition order state → inspector sign-off → release funds → dispute
freeze — so no story depends on work scheduled later in the backlog, and the two stories tied to the
hard NFRs (fund release, dispute freeze) were prioritised High. The weakness is housekeeping: the
backlog still carried unused example/template items (the coffee-ordering "Story 1.1 / 1.2" cards
first surfaced by the Jira tutorial) alongside the real escrow stories. They should have been deleted
during grooming — leaving them in inflates the backlog and makes priority ordering ambiguous.

**Q3. How did your simulated sprint align with your plan?**

The timebox and the sprint goal were respected: the sprint ran its fixed 1-week window and the goal
("deliver the escrow transaction flow incrementally") was clear and singular. Where plan and reality
diverged was scope vs. capacity. The plan committed all five stories to Sprint 1, but the snapshot
shows two completed, one in progress and two untouched. Progress did move through the correct flow
(To Do → In Progress → Done) as work was simulated, so the board mechanics matched the plan; the
*velocity assumption* did not. The realistic throughput was closer to two stories per sprint than
five.

**Q4. What insights did the burndown chart give about your team's capacity?**

The burndown line stayed almost flat early in the sprint and then dropped in discrete steps, rather
than declining smoothly toward the grey ideal-progress guide. A stepped burndown means work is only
recognised as done in batches (stories were closed together after review), and a line that sits above
the guideline means the committed scope was larger than capacity. The actionable insight is that the
team's sustainable velocity is below what Sprint 1 committed: the next sprint should pull fewer points
than the raw backlog total and explicitly reserve capacity for the escrow stories that keep slipping,
instead of assuming every high-priority story fits in one timebox.

---

### 3. Traceability to Lab 1

Each Lab 1 functional requirement maps to at least one user story in the epic:

| Lab 1 requirement | Jira user story |
|-------------------|-----------------|
| FR-001 Lock payment in escrow / state → "Under Inspection" | SP-7, SP-8 |
| FR-002 Inspection certification (approve / reject) | SP-9 |
| FR-003 Release funds on dual verification | SP-10 |
| FR-004 Escrow service fee + digital receipt | (carried to next sprint) |
| FR-005 Buyer dispute freezes funds | SP-11 |
| NFR-001 Immediate freeze / no withdrawals during dispute | SP-11 |
| NFR-002 Tamper-evident audit log | cross-cutting (audit writes in SP-7…SP-11) |

---

### 4. Evidence (screenshots)

| File | Shows |
|------|-------|
| `screenshots/03_backlog_epics_stories.png` | Backlog: Epic + user stories (SP-7 … SP-11), story points on the SP board |
| `screenshots/02_active_sprint_board.png` | Active Sprint board — Done 2 / In Progress 1 / To Do 2 |
| `screenshots/01_burndown_chart.png` | Sprint 1 Burndown Chart (Story Points vs. time) |
