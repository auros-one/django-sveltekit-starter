from urllib.parse import urlparse

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class XFrameAllowFrontendDomainsMiddleware(MiddlewareMixin):
    """
    The frontend is allowed to embed the admin site in an iframe.

    Uses Content-Security-Policy header with frame-ancestors directive to control
    which domains can embed this content in iframes, replacing the deprecated X-Frame-Options.
    """

    def process_response(self, request, response):
        referrer = request.headers.get("referer")
        if referrer:
            referrer_netloc = urlparse(referrer).netloc
            allowed_domains = settings.FRONTEND_DOMAINS
            if any(domain.strip() in referrer_netloc for domain in allowed_domains):
                response["Content-Security-Policy"] = (
                    f"frame-ancestors {referrer_netloc}"
                )
            else:
                response["Content-Security-Policy"] = "frame-ancestors 'none'"
        return response
