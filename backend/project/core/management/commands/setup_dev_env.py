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
        Seeds the database with an admin user that is a physician and owner of their practice
        """
    ).strip()

    def handle(self, *args: Any, **options: dict[str, Any]) -> None:
        user = User.objects.create_superuser(
            email="admin@admin.com",
            name="Admin",
            password="admin",
        )
        EmailAddress.objects.create(
            user=user, email=user.email, primary=True, verified=True
        )

        site = Site.objects.first()
        assert site
        site.domain = "localhost:5173"
        site.name = "Template Project"
        site.save()
