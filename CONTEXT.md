# CONTEXT — Secure Blog Domain Language

## Purpose

A portfolio blog demonstrating real security knowledge to recruiters and technical audiences. The blog itself is the security case study.

## Core Concepts

### Security Events
Events that are logged and may trigger alerts or blocking actions.

| Event Type | Description | Threshold for Action |
|------------|-------------|---------------------|
| Failed login | Invalid username/password attempt | 5 failures → alert, 20 failures → block |
| Rate limit exceeded | Request rate limit triggered | 10 exceedances → alert |
| Admin action | Create/edit/delete post by admin | Logged for audit |
| Suspicious pattern | Aggregated anomalous behavior | Triggers alert |

### Blocking
The act of preventing an IP address from accessing the application.

- **Alert-only**: Logging and notification without blocking
- **Timeout**: Temporary blocking with expiration
- **Block**: Permanent blocking until manually removed

### Security Incident
A security event that requires human investigation or response.

### Rate Limiting
Per-IP or per-user limits on request frequency to prevent abuse and brute force attacks.

### Trusted Sources
External systems that supply security-relevant data:

- **Renovate**: Automated dependency update PRs
- **pip-audit**: Python package vulnerability scanner
- **Trivy**: Container/filesystem vulnerability scanner
- **GitHub Security Advisories**: CVE monitoring
- **OpenClaw**: WhatsApp alert delivery
- **Resend**: Transactional email for 2FA

## Architecture

### Request Flow (Normal)
```
Browser → Cloudflare → Cloudflare Tunnel → Django (Gunicorn) → Postgres
```

### Request Flow (Static Files)
```
Browser → Cloudflare (cache) → Cloudflare Tunnel → Django → WhiteNoise
```

### Security Event Flow
```
Django → Redis (event queue) → Security Worker → nftables → IP blocked
```

### Alert Flow
```
Django → OpenClaw → WhatsApp (admin notification)
```

## Security Principles

1. **Defense in depth**: Multiple layers of security (CSP + escaping + input validation)
2. **Never trust**: Even internal messages (Redis) are treated as untrusted input
3. **Established over custom**: Use battle-tested packages (Django auth) over custom implementations
4. **Privilege separation**: Unprivileged Django → privileged Security Worker
5. **Escape output, not sanitize input**: Django templates auto-escape by default
