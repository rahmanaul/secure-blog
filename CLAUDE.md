# Secure Blog — Claude Code Configuration

A portfolio blog demonstrating real security knowledge. Every architectural decision is documented in ADRs.

## Quick Overview

- **Stack**: Django + HTMX + PostgreSQL on Raspberry Pi 4B
- **Security focus**: Session auth, rate limiting, IP blocking, CSP, markdown-only content
- **Documentation**: `CONTEXT.md` for domain language, `docs/adr/` for architecture decisions
- **Repo**: https://github.com/rahmanaul/secure-blog

## Agent skills

### Issue tracker

Issues are tracked in [GitHub Issues](https://github.com/rahmanaul/secure-blog/issues). See `docs/agents/issue-tracker.md`.

### Triage labels

Uses default triage labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout with `CONTEXT.md` and `docs/adr/`. See `docs/agents/domain.md`.
