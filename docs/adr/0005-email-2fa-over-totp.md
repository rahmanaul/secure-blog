# ADR 0005: Email 2FA over TOTP Apps

## Status

Accepted

## Context

Django admin requires two-factor authentication. Options include TOTP apps (Google Authenticator), hardware keys (YubiKey), or email-based 2FA. For a portfolio blog, we balance security with accessibility.

## Decision

Use email-based 2FA via Resend:
- Admin logs in with password
- 6-digit code sent to email
- Code required to complete login
- Using `django-two-factor-auth` package

### Why email 2FA

1. **Accessibility**: No phone app needed, email is universal
2. **Backup**: Email access = 2FA recovery
3. **Simple setup**: No TOTP scanning, no hardware tokens
4. **Portfolio context**: Demonstrates security awareness without UX barrier

## Alternatives Considered

### Alternative A: TOTP (Google Authenticator, Authy)
- **Pros**: More secure (phishing-resistant), no external dependency
- **Cons**: Requires phone, harder to explain/demo to recruiters
- **Rejected**: Email 2FA is sufficient for our threat model

### Alternative B: Hardware keys (WebAuthn, YubiKey)
- **Pros**: Strongest security, phishing-resistant
- **Cons**: Requires hardware, excludes many users
- **Rejected**: Overkill for personal blog, expensive to demo

### Alternative C: No 2FA (strong password only)
- **Pros**: Simplest setup
- **Cons**: Insufficient for security demonstration
- **Rejected**: Portfolio requires security best practices

## Consequences

### Positive
- 2FA implemented without UX barriers
- Easy to explain: "Check your email"
- Resend API for reliable delivery
- Demonstrates security layering

### Negative
- Email account compromise = blog compromise (accept for personal blog)
- Less phishing-resistant than TOTP
- Dependency on Resend (email delivery)

## Implementation Notes

- `django-two-factor-auth` package
- Resend for transactional email
- API key in `.env` (not in code)
- Email 2FA via `EmailDevice` in django-two-factor-auth
- Backup codes optional (email access = backup)
