# Example usage: make makemigrations message="create_table"
makemigrations:
	docker exec eqsitecms-$(eqname)-app sh -c "cd src && uv run alembic revision --autogenerate -m '$(message)'"

migrate:
	docker exec nexora-app sh -c "cd src && uv run alembic upgrade head"

shell:
	docker exec -it nexora-app sh

# Opens postgresql command line interface
psql:
	docker exec -it nexora-db psql -U nexoradev

dumpall:
	docker exec -t nexora-db pg_dumpall -c -U nexoradev > dump_`date +%Y-%m-%d"_"%H_%M_%S`.sql

lint:
	uv run mypy src

format:
	uv run isort src && uv run black src

# Dangerous
drop_db:
	docker exec -t nexora-db psql -U nexoradev -d postgres -c "DROP DATABASE IF EXISTS nexoradev;"

seed_dump:
	cat seed_mocks.sql | docker exec -i nexora-db psql -U nexoradev

test:
	PYTHONPATH=src uv run pytest -s -vv tests/

test_only_unit:
	PYTHONPATH=src uv run pytest -s -vv tests/unit/

test_only_integration:
	PYTHONPATH=src uv run pytest -s -vv tests/integration/

populate_demo_data:
	DB_HOST=localhost PYTHONPATH=src uv run python maintain/generate_dev_data.py

collect_by_formulas:
	DB_HOST=localhost PYTHONPATH=src uv run python maintain/run_statistic_formulas.py

