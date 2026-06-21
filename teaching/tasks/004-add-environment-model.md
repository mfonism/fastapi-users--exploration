# 004: Add Environment Model

## Task Metadata

| Field | Value |
|---|---|
| ID | 004 |
| Title | Add environment model |
| Parent epic | E1: Configuration and database infrastructure |
| Sibling tasks | 005, 006, 007, 008, 009, 010, 011 |
| Blocking tasks | 001 |
| Blocked tasks | 005 |
| Time estimate | 25-35 minutes |
| Difficulty | Beginner |
| Parallelizable | No |
| Suggested labels | `config`, `environment`, `beginner` |
| Suggested commit | `feat: add app environment helpers` |

## Rich Description

Create a small environment module that names the supported application
environments and resolves optional env files.

## Learning Goal

Students learn to replace scattered string literals with a small explicit model
of deployment environments.

## Files Created Or Modified

- `src/explore/env.py`

## Exact Implementation Objective

Define `AppEnv`, aliases like `dev` and `prod`, `normalize_app_env`, and
`resolve_env_files`.

## Acceptance Criteria

- Supported environments are `local`, `test`, `staging`, and `production`.
- Common aliases normalize to those values.
- Unknown environment names raise a clear error.
- Env-file resolution returns `.env` and `.env.<environment>` when present.

## Teaching Notes

Ask students why `test` should not connect to the same database as `local`.

