# PRD 001: Initial Django + HTMX Scaffold with Core Security Features

## Problem Statement

I need a portfolio blog that demonstrates real security knowledge to technical recruiters and engineering teams. Most portfolio blogs use modern SPA frameworks (Next.js, React) which, while popular, have larger attack surfaces and more frequent security vulnerabilities. I want something that serves as both a blog AND a security case study — where every architectural decision demonstrates security thinking.

The blog needs to be:
- A functional personal blog for writing technical posts
- Hosted on my own hardware (Raspberry Pi 4B)
- A demonstration of real security knowledge, not buzzwords
- Something I can explain to recruiters as "the blog itself is the security demonstration"

## Solution

Build a Django-based blog using HTMX for interactivity, with security at every layer:

1. **Django + HTMX scaffold**: Server-side rendered templates with HTMX for dynamic interactions, avoiding SPA complexity
2. **Security-first configuration**: Strict CSP, no inline scripts, auto-escaping, secure headers
3. **Authentication with 2FA**: Django's built-in session auth with email-based 2FA for admin access
4. **IP blocking architecture**: Decoupled queue-based system (Django → Redis → Security Worker → nftables) for privilege separation
5. **Markdown-only content**: No HTML sanitization needed — authors write in Markdown only
6. **Redis event queue**: Security events flow through a queue for reliable blocking

The blog posts themselves will document the security decisions, making the blog a recursive demonstration — the architecture explains itself.

## User Stories

### Blog Readers

1. As a blog reader, I want to view published blog posts, so that I can learn from the author's technical writing
2. As a blog reader, I want to see a list of all published posts on the homepage, so that I can browse content
3. As a blog reader, I want to read posts in a clean, readable format, so that I can focus on the content
4. As a blog reader, I want to navigate between posts, so that I can continue reading related content
5. As a blog reader, I want the site to load quickly, so that I have a good user experience

### Blog Author (Admin)

6. As a blog author, I want to log into an admin interface, so that I can create and manage content
7. As a blog author, I want my login to be protected by 2FA, so that my account remains secure even if my password is compromised
8. As a blog author, I want to receive 2FA codes via email, so that I can authenticate without additional apps
9. As a blog author, I want to create new blog posts using Markdown, so that I can write content efficiently
10. As a blog author, I want to edit existing blog posts, so that I can update content with new information
11. As a blog author, I want to delete blog posts, so that I can remove outdated or incorrect content
12. As a blog author, I want to preview posts before publishing, so that I can catch formatting errors
13. As a blog author, I want to save drafts without publishing, so that I can work on posts over time
14. As a blog author, I want to see a list of all my posts (drafts and published), so that I can manage my content
15. As a blog author, I want to be able to logout, so that my session ends securely

### Security & Observability

16. As an administrator, I want failed login attempts to be logged, so that I can detect brute force attacks
17. As an administrator, I want to be alerted after multiple failed logins from an IP, so that I can investigate potential attacks
18. As an administrator, I want IPs with excessive failed logins to be automatically blocked, so that the application is protected
19. As an administrator, I want rate limiting on login endpoints, so that brute force attacks are slowed
20. As an administrator, I want security events to flow through a queue, so that blocking survives restarts
21. As an administrator, I want the blocking system to be privilege-separated, so that a web app compromise cannot directly execute firewall commands
22. As an administrator, I want to receive WhatsApp alerts for security incidents, so that I can respond quickly
23. As an administrator, I want admin actions to be logged for audit, so that I have a record of changes

### Content Management

24. As a blog author, I want to write content in Markdown only, so that I don't need to worry about HTML sanitization
25. As a blog author, I want Markdown to be rendered safely on the frontend, so that readers see formatted content
26. As a blog author, I want code blocks in posts to be syntax-highlighted, so that code is readable
27. As a blog author, I want to include images in posts, so that I can add diagrams and screenshots
28. As a blog author, I want posts to have titles and publication dates, so that content is organized

### Technical/Recruiter Audience

29. As a technical recruiter, I want to see ADRs explaining architectural decisions, so that I understand the candidate's security thinking
30. As a technical recruiter, I want to see evidence of real security implementation, not just configuration, so that I can evaluate the candidate's depth

## Implementation Decisions

### Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Frontend | HTMX + Tailwind CSS | Reduced attack surface vs SPA, server-side rendering |
| Backend | Django | 20+ years of battle-tested security, built-in auth, auto-escaping |
| Database | PostgreSQL | Robust relational database with good security features |
| Server | Gunicorn | Production-grade WSGI server |
| Message Queue | Redis | Lightweight, fast, supports persistence for queue reliability |
| Deployment | Docker on Raspberry Pi 4B | Self-hosted, controllable environment |

### Authentication & Authorization

- **Session-based authentication**: Use Django's built-in session middleware (no JWT complexity)
- **Email-based 2FA**: Use Django's OTP email backend for 2FA (accessible, no app required)
- **Admin-only access**: Only the author needs login; public content is read-only
- **CSRF protection**: All forms include `{% csrf_token %}` token

### Security Configuration

The following Django settings will be configured:

- `SECURE_SSL_REDIRECT = True` — Redirect HTTP to HTTPS
- `SESSION_COOKIE_SECURE = True` — Cookies only over HTTPS
- `CSRF_COOKIE_SECURE = True` — CSRF cookies only over HTTPS
- `SECURE_HSTS_SECONDS = 31536000` — HTTP Strict Transport Security
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- `SECURE_BROWSER_XSS_FILTER = True`
- `SECURE_CONTENT_TYPE_NOSNIFF = True`
- `X_FRAME_OPTIONS = 'DENY'` — Prevent clickjacking

