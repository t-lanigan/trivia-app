
test:
	dropdb trivia_test
	createdb trivia_test
	psql trivia_test < trivia.psql
	python test_flaskr.py

run:
	npm start