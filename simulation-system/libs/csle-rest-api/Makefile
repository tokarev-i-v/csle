.PHONY: clean

all: install_dev install unit_tests tests release

release: build push

install_dev:
    pip install -r requirements_dev.txt

tests:
	tox

unit_tests:
	pytest --cov=csle_rest_api

types:
	mypy .

lint:
	flake8 .

docs:
	cd docs; sphinx-apidoc -f -o source/ ../csle_rest_api/ && make html && cp -r build/html ../../../../docs/_docs/csle-rest-api

install:
	pip install -e .

build:
	python3 -m build

push:
	python3 -m twine upload dist/*

clean:
	rm -r dist