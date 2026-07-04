# Linear Field Guide

Use this field set when creating issues from the task files.

## Required Fields

| Field | Recommended Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Issue type | Story or Task |
| Status | Backlog until pulled into a cycle |
| Priority | P1 for core path, P2 for polish, P3 for optional hardening |
| Estimate | Use Fibonacci points: 1, 2, 3, 5, 8 |
| Level | Junior, Intermediate, Senior, or Advanced |
| Parent | Epic or parent issue from [epics](epics) |
| Labels | Use component and work-type labels from each task |
| Blocking issues | Copy from each task metadata table |
| Blocked issues | Copy from each task metadata table |

## Recommended Optional Fields

| Field | Use |
|---|---|
| Cycle | Sprint or delivery window |
| Target start | Set when the issue is scheduled |
| Target due | Set when the issue has release pressure |
| Assignee | Engineer owning implementation |
| Reviewer | Engineer expected to review the PR |
| QA owner | Person responsible for manual verification, if any |
| Project milestone | Foundation, Core Auth, Account Management, Recovery, Email Change, Release |
| Component | Config, DB, Auth, Users, Passwords, Reactivation, Email Change, Docs |
| Risk | Low, Medium, High |
| Customer impact | Internal developer, API consumer, security-sensitive |

## Standard Labels

Use consistent labels so the project can be filtered:

- `backend`
- `api`
- `auth`
- `database`
- `migration`
- `tests`
- `docs`
- `tooling`
- `security`
- `junior-friendly`
- `senior-owned`
- `needs-review`
- `stretch`

## Level Guidance

| Level | Meaning |
|---|---|
| Junior | Small or well-bounded work with clear tests and few moving parts. |
| Intermediate | Multi-file work or framework integration with clear patterns nearby. |
| Senior | Infrastructure, architecture, security-sensitive, or high-blast-radius work. |
| Advanced | Complex workflow work that should be split or heavily paired if assigned to students. |

## Priority Guidance

| Priority | Meaning |
|---|---|
| P0 | Urgent production breakage. Avoid for planned work. |
| P1 | Required for core service functionality. |
| P2 | Required before release, but not first-path blocking. |
| P3 | Useful hardening or polish. |

## Estimate Guidance

| Points | Meaning |
|---|---|
| 1 | Small change, low uncertainty, less than half a day. |
| 2 | Focused change, several files, clear pattern. |
| 3 | Standard feature ticket, tests required, some integration. |
| 5 | Multi-layer change or meaningful security edge cases. |
| 8 | Large or risky; consider splitting before assigning to a junior engineer. |

## Description Standard

Every issue should include:

- context
- scope
- non-goals
- implementation notes
- acceptance criteria
- test plan
- dependencies
- rollout or documentation notes
- junior engineer guidance
