"""
Multi-tenancy middleware using Django Sites framework.
"""

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin


class SiteMiddleware(MiddlewareMixin):
    """
    Middleware to identify and attach site context.

    Site determination order:
    1. X-Tenant-Domain header (for development/API clients)
    2. Host header domain matching
    3. Subdomain extraction from host
    4. Fallback to default site

    For development with separate frontend:
    - Frontend sends X-Tenant-Domain: demo.localhost
    - Backend uses that to determine the site

    For production:
    - Each tenant has its own domain
    - Site is determined by the actual domain
    """

    def process_request(self, request):
        """Extract site from domain/headers and attach to request."""
        site = None

        # First, check for X-Tenant-Domain header (useful for development)
        tenant_domain = request.headers.get("x-tenant-domain")

        if tenant_domain:
            try:
                site = Site.objects.get(domain=tenant_domain)
            except Site.DoesNotExist:
                if settings.DEBUG:
                    # Auto-create site in development
                    site = Site.objects.create(
                        domain=tenant_domain, name=f"{tenant_domain} (Auto-created)"
                    )

        # If no site from header, use host-based detection
        if not site:
            host = request.get_host()

            # Handle port for development
            if ":" in host:
                host_without_port = host.split(":")[0]
            else:
                host_without_port = host

            try:
                # Try to get site by exact domain match first
                try:
                    site = Site.objects.get(domain=host)
                except Site.DoesNotExist:
                    try:
                        # Try without port for development
                        site = Site.objects.get(domain=host_without_port)
                    except Site.DoesNotExist:
                        # Check if this is a development environment
                        if settings.DEBUG:
                            if "localhost" in host_without_port:
                                # Extract subdomain from localhost
                                parts = host_without_port.split(".")
                                if len(parts) >= 2:  # e.g., "demo.localhost"
                                    subdomain = parts[0]
                                    # Create development site if it doesn't exist
                                    site, created = Site.objects.get_or_create(
                                        domain=f"{subdomain}.localhost",
                                        defaults={"name": f"{subdomain.title()} (Dev)"},
                                    )
                                else:
                                    # Default localhost without subdomain
                                    # For development, default to demo.localhost
                                    site = Site.objects.get_or_create(
                                        domain="demo.localhost",
                                        defaults={"name": "Demo Site (Development)"},
                                    )[0]
                            else:
                                # Non-localhost development access
                                site = Site.objects.get_or_create(
                                    domain="demo.localhost",
                                    defaults={"name": "Demo Site (Development)"},
                                )[0]
                        else:
                            # Production: strict domain matching
                            raise Http404(f"No site configured for domain: {host}")

            except Exception as e:
                # In case of any database errors
                if settings.DEBUG:
                    # Use demo site as fallback in development
                    site = Site.objects.get_or_create(
                        domain="demo.localhost",
                        defaults={"name": "Demo Site (Development)"},
                    )[0]
                else:
                    # In production, re-raise the exception
                    raise e

        # Attach site to request
        request.site = site

        # Set current site for Django (for compatibility)
        settings.SITE_ID = site.pk

        # Always return None to continue processing
        return None
