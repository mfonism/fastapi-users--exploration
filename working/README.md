# Working Plan: Explore Auth API

This directory reframes the repository as professional delivery work that can
also be used with students. It is written in a Linear/GitHub-Issue style, but
the order is intentionally educational: each task introduces a concept before
later tasks depend on it.

The current repository is treated as the target state, but the roadmap rebuilds
that target in a sequence that makes sense to learners.

## Directory Layout

| Path | Purpose |
|---|---|
| [project-brief.md](project-brief.md) | Product, technical, and delivery context. |
| [linear-field-guide.md](linear-field-guide.md) | Recommended fields for Linear issues. |
| [definition-of-ready-done.md](definition-of-ready-done.md) | Team rules for when work is ready to start and done. |
| [epics](epics) | Milestone grouping for the classroom work simulation. |
| [tasks](tasks) | Implementation tickets ordered by learning dependency. |

## Teaching And Delivery Shape

| Classroom Need | Roadmap Choice |
|---|---|
| Students should meet concepts in a useful order. | Define a simple user shape before database persistence. |
| Some infrastructure is too senior-heavy for early tickets. | Keep DB/Alembic setup as a senior-owned ticket with clear constraints. |
| Students should see real workplace artifacts. | Keep Linear-style metadata, acceptance criteria, test plans, and PR titles. |
| Later decisions should not appear from nowhere. | Track deferred work in non-goals and downstream tickets. |

## After Every Issue

Each issue should end by asking:

- Does this change the README?
- Should any team convention move into `AGENTS.md`?
- Should any repeated workflow become a Codex skill or local guide?

It is acceptable for an issue to say "no docs change needed", but the question
should be asked deliberately.

## Recommended Linear Setup

Create one Linear project:

- **Project:** Explore Auth API
- **Team:** Backend
- **Project status:** Planned
- **Priority:** P1 for core auth and persistence, P2 for polish and docs
- **Target:** Internal API service implementation

Create these epics or parent issues:

1. Foundation and First App Concepts
2. Persistence and Test Infrastructure
3. Core Authentication
4. Account Self-Service
5. Recovery and Reactivation
6. Email Change Workflow
7. API Contract and Documentation

Then import or create the task files in [tasks](tasks).

## Suggested Delivery Order

1. Initialize the packaged project.
2. Add the first endpoint and test.
3. Add local tooling.
4. Define the first user shape without persistence.
5. Add senior-owned database, Alembic, commands, and test infrastructure.
6. Turn the user shape into a SQLAlchemy-backed model.
7. Add account-state behavior and factories.
8. Integrate `fastapi-users`, Redis auth, and generated routers.
9. Build registration, verification, login, logout, and current-user behavior.
10. Build account self-service, recovery, reactivation, and email-change flows.
11. Finalize OpenAPI, README, and release checks.
