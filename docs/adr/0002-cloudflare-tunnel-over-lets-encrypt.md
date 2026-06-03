# ADR 0002: Cloudflare Tunnel over Let's Encrypt

## Status

Accepted

## Context

The blog will be self-hosted on a Raspberry Pi 4B. We need HTTPS/TLS termination. Options include Let's Encrypt with certbot, self-signed certificates, or Cloudflare Tunnel.

## Decision

Use Cloudflare Tunnel (cloudflared):
- No certificate management on the Pi
- DDoS protection included
- Pi's IP address hidden from internet
- TLS handled by Cloudflare edge
- Blog bound to localhost (127.0.0.1) only

### Security benefits

1. **No exposed attack surface**: Pi is not directly accessible
2. **No cert expiration risk**: Cloudflare handles renewals
3. **DDoS protection**: Cloudflare absorbs attacks before they reach the Pi
4. **IP hiding**: Scanners cannot find the Pi directly

## Alternatives Considered

### Alternative A: Let's Encrypt (certbot)
- **Pros**: Standard approach, full control, free
- **Cons**: Cert expiration risk, exposes Pi IP, no DDoS protection, requires port 80/443 open
- **Rejected**: More complexity, more attack surface

### Alternative B: Self-signed certificates
- **Pros**: No external dependency
- **Cons**: Browser warnings, poor UX, still exposes IP
- **Rejected**: Unusable for a public portfolio

## Consequences

### Positive
- No cert management overhead
- Pi stays hidden and protected
- Simplified architecture

### Negative
- Dependency on Cloudflare (free tier)
- Requires Cloudflare domain
- All traffic routes through Cloudflare (privacy consideration)

## Implementation Notes

- Bind Django/Gunicorn to 127.0.0.1 only
- Use `SECURE_PROXY_SSL_HEADER` in Django settings
- Cloudflare Tunnel handles TLS termination
