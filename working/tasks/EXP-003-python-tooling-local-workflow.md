# EXP-003: Configure Python Tooling And Local Developer Workflow

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Issue type | Task |
| Status | Backlog |
| Priority | P1 |
| Estimate | 2 points |
| Level | Junior |
| Parent epic | EPIC-01: Foundation and First App Concepts |
| Sibling issues | EXP-001, EXP-002, EXP-004 |
| Blocking issues | EXP-001 |
| Blocked issues | EXP-005, EXP-018 |
| Labels | `backend`, `tooling`, `junior-friendly` |
| Component | Tooling |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-003-python-tooling` |
| Suggested PR title | `EXP-003 Configure Python tooling and local workflow` |

## Context

The team needs consistent formatting, linting, and commit hygiene before the
project starts accumulating feature code.

## Scope

- Configure Ruff for formatting and linting.
- Add pre-commit hooks for linting and formatting.
- Add commit message checks.
- Add relevant dev dependencies.
- Update ignore rules for local-only files.

## Non-Goals

- No CI pipeline in this ticket.
- No database tooling.
- No application behavior changes.

## Implementation Notes

- Match the target Python version.
- Keep `.env.example` trackable once it exists, while ignoring real `.env`
  files.
- Prefer checks that are fast enough to run locally before every commit.

## Acceptance Criteria

- `uv run ruff check .` passes.
- `uv run ruff format .` runs successfully.
- Pre-commit hooks are configured and documented.
- Commit message checks are available.
- Local-only files are ignored by git.

## Test Plan

- Run Ruff check and format.
- Run pre-commit against all files after hooks are installed.

## Docs And Team Notes

- README should explain the basic local quality commands.
- If commit conventions become detailed, consider moving them into
  `AGENTS.md`.

## Junior Engineer Guidance

This ticket creates the guardrails. Do not fix unrelated style issues outside
files touched by this task unless the tooling requires it.
