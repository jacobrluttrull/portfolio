# CLAUDE.md

Project-specific context lives in `CONTEXT.md`. This file tracks agent-skill configuration.

## Agent skills

### Issue tracker

Issues live in this repo's GitHub Issues (`jacobrluttrull/portfolio`), managed via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary — `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix` — used as-is. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.

### Design overhaul
Current plan is to redesign website with more professional and simple approach while keeping the core features intact. Use the Figma MCP server to help make designs and review them to me first before coding. No coding unless I approve the design.
Put all design files in docs/design (make if not already exists). Gitignore these files. Only for local use. Do not commit to repo. Only commit the exported images of the design files.
