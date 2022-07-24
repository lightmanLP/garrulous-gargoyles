lint-game:
	flake8 game
	pylint game

lint-server:
	flake8 server
	flake8 server

lint: lint-game lint-server
