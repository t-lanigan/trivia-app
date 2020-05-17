import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    app.config['QUESTIONS_PER_PAGE'] = 10
    db = setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        """Set response headers

        Arguments:
            response {[type]} -- the response before it goes out.

        Returns:
            response -- with headers added for access control.
        """
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def categories():
        """Handles GET Request for categories

        Returns:
            response, code -- the list of all categories.
        """

        try:
            response = jsonify({
                "success": True,
                "categories": [category.type for category in Category.query.all()]
            })

            return response, 200
        except Exception as e:
            app.logger.error(e)
            abort(500)

    @app.route('/status/am-i-up', methods=['GET'])
    def am_i_up():
        """Check to see if the app is running

        Returns:
            response, code -- the response and code
        """

        response = jsonify({
            "success": True,
        })

        return response, 200

    @app.route('/questions', methods=['GET'])
    def questions():
        """Handle GET requests for questions, including pagination (set page variable above in configs.)

        Returns:
            response -- the list of all questions including pagination.
        """

        try:
            page = request.args.get('page', 1, type=int)

            # SQLAlchemy has a function to paginate. Join the questions and categories table.
            questions = Question.query.join(
                Category, Category.id == Question.category).add_columns(
                Category.type).paginate(page, app.config['QUESTIONS_PER_PAGE'], False)

            formatted_questions = format_questions(questions.items)

            response = jsonify({
                "success": True,
                "questions": formatted_questions,
                "total_questions": len(Question.query.all()),
                'current_category': None,
                "categories": [category.type for category in Category.query.all()]
            })

            return response, 200
        except Exception as e:
            app.logger.error(e)
            abort(500)

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """ Deletes a question

        Arguments:
            question_id int -- the id of the quetsion

        Returns:
            response -- the succesfull deletion.
        """

        question = Question.query.filter_by(id=question_id).one_or_none()
        try:
            question.delete()

            response = jsonify({
                "success": True,
            })

            return response, 200

        except Exception as e:
            app.logger.error(e)
            abort(404)

    @app.route("/questions", methods=["POST"])
    def create_question():
        """Creates a questions to be submitted to the database

        Returns:
            response -- the list of all questions.
        """

        try:
            body = request.get_json()
            question = Question(
                question=body.get("question"),
                answer=body.get("answer"),
                category=int(body.get("category")),
                difficulty=int(body.get("difficulty"))
            )
            question.insert()

            response = jsonify({
                "success": True,
                "question": question.format(),
            })
            return response, 201
        except Exception as e:
            app.logger.error(e)
            abort(500)

    @app.route("/questions/search", methods=["POST"])
    def search_question():
        """Searches questions using a POST request.

        Returns:
            response -- questions filtered by a search term.
        """

        try:
            body = request.get_json()
            wild_search_term = '%' + body['searchTerm'] + '%'

            like_questions = Question.query.filter(
                Question.question.ilike(wild_search_term)).join(
                Category, Category.id == Question.category).add_columns(
                Category.type)

            formatted_questions = format_questions(like_questions)

            response = jsonify({
                "success": True,
                "questions": formatted_questions,
                "current_category": None,
            })
            return response, 200
        except Exception as e:
            app.logger.error(e)
            abort(500)

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        """Gets the list of questions filtered by category.

        Arguments:
            category_id int -- the category id

        Returns:
            response -- the questions filtered by category.
        """

        # Category comes indexed by 0.
        category_id = category_id + 1
        try:
            questions = Question.query.filter_by(category=category_id)\
                .join(Category, Category.id == Question.category)\
                .add_columns(Category.type)

            formatted_questions = format_questions(questions)
            response = jsonify({
                "success": True,
                "questions": formatted_questions,
                "current_category": None,
            })
            return response, 200
        except Exception as e:
            app.logger.error(e)
            abort(500)

    @app.route("/quizzes", methods=["POST"])
    def get_quiz_question():
        """a POST endpoint to get questions to play the quiz.

        This endpoint takescategory and previous question parameters 
        and return a random questions within the given category, 
        if provided, and that is not one of the previous questions.

        Returns:
            response -- a random question
        """

        try:
            body = request.get_json()
            print(body)
            previous_questions = body.get("previous_questions")

            # categories is indexed at 0, this adds one to match the db.
            category_id = str(int(body.get("quiz_category")["id"]) + 1)

            # if type is 'click' or ALL, then return all the questions.
            if body.get("quiz_category")["type"] == 'click':
                questions = Question\
                    .query\
                    .filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question\
                    .query\
                    .filter_by(category=category_id)\
                    .filter(Question.id.notin_(previous_questions)).all()

            # Get a random question if there are any left.
            question = random.choice(questions).format() if questions else None

            response = jsonify({
                "success": True,
                "question": question,
            })
            return response, 200

        except Exception as e:
            app.logger.error(e)
            abort(500)

    def format_questions(questions):
        """The front end expect questions formatted in a specific way

        Arguments:
            questions_category  -- questions and corresponding category
        """

        formatted_questions = []
        for question, category in questions:
            question = question.format()
            question["category"] = category
            formatted_questions.append(question)

        return formatted_questions

    @app.errorhandler(404)
    def resource_not_found_error(error):
        response = jsonify({
            "success": False,
            "error": 404,
            "message": error.description
        })
        return response, 404

    @app.errorhandler(422)
    def unprocessible_entity_error(error):
        response = jsonify({
            "success": False,
            "error": 422,
            "message": error.description
        })
        return response, 422

    @app.errorhandler(500)
    def internal_server_error(error):
        response = jsonify({
            "success": False,
            "error": 500,
            "message": error.description
        })
        return response, 500

    return app
