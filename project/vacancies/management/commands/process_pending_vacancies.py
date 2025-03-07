import logging
from textwrap import dedent

from django.core.management.base import BaseCommand

from project.vacancies.tasks import process_pending_vacancies_task

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = dedent(
        """
        Enqueues a Celery task to process all pending ScrapedVacancy records.
        """
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch_size", type=int, default=5000, help="The batch size to process."
        )
        parser.add_argument(
            "--concurrency", type=int, default=100, help="Max concurrent operations."
        )

    def handle(self, *args, **options):
        batch_size = options["batch_size"]
        concurrency = options["concurrency"]
        logger.info(
            f"Enqueueing Celery task: Processing vacancies with batch_size={batch_size}, concurrency={concurrency}"
        )
        process_pending_vacancies_task.delay(batch_size, concurrency)
