TEST_APP_NAME := trivia_test

test:
	@dropdb $(TEST_APP_NAME)
	@createdb $(TEST_APP_NAME)
	@psql $(TEST_APP_NAME) < trivia.psql
	python test_flaskr.py

run-backend:
	FLASK_APP=flaskr FLASK_ENV=development flask run

connect-to-db:
	psql $(TEST_APP_NAME)

reset-db:
	dropdb $(TEST_APP_NAME)
	createdb $(TEST_APP_NAME)
	psql $(TEST_APP_NAME) < trivia.psql