# EXP-002: Add Health Endpoint And First Test

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Issue type | Story |
| Status | Backlog |
| Priority | P1 |
| Estimate | 2 points |
| Level | Junior |
| Parent epic | EPIC-01: Foundation and First App Concepts |
| Sibling issues | EXP-001, EXP-003, EXP-004 |
| Blocking issues | EXP-001 |
| Blocked issues | EXP-003, EXP-004 |
| Labels | `backend`, `api`, `tests`, `junior-friendly` |
| Component | App scaffold |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-002-health-endpoint` |
| Suggested PR title | `EXP-002 Add health endpoint and first test` |

## Context

The service needs the smallest possible FastAPI app and a first test so
students see the app/test feedback loop before deeper infrastructure appears.

## Scope

- Add FastAPI dependency.
- Add `src/explore/app.py`.
- Create a FastAPI `app` object.
- Add `GET /health`.
- Add a test in `tests/` separate from `src/`.

## Non-Goals

- No database setup.
- No auth setup.
- No environment settings.
- No advanced test fixtures.

## Implementation Notes

- The route should return `{"status": "ok"}`.
- Keep the endpoint boring on purpose; its job is to prove the app runs.
- Use a test client appropriate for the current project setup.

## Acceptance Criteria

- `GET /health` returns 200.
- The response body is `{"status": "ok"}`.
- The test passes with `uv run pytest`.
- README explains how to run the app or test the endpoint.

## Test Plan

- Run `uv run pytest`.
- Optionally start the dev server and call `/health` manually.

## Docs And Team Notes

- Update README with the first useful local command.
- If the app startup pattern becomes a convention, consider documenting it in
  `AGENTS.md` later.

## Junior Engineer Guidance

This is the first app behavior. Keep it small and tested. Resist the temptation
to add settings, DB, or auth early.