### Content Security Policy

Strict CSP header allowing only necessary sources:

```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; object-src 'none'; base-uri 'self'; form-action 'self'
```

Note: `unsafe-inline` for styles is acceptable because we control all CSS.

### IP Blocking Architecture

Decoupled queue-based system for privilege separation:

```
Django (unprivileged) → Redis (event queue) → Security Worker (privileged) → nftables
```

**Event format** (JSON in Redis queue):
```json
{
  "action": "block" | "unblock" | "alert",
  "ip": "192.168.1.1",
  "reason": "Failed login threshold exceeded",
  "timestamp": "2025-01-15T10:30:00Z",
  "duration": null | "24h"
}
```

**Thresholds**:
- 5 failed logins → Alert only (WhatsApp notification)
- 20 failed logins → Alert + 24-hour IP block
- 10 rate limit violations → Alert only

### Rate Limiting

- Use `django-axe` for login attempt tracking
- Use `django-ratelimit` for general endpoint rate limiting
- Per-IP limits on:
  - Login endpoint: 5 attempts per minute
  - General requests: 100 requests per minute

### Markdown-Only Content

- Post content is stored as Markdown in database
- No HTML input is accepted from authors
- Markdown is rendered server-side using a trusted library
- No HTML sanitization needed because HTML is never accepted

### Template Structure

- Base template with common layout, CSRF token, security headers
- Post list template (homepage)
- Single post template
- Admin login template
- Admin dashboard template (list posts, create, edit, delete)
- HTMX attributes for dynamic interactions where needed

## Testing Decisions

### What Makes a Good Test

Tests should verify **external behavior** and **security properties**, not implementation details. A test is good if:
- It describes behavior in terms a user would understand
- It verifies a security guarantee (e.g., "unauthenticated users cannot access admin")
- It remains valid when implementation changes

### Modules to Test

1. **Authentication views**:
   - Login accepts valid credentials
   - Login rejects invalid credentials
   - Login requires CSRF token
   - 2FA is required after valid password
   - Logout terminates the session

2. **Admin views**:
   - Unauthenticated requests redirect to login
   - Authenticated non-admins are rejected (if multi-user added later)
   - CRUD operations on posts work for authenticated admin

3. **Public views**:
   - Homepage displays published posts
   - Individual post pages render correctly
   - Drafts are not visible to public
   - Markdown renders to safe HTML

4. **Security middleware**:
   - Security headers are present on responses
   - CSP header is correctly set
   - HTTPS redirect is enabled

5. **Rate limiting**:
   - Login endpoint enforces rate limit
   - Exceeding limit returns 429 status

6. **IP blocking queue**:
   - Failed login events are queued
   - Event format matches schema
   - Worker can process queued events

### Prior Art

Given this is a new Django project, tests will follow Django's standard testing patterns:
- `django.test.TestCase` for database tests
- `django.test.Client` for view tests
- Mocking for external services (Redis, email, nftables)

## Out of Scope

The following features are explicitly out of scope for this initial PRD:

- **User registration**: Only the author needs an account; no public user signup
- **Comments**: Blog is read-only for public; no comment system
- **Social features**: No sharing buttons, likes, or social media integration
- **Search**: No search functionality (can be added later)
- **Tags/categories**: Simple post list only (can be extended later)
- **RSS feeds**: Can be added in a later PRD
- **Email subscriptions**: Can be added in a later PRD
- **Multiple authors**: Single-author blog initially
- **Cloudflare Tunnel setup**: Configuration covered in ADR, implementation in separate PRD
- **Security Worker implementation**: Covered in separate PRD
- **OpenClaw WhatsApp integration**: Covered in separate PRD
- **Deployment to Pi**: Covered in separate PRD
- **Blog posts about security**: Writing content is separate from building features

## Further Notes

### Project Structure

```
secure-blog/
├── blog/                # Main Django app
│   ├── models.py        # Post model
│   ├── views.py         # Public and admin views
│   ├── forms.py         # Authentication and post forms
│   ├── templates/      # HTML templates
│   └── urls.py          # URL configuration
├── security/            # Security app (event logging, queue)
│   ├── models.py        # SecurityEvent model
│   ├── queue.py         # Redis queue interface
│   └── middleware.py    # Rate limiting middleware
├── config/              # Django settings
├── docs/
│   ├── adr/             # Architecture Decision Records
│   └── prd/             # Product Requirements Documents
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
```

### Dependencies

Key Python packages to be specified in requirements.txt:
- `django` — Web framework
- `django-htmx` — HTMX integration for Django
- `django-axe` — Login attempt tracking
- `django-ratelimit` — Rate limiting
- `django-otp` — 2FA support
- `gunicorn` — WSGI server
- `redis` — Redis client for queue
- `psycopg2-binary` — PostgreSQL adapter
- `markdown` — Markdown rendering

### Security Posture Throughout Development

When implementing this PRD:
1. Every feature should consider: "What does this look like to an attacker?"
2. Prefer Django defaults over custom implementations
3. Never trust input — even from internal components (validate Redis messages)
4. Log security events — observability is a defense
5. Test security properties, not just happy paths

### Recruiter Pitch

This project serves as a talking point for interviews:

> "Instead of building another Next.js portfolio, I built something that demonstrates real security knowledge. Every architectural decision — from using Django over React to implementing a privilege-separated IP blocking system — is documented with ADRs explaining the trade-offs. The blog itself is the security case study."
