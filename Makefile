lint-game:
	flake8 game
	pylint game

lint-server:
	flake8 server
	pylint server

lint: lint-game lint-server
isort:
	isort game
	isort server
black:
	black game
	black server
