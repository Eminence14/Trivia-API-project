from math import remainder
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def pagination(request, trivia):
    page = request.args.get('page', 1, type=int)
    start = (page - 1)* QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    trivia = [trivium.format() for trivium in trivia]
    present_trivia = trivia[start:end]
    return present_trivia

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Allow-Control-Access-Headers', 'Content-Type, Authorization'
        )
        response.headers.add(
            'Allow-Control-Access-Methods', 'GET, POST, PATCH, OPTIONS, PUT'
        )
        response.headers.add('Allow-Control-Access-Origin', '*')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        # present_trivia = pagination(request, trivia)
        cat = [category.format() for category in categories]
        categ = {category.id:category.type for category in categories}
        return jsonify ({
            'success': True,
            "categories": categ,
            "total_category": len(cat)
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    """
    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        quest_categories = Category.query.order_by(Category.id).all()
        all_categories = {category.id:category.type for category in quest_categories}
        # formatted_quest = [question.format() for question in questions]
        page_quest = pagination(request, questions)
        return jsonify ({
            'success': True,
            'categories': all_categories,
            # 'current_category': Question.category,
            'questions': page_quest,
            'totalQuestions': len(questions)
        })


    """

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.order_by(Question.id).filter(Question.id == question_id).first()
        question.delete()
        remainder = Question.query.order_by(Question.id).all()
        format_quest = pagination(request, remainder)
        return jsonify({
            'success': True,
            'question': question_id,
            'remaining_questions': format_quest
        })
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def new_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        add_quest = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        add_quest.insert()

        present_quest = Question.query.order_by(Question.id).all()
        page_quest = pagination(request, present_quest)

        return jsonify({
            'success': True,
            'questions': page_quest
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        search = body.get('searchTerm')
        search_quest = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search))).all()
        related_quest = pagination(request, search_quest)

        if  len(related_quest) == 0:
            abort(404)

        else:
            return jsonify({
                'success': True,
                'related_questions': related_quest,
                'length_related_question': len(related_quest)
            })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions')
    def particular_cat(category_id):
        category_question = Question.query.order_by(Question.id).filter(Question.category == str(category_id)).all()
        cat_formatted = pagination(request, category_question)
        # cat_formatted = [question.format() for question in category_question]
        return jsonify({
            'success': True,
            'category_id': category_id,
            'category_question': cat_formatted
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        if quiz_category['id'] == 0:
            questions = Question.query.filter(Question.id not in previous_questions ).all()
            if len(previous_questions) > len(questions):
                questions = None
        else:
            questions = Question.query.filter(Question.id not in previous_questions).filter(Question.category == quiz_category['id']).all()

        format_question = [question.format() for question in questions]
        random_quiz = random.randint(0, len(format_question) - 1)
        next_question = format_question[random_quiz]
        return jsonify({
            'success': True,
            'question': random_quiz,
            'next_question': next_question
        })
    """
        
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad Request"
        }), 400
    @app.errorhandler(404)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not Found"
        }), 404
    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Method Not Allowed"
        }), 405
    @app.errorhandler(422)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable"
        }), 422
    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "Internal Server Error"
        }), 500

    return app

