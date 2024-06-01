run:
	python3 manage.py runserver

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

restartdb:
	python3 manage.py makemigrations account
	python3 manage.py makemigrations base
	python3 manage.py makemigrations statement
	python3 manage.py makemigrations django_bot
	python3 manage.py migrate
	python3 manage.py createsuperuser

daemon:
	celery -A config multi start worker1 \
    --pidfile="$HOME/run/celery/%n.pid" \
    --logfile="$HOME/log/celery/%n%I.log"

celery:
	celery -A config worker -l info