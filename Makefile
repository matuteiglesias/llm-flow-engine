.PHONY: run dev test lint format docker-build docker-run

run:
	python3 -m pipeline_core.flows.run_flow --flow pipeline_core/flows/hello.yaml

dev:
	./scripts/dev_start.sh

test:
	pytest -v

lint:
	flake8 .

format:
	black . && isort .

docker-build:
	docker build -t ai-workflow-mvp .

docker-run:
	docker run -p 8000:8000 --env-file .env ai-workflow-mvp
