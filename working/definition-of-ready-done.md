# Definition Of Ready And Done

## Definition Of Ready

An issue is ready to start when:

- the title describes the deliverable, not just the activity
- the parent epic is set
- blockers are listed
- files or modules likely to change are listed
- acceptance criteria are concrete and testable
- test expectations are clear
- non-goals are explicit
- security-sensitive behavior is called out
- a junior engineer can explain the expected outcome before starting

## Definition Of Done

An issue is done when:

- implementation matches the scope
- acceptance criteria are satisfied
- relevant tests are added or updated
- existing tests pass locally, or failures are documented
- Ruff passes on changed Python files
- migrations are included for schema changes
- `src/explore/db/registry.py` imports any new SQLAlchemy model
- README or docs are updated when setup or behavior changes
- PR description includes test evidence
- reviewer questions are resolved

## PR Checklist

Use this checklist in each PR:

- [ ] Scope matches the issue.
- [ ] Tests added or updated.
- [ ] Migrations included when DB schema changes.
- [ ] Auth/security edge cases considered.
- [ ] No secrets committed.
- [ ] Public schemas do not expose internal fields.
- [ ] Error details are stable and documented where needed.
- [ ] Local commands run and results are pasted into the PR.

## Junior Engineer Handoff Checklist

Before assigning a ticket to a junior engineer, make sure they know:

- which files to inspect first
- which test file should fail before implementation
- which command verifies the ticket
- what not to change
- who to ask for review

