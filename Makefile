PKG=uploader

.PHONY: all clean version init flake8 pylint lint test coverage

init: clean
	pipenv --python 3.7
	pipenv install

dev: init
	pipenv install --dev

run:
	pipenv run python main.py

commit:
	pipenv run cz commit

flake8:
	pipenv run flake8

pylint:
	pipenv run pylint $(PKG)

lint: flake8 pylint

black:
	pipenv run black $(PKG) -l 120 --skip-string-normalization

clean:
	find . -type d -name '__pycache__' -delete
