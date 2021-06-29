release: ./manage.py migrate
web: gunicorn --bind 0.0.0.0:$PORT opengeo.wsgi
worker: REMAP_SIGTERM=SIGQUIT celery --app opengeo.celery worker --loglevel INFO --without-heartbeat
flower: flower --broker=$CLOUDAMQP_URL
