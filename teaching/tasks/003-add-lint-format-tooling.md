# 003: Add Lint And Format Tooling

## Task Metadata

| Field | Value |
|---|---|
| ID | 003 |
| Title | Add lint and format tooling |
| Parent epic | E0: Foundation and tooling |
| Sibling tasks | 001, 002 |
| Blocking tasks | 001 |
| Blocked tasks | 009 |
| Time estimate | 20-30 minutes |
| Difficulty | Beginner |
| Parallelizable | No |
| Suggested labels | `tooling`, `ruff`, `pre-commit` |
| Suggested commit | `chore: configure ruff and pre-commit` |

## Rich Description

Add Ruff and pre-commit so formatting and linting become automatic early in the
course. This avoids style churn later when many feature files are created.

## Learning Goal

Students learn how a project can encode formatting and linting rules instead of
relying on individual editor settings.

## Files Created Or Modified

- `pyproject.toml`
- `.pre-commit-config.yaml`
- `uv.lock`

## Exact Implementation Objective

Configure Ruff with line length 88, Python 3.14 target, and lint rules matching
the final codebase. Add pre-commit hooks for `ruff` and `ruff-format`.

## Acceptance Criteria

- Ruff is listed in the dev dependency group.
- `pyproject.toml` contains `[tool.ruff]` and `[tool.ruff.lint]`.
- `.pre-commit-config.yaml` runs Ruff lint and format hooks.
- `uv run ruff check .` succeeds.
- `uv run ruff format .` succeeds.

## Teaching Notes

Keep this task short. The point is the workflow, not memorizing lint codes.

