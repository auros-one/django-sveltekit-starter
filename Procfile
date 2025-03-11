web: gunicorn project.wsgi:application
worker: celery -A project worker --loglevel=info --autoscale=10,3
beat: celery -A project beat --loglevel=info
flower: celery -A project flower --address=0.0.0.0 --port=5555 --url_prefix=flower
