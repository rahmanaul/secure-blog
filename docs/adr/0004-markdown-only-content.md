# ADR 0004: Markdown-Only Content, No Rich HTML

## Status

Accepted

## Context

Blog posts need some formatting capability. Options include rich text editors (with HTML sanitization), Markdown, or plain text. Rich HTML introduces XSS risks and requires careful sanitization.

## Decision

Use Markdown for all content:
- Admin writes posts in Markdown
- Django renders Markdown to HTML safely
- No raw HTML allowed
- No sanitization needed (no HTML to sanitize)

### Security benefits

1. **No XSS risk**: Markdown doesn't allow script tags by default
2. **No sanitization bugs**: We're not trying to strip dangerous HTML
3. **Simple mental model**: Authors write Markdown, renderer handles safety
4. **Future-proof**: If we add comments, they're also Markdown-only

## Alternatives Considered

### Alternative A: Rich text with HTML sanitization (bleach)
- **Pros**: More formatting options, familiar to users
- **Cons**: Sanitization is error-prone, always risks missing edge cases
- **Rejected**: "Sanitize input" approach is fundamentally less safe

### Alternative B: WYSIWYG editor that outputs safe HTML
- **Pros**: Best UX, familiar writing experience
- **Cons**: Still requires sanitization, more dependencies
- **Rejected**: Overkill for a simple blog

### Alternative C: Plain text only
- **Pros**: Absolute simplest
- **Cons**: No formatting at all, hard to read
- **Rejected**: Too restrictive

## Consequences

### Positive
- No XSS vulnerabilities from post content
- No complex sanitization logic
- Comments can use same safe approach
- Markdown is portable

### Negative
- Limited formatting (no custom CSS classes, etc.)
- Some writers prefer WYSIWYG
- Tables/lists require Markdown syntax

## Implementation Notes

- Use Python-Markdown or similar library
- Django templates auto-escape rendered output
- If we add comments later: same Markdown-only approach
- Admin: either raw Markdown textarea or simple Markdown editor
