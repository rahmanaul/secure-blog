# Secure Blog — Portfolio Project with Real Security

A portfolio blog that **is** the security demonstration.

## What This Is

A personal blog hosted on a Raspberry Pi 4B that demonstrates real security knowledge to recruiters. Every architectural decision is explained in ADRs. The blog itself is the case study.

## Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTMX + Tailwind CSS (built, not CDN) |
| Backend | Django |
| Database | PostgreSQL (Docker on Pi) |
| Server | Gunicorn |
| SSL/TLS | Cloudflare Tunnel |
| Deployment | Docker on Raspberry Pi 4B |

## Security Architecture

```
Browser → Cloudflare → Cloudflare Tunnel → Django → Postgres
                                              ↓
                                          Redis Queue → Security Worker → nftables
```

## Key Security Features

- **Session-based auth** with Django built-in (no custom crypto)
- **Rate limiting** via Django Axe and Django Ratelimit
- **IP blocking** via Redis → Security Worker → nftables
- **Strict CSP** (no inline scripts, minimal sources)
- **Markdown-only content** (no HTML sanitization needed)
- **Email 2FA** for Django admin
- **Auto-escaping** Django templates (no `|safe` unless necessary)
- **Dependency scanning** via Renovate, Trivy, pip-audit
- **Logging** with OpenClaw WhatsApp alerts

## Documentation

- `CONTEXT.md` — Domain language and core concepts
- `docs/adr/` — Architecture Decision Records explaining each choice

## ADRs

| # | Title | Summary |
|---|-------|---------|
| 0001 | HTMX + Django over SPA Frameworks | Reduced attack surface over modern UX |
| 0002 | Cloudflare Tunnel over Let's Encrypt | Simplicity and DDoS protection |
| 0003 | IP Blocking Architecture | Privilege separation via queue |
| 0004 | Markdown-Only Content | No HTML sanitization needed |
| 0005 | Email 2FA over TOTP | Accessibility over maximum security |

## How to Explain This to Recruiters

> "Instead of building another Next.js blog, I built something that demonstrates real security knowledge. Every layer — from framework choice to IP blocking architecture — is documented with ADRs explaining the trade-offs. The blog itself is the security case study."

## Next Steps

1. Scaffold Django project with HTMX
2. Configure security settings
3. Implement auth with 2FA
4. Build Redis queue and security worker
5. Deploy to Pi
6. Write blog posts about the security decisions
