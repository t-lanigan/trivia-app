import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_status(self):
        """Test GET /status/am-i-up"""
        response = self.client().get("/status/am-i-up")
        data = json.loads(response.data.decode())
        self.assertEqual(data["success"], True)
        self.assertEqual(response.status_code, 200)

    def test_get_categories(self):
        """Test GET /categories."""
        response = self.client().get("/categories")
        data = json.loads(response.data.decode())
        self.assertEqual(data["success"], True)
        self.assertEqual(response.status_code, 200)

    def test_get_questions(self):
        """Test GET /questions"""
        response = self.client().get("/questions")
        data = json.loads(response.data.decode())
        categories = ['Science', 'Art', 'Geography',
                      'History', 'Entertainment', 'Sports']
        self.assertEqual(data['categories'], categories)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data["success"], True)
        self.assertEqual(response.status_code, 200)

    def test_get_questions_pagination(self):
        """Test GET /questions?page=2 pagination"""
        response = self.client().get("/questions?page=2")
        data = json.loads(response.data.decode())
        self.assertEqual(data["success"], True)
        self.assertEqual(response.status_code, 200)

    def test_delete_question(self):
        """Test DELETE /questions?page=2 pagination"""
        deletion = self.client().delete("/questions/2")
        self.assertEqual(deletion.status_code, 200)
        response = self.client().get('/questions')
        data = json.loads(response.data.decode())
        self.assertGreater(data['total_questions'], 10)
        self.assertEqual(data["success"], True)
        self.assertEqual(response.status_code, 200)

    def test_create_question(self):
        """Test POSTing a new question."""
        body = {
            "question": "How many?",
            "answer": "5",
            "category": 2,
            "difficulty": 5
        }
        response = self.client().post("/questions",
                                      content_type="application/json",
                                      data=json.dumps(body))
        data = json.loads(response.data.decode())
        self.assertEqual(data["success"], True)
        self.assertEqual(response.status_code, 201)

    def test_search_question(self):
        """Test searching a question."""
        body = {"searchTerm": "royal"}

        response = self.client().post("/questions/search",
                                      content_type="application/json",
                                      data=json.dumps(body))
        data = json.loads(response.data.decode())
        self.assertEqual(data['questions'][0]['answer'],
                         'The Palace of Versailles')
        self.assertEqual(data["success"], True)
        self.assertEqual(response.status_code, 200)

    def test_get_questions_by_category(self):
        """Test get question by category."""
        response = self.client().get('/categories/0/questions')
        data = json.loads(response.data.decode())
        self.assertEqual(data['questions'][0]['category'],
                         'Science')
        self.assertLess(len(data['questions']), 5)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_resource_not_found(self):
        """Test resource not found"""
        res = self.client().get("/fake-endpoint")
        self.assertEqual(res.status_code, 404)

    def test_internal_service_error(self):
        """Test internal_service_error, should be rare"""
        response = self.client().get("/questions?page=3")
        data = json.loads(response.data.decode())
        self.assertEqual(data["success"], False)
        self.assertEqual(response.status_code, 500)

    def unprocessible_entity_error(self):
        """Test unprocessible_entity_error"""
        body = {
            "question": "How many?",
            "answer": "5",
            "category": "not existant",  # needs an id, not a str.
            "difficulty": 5
        }
        response = self.client().post("/questions",
                                      content_type="application/json",
                                      data=json.dumps(body))
        data = json.loads(response.data.decode())
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
