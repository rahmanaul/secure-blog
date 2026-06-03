# ADR 0003: IP Blocking Architecture (Redis + Worker + nftables)

## Status

Accepted

## Context

When security events occur (failed logins, rate limit breaches), we need to block malicious IPs. Django could execute firewall commands directly, but this is dangerous and violates privilege separation.

## Decision

Use a decoupled architecture:

```
Django (unprivileged) → Redis (event queue) → Security Worker (privileged) → nftables
```

### Why this architecture

1. **Never trust**: Django treats Redis messages as untrusted input
2. **Privilege separation**: Django runs unprivileged; only worker touches firewall
3. **Defense in depth**: Worker validates everything again before blocking
4. **Reliability**: Queue survives restarts; no lost blocks

## Alternatives Considered

### Alternative A: Django executes iptables/nftables directly
- **Pros**: Simpler, fewer moving parts
- **Cons**: Django needs root, command injection risk, fragile
- **Rejected**: Security risk outweighs simplicity

### Alternative B: NGINX-level blocking only
- **Pros**: No firewall interaction
- **Cons**: NGINX blocking is less permanent, harder to manage
- **Rejected**: Firewall-level blocking is more robust

### Alternative C: fail2ban-style log monitoring
- **Pros**: Battle-tested approach
- **Cons**: Tightly coupled to log format, less flexible
- **Rejected**: Our queue-based approach is more maintainable

## Consequences

### Positive
- Django can't compromise the firewall (no direct access)
- Validation happens twice (Django and worker)
- Queue survives restarts
- Clean separation of concerns

### Negative
- More moving parts (Redis, worker)
- Requires Redis persistence for reliability
- More complex to debug

## Implementation Notes

- Django writes to Redis queue: `{"action": "block", "ip": "1.2.3.4", "reason": "..."}`
- Worker reads queue, validates IP format, executes nftables command
- nftables uses sets for atomic updates
- OpenClaw handles alert delivery via WhatsApp

## Thresholds

| Event | Alert | Block |
|-------|-------|-------|
| Failed login (5+) | ✅ | ❌ |
| Failed login (20+) | ✅ | ✅ |
| Rate limit (10+) | ✅ | ❌ |
