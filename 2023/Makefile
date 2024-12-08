.PHONY: all pretty lint

all: lint
lint:
	black --diff .
	ruff .

pretty:
	black .
	ruff --fix .
