from django.conf import settings


class CSPMiddleware:
    """Add Content Security Policy header to all responses."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Map setting keys to CSP directive names
        csp_config = {
            'default-src': ('CSP_DEFAULT_SRC', "'self'"),
            'script-src': ('CSP_SCRIPT_SRC', "'self'"),
            'style-src': ('CSP_STYLE_SRC', "'self' 'unsafe-inline'"),
            'img-src': ('CSP_IMG_SRC', "'self' data:"),
            'object-src': ('CSP_OBJECT_SRC', "'none'"),
            'base-uri': ('CSP_BASE_URI', "'self'"),
            'form-action': ('CSP_FORM_ACTION', "'self'"),
        }

        directives = []
        for directive_name, (setting_key, default_value) in csp_config.items():
            value = getattr(settings, setting_key, default_value)
            directives.append(f"{directive_name} {value}")

        response["Content-Security-Policy"] = "; ".join(directives)
        return response
