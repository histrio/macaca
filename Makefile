.PHONY: docs

init:
	pip install -r REQUIREMENTS

run:
	export PYTHONPATH=$PYTHONPATH:src
	cd src && python macaca/alfa.py test

test:
	py.test

coverage:
	py.test --verbose --cov-report term --cov=macaca test_macaca.py

ci: init
	py.test --junitxml=junit.xml

certs:
	curl http://ci.kennethreitz.org/job/ca-bundle/lastSuccessfulBuild/artifact/cacerts.pem -o requests/cacert.pem

publish:
	python setup.py sdist upload
	python setup.py bdist_wheel upload

build:
	python setup.py clean sdist

deploy:
	fab -H bars@mu.bars-open.ru host_type

docs-init:
	pip install -r docs/REQUIREMENTS

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

db-init:
	cd src && python -c "from macaca.database import Base,db; Base.metadata.create_all(db)" 
	@echo "Database created."


