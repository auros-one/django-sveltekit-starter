import logging
from textwrap import dedent

from django.core.management.base import BaseCommand

from project.vacancies.tasks import optimize_dspy_model_task

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = dedent(
        """
        Enqueues a Celery task to optimize and save the DSPY model for approved vacancies.
        """
    )

    def handle(self, *args, **options):
        logger.info("Enqueueing Celery task: DSPY model optimization.")
        optimize_dspy_model_task.delay()
