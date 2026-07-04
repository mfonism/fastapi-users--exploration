# EPIC-01: Foundation And First App Concepts

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Status | Backlog |
| Priority | P1 |
| Milestone | Foundation |
| Labels | `backend`, `tooling`, `developer-experience`, `junior-friendly` |
| Child issues | EXP-001, EXP-002, EXP-003, EXP-004 |
| Blocking epics | None |
| Blocked epics | EPIC-02 |

## Objective

Create the service skeleton, first tested endpoint, development tooling, and a
small user shape before database persistence enters the project.

## Success Criteria

- The project is initialized as a packaged uv application.
- The app can run locally and expose `/health`.
- Python tooling is configured and documented.
- A simple user shape exists with tests and no database dependency.

## Notes For Junior Engineers

This epic creates a reliable workbench and introduces the first domain idea.
Avoid persistence and auth logic here; those have dedicated follow-up issues.
