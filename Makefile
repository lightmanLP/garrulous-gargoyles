lint-client:
	flake8 client
	pylint client

lint-server:
	flake8 server
	pylint server

lint: lint-client lint-server
isort:
	isort client
	isort server
black:
	black client
	black server
