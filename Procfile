release: python manage.py migrate --noinput
web: gunicorn project.wsgi:application
worker: celery -A project worker --loglevel=info --autoscale=2,1
beat: celery -A project beat --loglevel=info
flower: celery -A project flower --address=0.0.0.0 --port=5555 --url_prefix=api/admin/flower
