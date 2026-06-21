# 001: Scaffold Project

## Task Metadata

| Field | Value |
|---|---|
| ID | 001 |
| Title | Scaffold project |
| Parent epic | E0: Foundation and tooling |
| Sibling tasks | 002, 003 |
| Blocking tasks | None |
| Blocked tasks | 002, 003, 004 |
| Time estimate | 20-30 minutes |
| Difficulty | Beginner |
| Parallelizable | No |
| Suggested labels | `setup`, `beginner`, `infrastructure` |
| Suggested commit | `chore: scaffold python package` |

## Rich Description

Create the project skeleton students will build on for the rest of the
workshop. This should establish an importable Python package, basic project
metadata, ignored local files, and a README placeholder.

## Learning Goal

Students learn what files make a Python project installable and how the `src/`
layout keeps application code separate from tests and tooling.

## Files Created Or Modified

- `.python-version`
- `.gitignore`
- `pyproject.toml`
- `README.md`
- `src/explore/__init__.py`

## Exact Implementation Objective

Create a uv-managed Python package named `explore` with Python 3.14 metadata and
an empty package under `src/explore`.

## Acceptance Criteria

- `pyproject.toml` defines the package name, version, Python requirement, and build backend.
- `.gitignore` excludes virtual environments, caches, build artifacts, local env files, and editor files.
- `src/explore/__init__.py` exists.
- `README.md` has a project title and one-sentence placeholder summary.
- `uv sync` can create the environment.

## Teaching Notes

Explain that this task intentionally has no web framework yet. The goal is a
clean shell where future app code has an obvious place to live.

