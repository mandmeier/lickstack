web: gunicorn lickstack.wsgi
web: python manage.py collectstatic --no-input; gunicorn lickstack.wsgi --log-file - --log-level debug
