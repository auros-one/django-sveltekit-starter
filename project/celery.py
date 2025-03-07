import os

from celery import Celery

# Set the default Django settings module for the 'celery' program
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# Create Celery app
app = Celery("job-funnel-celery")

# Load config from Django settings (CELERY_ namespace)
app.config_from_object("django.conf:settings", namespace="CELERY")

# Add task routing configuration
app.conf.update(
    flower_basic_auth=os.environ.get("FLOWER_BASIC_AUTH", None),
    flower_url_prefix=os.environ.get("FLOWER_URL_PREFIX", None),
    flower_persistent=True,
    flower_db=os.environ.get("FLOWER_DB", "flower"),
)

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
