# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

or use `make run-backend`

## API Description

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

`GET '/categories'`
- Fetches the categories.
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an array of categories types.

```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "success": true
}
```

`GET '/status/am-i-up'`
- Fetches a response if the backend server is up.
- Request Arguments: None
- Returns object saying if request was successful.

```
{
  "success": true
}
```


`GET '/questions?page=<int:page>'`
- Fetches an object with the questions in the database and some relavent information
- Request Arguments: page (int)
- Includes pagination
- Returns object with the categories, questions, and total amount of questions.

```
{
  "categories": [
    "Science", 
    ...
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": "History", 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 18
}
```

`DELETE '/questions/<int:question_id>'`
- Deletes a question in the database.
- Request Arguments: question_id (int)
- Returns object with the success message.

```
{
  "success": true
}
```

`POST '/questions'`
- Adds a new question to the database.
- Request Arguments: 

```
{
    "question": "What is the best color?",
    "answer": "blue",
    "category": 4,
    "difficulty": 2
}
```
- Returns the question added with the success message.

```
{
    "success": True,
    "question": {
            "question": "What is the best color?",
            "answer": "blue",
            "category": 4,
            "difficulty": 2
    }
}
```

`POST '/questions/search'`
- Adds searched through the questions in the database.
- Request Arguments: 

```

{
    "searchTerm": "Cassius"
}
```
- Returns the question that have the provide string.

```
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": "History", 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
  ], 
  "success": true
}
```

`GET '/categories/<int:category_id>/questions'`
- Returns the questions by category
- Request Arguments: the category id (int)
- Returns:
```
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": "History", 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    ...
  ], 
  "success": true
}
```


`POST '/quizzes'`
- Returns a random question given the questions already asked
- Request:
  ```

    {
        "quiz_category": {"id": 1},
        "previous_questions": [1, 2, ...]
    }
  ```
- Returns:

```
{
    {
        "answer": "Blood",
        "category": "Science",
        "category_id": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    }
}
```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

or `make test`