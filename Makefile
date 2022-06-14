COMPOSE_DEV := -f ./etc/docker/compose/docker-compose.yml \
	-f ./etc/docker/compose/docker-compose.override.yml

# Run Targets

start: stop
	docker-compose $(COMPOSE_DEV) rm -f \
	&& docker-compose $(COMPOSE_DEV) up -d postgres redis \
	celery_scheduler celery_worker proxy app

stop:
	docker-compose $(COMPOSE_DEV) stop && docker-compose $(COMPOSE_DEV) rm -f

restart: stop start

# Development Targets

start-infra:
	docker-compose $(COMPOSE_DEV) \
	up -d redis
