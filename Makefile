test:
	docker-compose -f local.yml run --rm app python -m pytest -v

build:
	docker-compose -f local.yml build
