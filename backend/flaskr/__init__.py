import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    app.config['QUESTIONS_PER_PAGE'] = 10
    db = setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
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
            json -- {"success": Boolean, "categories": str}
        """
        return jsonify({
            "success": True,
            "categories": [category.type for category in Category.query.all()]
        })

    @app.route('/status/am-i-up', methods=['GET'])
    def am_i_up():
        """Check to see if the app is running

        Returns:
            JSON -- {"success": Boolean}
        """
        return jsonify({
            "success": True,
        })

    @app.route('/questions', methods=['GET'])
    def questions():
        """Handle GET requests for questions, including pagination (set page variable above in configs.)

        Returns:
            JSON -- {"success": Boolean,
                     "questions: formatted_questions,
                     "total_questions": int,
                     "current_category: str,
                     "categories": str}
        """
        page = request.args.get('page', 1, type=int)

        # SQLAlchemy has a function to paginate. Join the questions and categories table.
        questions = Question.query.join(
            Category, Category.id == Question.category).add_columns(
            Category.type).paginate(page, app.config['QUESTIONS_PER_PAGE'], False)

        # The front end expect questions formatted is the following way:
        formatted_questions = []
        for question, category in questions.items:
            question = question.format()
            question["category"] = category
            formatted_questions.append(question)

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(Question.query.all()),
            'current_category': None,
            "categories": [category.type for category in Category.query.all()]
        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """ Deletes a question

        Arguments:
            question_id int -- the id of the quetsion

        Returns:
            JSON -- the succesful response.
        """
        try:
            question = Question.query.filter_by(id=question_id).first()
            question.delete()
            return jsonify({
                "success": True,
            })

        except Exception as e:
            app.logger.error(e)
            return jsonify({"message": "Question doesn't exist."})

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(404)
    def resource_not_found_error(error):
        response = jsonify({
            "success": False,
            "error": 404,
            "message": error.description
        })
        return response, 404

    @app.errorhandler(500)
    def internal_server_error(error):
        response = jsonify({
            "success": False,
            "error": 500,
            "message": error.description
        })
        return response, 500

    @app.errorhandler(422)
    def unprocessible_entity_error(error):
        response = jsonify({
            "success": False,
            "error": 422,
            "message": error.description
        })
        return response, 422

    return app
