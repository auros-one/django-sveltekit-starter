"""
Multi-tenancy middleware using Django Sites framework.
"""

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin


class SiteMiddleware(MiddlewareMixin):
    """
    Middleware to identify and attach site context based on subdomain.

    Subdomain pattern: {site_domain} -> site

    For development: demo.localhost:5173 -> site with domain "demo.localhost"
    For production: client1.example.com -> site with domain "client1.example.com"
    Fallback: localhost:8000 -> first available site (for development convenience)
    """

    def process_request(self, request):
        """Extract site from domain and attach to request."""
        host = request.get_host()

        # Handle port for development
        if ":" in host:
            host_without_port = host.split(":")[0]
        else:
            host_without_port = host

        site = None

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
                                # Default localhost without subdomain - use first available site
                                # This handles localhost:8000 access during development
                                site = Site.objects.first()
                                if not site:
                                    # Create a default site if none exists
                                    site = Site.objects.create(
                                        domain="localhost",
                                        name="Default Development Site",
                                    )
                        else:
                            # Non-localhost development access - use first site
                            site = Site.objects.first()
                            if not site:
                                # Create a default site instead of raising 404
                                site = Site.objects.create(
                                    domain=host_without_port, name="Default Site"
                                )
                    else:
                        # Production: use first site as fallback instead of 404
                        site = Site.objects.first()
                        if not site:
                            raise Http404(f"No sites configured for domain: {host}")

            # Attach site to request
            request.site = site

            # Set current site for Django
            settings.SITE_ID = site.pk

        except Exception as e:
            # In case of any database errors, use a default site to prevent blocking
            if settings.DEBUG:
                # Create or get a default site
                site, created = Site.objects.get_or_create(
                    domain="localhost", defaults={"name": "Default Development Site"}
                )
                request.site = site
                settings.SITE_ID = site.pk
            else:
                # In production, re-raise the exception
                raise e

        # Always return None to continue processing
        return None
