buildimg:
	docker build -t django_oauth2_backend:latest .

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

restart:
	docker-compose restart

clean:
	docker container prune && docker volume prune && docker image prune

# Container command
schema:
	poetry run src/manage.py spectacular --file schema.yml

dev:
	poetry run src/manage.py runserver 0.0.0.0:8000

prd:
	poetry run uwsgi --ini uwsgi.ini