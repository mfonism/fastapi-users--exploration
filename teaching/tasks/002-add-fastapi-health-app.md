# 002: Add FastAPI Health App

## Task Metadata

| Field | Value |
|---|---|
| ID | 002 |
| Title | Add FastAPI health app |
| Parent epic | E0: Foundation and tooling |
| Sibling tasks | 001, 003 |
| Blocking tasks | 001 |
| Blocked tasks | 011 |
| Time estimate | 20-30 minutes |
| Difficulty | Beginner |
| Parallelizable | No |
| Suggested labels | `api`, `fastapi`, `beginner` |
| Suggested commit | `feat: add FastAPI health endpoint` |

## Rich Description

Install FastAPI and create the smallest useful API. The first visible behavior
is a health endpoint that returns a stable JSON payload.

## Learning Goal

Students learn how a FastAPI app object is created and how decorators map Python
functions to HTTP routes.

## Files Created Or Modified

- `pyproject.toml`
- `uv.lock`
- `src/explore/app.py`

## Exact Implementation Objective

Add a `FastAPI` app object and a `GET /health` route returning
`{"status": "ok"}`.

## Acceptance Criteria

- `fastapi[standard]` is installed.
- `src/explore/app.py` exports `app`.
- `GET /health` returns status 200.
- The route has no database or auth dependencies.
- The app can be run with `uv run fastapi dev src/explore/app.py`.

## Teaching Notes

This is the first feedback loop. Show the OpenAPI docs and the health endpoint
before adding any infrastructure.

## Code Anchor

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}
```

