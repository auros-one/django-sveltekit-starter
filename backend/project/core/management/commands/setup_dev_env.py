import logging
from textwrap import dedent
from typing import Any

from allauth.account.admin import EmailAddress
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from project.accounts.models import User

logger: logging.Logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help: str = dedent(
        """
        Seeds the database with a default site and admin user for development.
        Creates site 'demo.localhost' accessible at demo.localhost:5173
        """
    ).strip()

    def handle(self, *args: Any, **options: dict[str, Any]) -> None:
        # Create or get demo site
        site, created = Site.objects.get_or_create(
            domain="demo.localhost", defaults={"name": "Demo Site (Development)"}
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Created demo site: {site.domain}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"📝 Demo site already exists: {site.domain}")
            )

        # Create admin user for the demo site
        admin_email = "admin@admin.com"

        try:
            admin_user = User.objects.get(email=admin_email, site=site)
            self.stdout.write(
                self.style.WARNING(
                    f"📝 Admin user already exists: {admin_email} (site: {site.name})"
                )
            )
        except User.DoesNotExist:
            # Create admin user
            admin_user = User.objects.create_superuser(
                email=admin_email, site=site, name="Admin User", password="admin"
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Created admin user: {admin_email} (site: {site.name})"
                )
            )

            # Create email address record for allauth
            EmailAddress.objects.create(
                user=admin_user,
                email=admin_email,
                primary=True,
                verified=True,  # Pre-verify for development
            )
            self.stdout.write(
                self.style.SUCCESS("✅ Created verified email address for admin user")
            )

        self.stdout.write(
            self.style.SUCCESS(
                dedent(
                    f"""
                    🎉 Development environment setup complete!

                    📍 Site: {site.name} ({site.domain})
                    👤 Admin: {admin_email} / admin
                    🌐 Frontend: http://localhost:5173
                    🔧 Backend: http://localhost:8000

                    Username format: {admin_user.username} (internal only)
                    """
                ).strip()
            )
        )
