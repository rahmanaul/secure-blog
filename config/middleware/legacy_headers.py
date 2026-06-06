"""Legacy security headers that Django doesn't set by default."""


class LegacySecurityHeadersMiddleware:
    """Add legacy security headers like X-XSS-Protection."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # X-XSS-Protection is deprecated but still in acceptance criteria
        response["X-XSS-Protection"] = "1; mode=block"
        return response
