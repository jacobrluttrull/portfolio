# CLAUDE.md

Project-specific context lives in `CONTEXT.md`. This file tracks agent-skill configuration.

## Agent skills

### Issue tracker

Issues live in this repo's GitHub Issues (`jacobrluttrull/portfolio`), managed via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary — `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix` — used as-is. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
