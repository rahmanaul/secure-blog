import pytest


@pytest.mark.django_db
class TestSecurityHeaders:
    """All responses include security headers to protect against vulnerabilities."""

    def test_homepage_has_security_headers(self, client):
        """The homepage includes all required security headers."""
        # Simulate HTTPS request (HSTS only set on secure connections)
        response = client.get("/", secure=True)

        # HSTS with 1-year duration including subdomains and preload
        assert response.get("Strict-Transport-Security") == "max-age=31536000; includeSubDomains; preload"

        # Prevent clickjacking
        assert response.get("X-Frame-Options") == "DENY"

        # Prevent MIME sniffing
        assert response.get("X-Content-Type-Options") == "nosniff"

        # XSS filter enabled
        assert response.get("X-XSS-Protection") == "1; mode=block"

        # CSP header
        csp = response.get("Content-Security-Policy")
        assert csp is not None
        assert "default-src 'self'" in csp
        assert "script-src 'self'" in csp
        assert "style-src 'self' 'unsafe-inline'" in csp
        assert "img-src 'self' data:" in csp
        assert "object-src 'none'" in csp
        assert "base-uri 'self'" in csp
        assert "form-action 'self'" in csp

    def test_single_post_has_security_headers(self, client):
        """Single post pages also include all security headers."""
        # Create a post first
        from blog.models import Post
        from django.utils import timezone
        post = Post.objects.create(
            title="Test Post",
            content="Content...",
            published_at=timezone.now(),
        )

        # Simulate HTTPS request (HSTS only set on secure connections)
        response = client.get(f"/posts/{post.id}/", secure=True)

        # Verify same headers
        assert response.get("Strict-Transport-Security") == "max-age=31536000; includeSubDomains; preload"
        assert response.get("X-Frame-Options") == "DENY"
        assert response.get("X-Content-Type-Options") == "nosniff"
        assert response.get("X-XSS-Protection") == "1; mode=block"
        assert response.get("Content-Security-Policy") is not None
