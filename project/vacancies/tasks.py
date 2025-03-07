import logging
import os
from datetime import datetime

from celery import shared_task

from project.vacancies.models import ScrapedVacancy, Status, Vacancy
from project.vacancies.services.dspy.dspy_model_training import (
    generate_examples,
    train_dspy_model,
)
from project.vacancies.services.vacancy_parsing import process_vacancies

logger = logging.getLogger(__name__)


@shared_task
def process_pending_vacancies_task(ids=None, batch_size=5000, concurrency=100):
    """
    Celery task to process pending ScrapedVacancy records.
    """
    # Determine which vacancies to process
    if ids:
        # Process only specific vacancies
        vacancies = ScrapedVacancy.objects.filter(id__in=ids)
        count = vacancies.count()
        logger.info(
            f"[process_pending_vacancies] Processing {count} selected vacancies"
        )
    else:
        # Process all pending vacancies
        vacancies = ScrapedVacancy.objects.filter(status=Status.PENDING)
        count = vacancies.count()
        logger.info(f"[process_pending_vacancies] Processing {count} pending vacancies")

    if count == 0:
        logger.info("[process_pending_vacancies] No vacancies to process")
        return 0

    # Process vacancies in batches for memory efficiency
    batch = []
    processed = 0

    for scraped_vacancy in vacancies.iterator():
        batch.append(scraped_vacancy)
        if len(batch) >= batch_size:
            process_vacancies(batch, max_concurrent=concurrency)
            processed += len(batch)
            logger.info(
                f"[process_pending_vacancies] Processed batch: {processed}/{count}"
            )
            batch = []

    # Process remaining vacancies
    if batch:
        process_vacancies(batch, max_concurrent=concurrency)
        processed += len(batch)

    logger.info(f"[process_pending_vacancies] Done! Processed {processed} vacancies")
    return processed


@shared_task
def optimize_dspy_model_task():
    """
    Celery task to optimize and save the DSPY model.
    """
    vacancies = Vacancy.objects.filter(is_approved=True)
    examples = generate_examples(vacancies)
    model = train_dspy_model(examples)
    model_dir = get_or_create_model_dir()

    # Save latest version
    latest_path = os.path.join(model_dir, "optimized_parser_latest.json")
    model.save(latest_path)
    logger.info("Model saved as optimized_parser_latest.json")

    # Save versioned backup
    versioned_path = os.path.join(
        model_dir, f"optimized_parser_{get_date_string()}.json"
    )
    model.save(versioned_path)
    logger.info(f"Model backup saved as {versioned_path}")


def get_date_string():
    today = datetime.now()
    return today.strftime("%Y_%m_%d_%H_%M")


def get_or_create_model_dir():
    model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    os.makedirs(model_dir, exist_ok=True)
    return model_dir
