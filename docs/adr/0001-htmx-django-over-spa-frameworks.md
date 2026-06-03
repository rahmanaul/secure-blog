# ADR 0001: HTMX + Django over SPA Frameworks

## Status

Accepted

## Context

We need a tech stack for a portfolio blog that demonstrates security knowledge. The modern default would be Next.js or React SPA, but these have larger attack surfaces and more frequent CVE reports.

## Decision

Use HTMX + Django with:
- Server-side rendering by default
- Minimal JavaScript (only HTMX library)
- Django's mature security defaults
- Tight coupling between frontend and backend logic

### Why this matters for security

1. **Smaller attack surface**: No client-side routing, hydration, or complex state management
2. **Proven security**: Django has 20+ years of battle-testing; React ecosystem has more CVEs
3. **Simpler mental model**: Less code = fewer bugs

## Alternatives Considered

### Alternative A: Next.js/React SPA
- **Pros**: Modern UX patterns, larger talent pool, more "current" tech
- **Cons**: Larger attack surface, more dependencies, more CVEs, harder to secure
- **Rejected**: Security demonstration outweighs modern aesthetics

### Alternative B: Vanilla HTML + jQuery
- **Pros**: Minimal dependencies
- **Cons**: Outdated patterns, harder to maintain, no HTMX benefits
- **Rejected**: HTMX gives us interactivity without complexity

## Consequences

### Positive
- Fewer JavaScript security vulnerabilities
- Django's built-in CSRF, auth, and escaping work seamlessly
- Easier to explain to recruiters: "I chose reduced attack surface over buzzwords"

### Negative
- Less "modern" looking portfolio to some recruiters
- No client-side routing or state management
- HTMX has smaller community than React

## Implementation Notes

- Use HTMX from CDN or bundle with Tailwind build
- Django templates with `{% csrf_token %}` and auto-escaping
- No inline scripts; HTMX attributes only
