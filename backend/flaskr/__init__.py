from ast import Not
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Acess-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Acess-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories')
    def categories():
        c = Category.query.all()

        if c:
            category = [i.format() for i in c]
            total = len(category)
            return jsonify({
            "categories":category,
            "success":True,
            "total_categories":total,
            "status_code":200
        })
        else:
            return not_found(404)


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def questions():
        q = Question.query.all()

        # print('----------------')
        # print(q)
        # print('----------------')

        if q:
            page = request.args.get('page',1,type=int)
            if page and len(q) > page:
                question = [i.format() for i in q]
                paginated_questions = paginate(question,page)
                total = len(paginated_questions)
                categories = Category.query.all()
                categ = [i.format() for i in categories]
                # print('----------------')
                # print(categories)
                # print('----------------')
                return jsonify({
                    "questions":paginated_questions,
                    "total_questions":total,
                    "currentCategory":'All',
                    "categories": categ,
                    "success":True,
                })
            else:
                return not_found(404)

        else:
            return not_found(404)





    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>',methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            return unprocessable(422,'question')
        else:
            question.delete()
            return jsonify({
                "success":True,
                "message": f'question with {question_id} has been successfully deleted from the database!'
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
    @app.route('/questions/create', methods=['POST'])
    def create_question():
        new_question = request.get_json()
        q = new_question['question']
        a = new_question['answer']
        c = new_question['category']
        d = new_question['difficulty']
        if new_question:
            question = Question(question=q,answer=a,category=c,difficulty=d)
            question.insert()
            return jsonify({
                "status":200,
                "message":"New Question has been inserted successfully"
            })
        else:
            return unprocessable(422,'your new question')

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_item = (request.get_json()['searchTerm'])
        # print(dict(request.get_json())['searchTerm'])
        print((request.get_json())['searchTerm'])
        print('---------------\n\n')
        s_r = Question.query.all()
        search_results = []
        if search_item == '':
            return unprocessable(422,'empty search')
        else:
            #   venues.append(Venue.query.filter(Venue.name.ilike(f'{item}%')).first())
            # s_r.append(Question.query.filter(Question.question.ilike('%{search_item}%')).all())
            # s_r.append(Question.query.filter(Question.question.ilike('{search_item}%')).all())
            # s_r.append(Question.query.filter(Question.question.ilike('%{search_item}')).all())
            # s_r.append(Question.query.filter(Question.question.ilike('{search_item}')).all())
            for i in s_r:
                formatted = i.format()
                if search_item in formatted['question']:
                    search_results.append(i.format())

            total = len(search_results)
            print('-=-=-=\n',s_r,'\n=-=-=')
            return jsonify({
                "success":True,
                "questions":search_results,
                "total_questions":total,
                "current_category":'All'
            })
            
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions')
    def get_questions(category_id):
        category_name = Category.query.get(category_id).format()['type']
        print('s ',category_id,category_name)
        q = Question.query.filter_by(category=category_name).all()
        print(category_name,q)

        if q:
            questions = [i.format() for i in q]
            total = len(questions)
            return jsonify({
                "questions":questions,
                "current_category":category_name,
                "total_questions":total,
                "success":True
            })
        else:
            return not_found(404)

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
    def random_question():
        r = request.get_json()
        previous_questions = r['previous_questions']
        selected_category = r['quiz_category']
        print('==============', previous_questions ,'\n========')
        if selected_category['type'] != 'click':
            print('hereee')
            category_type = selected_category['type']
            questions = Question.query.filter_by(category=category_type).all()
            print(questions,'ooo')
        else:
            print('rogress',selected_category)
            questions = Question.query.all()

        print('----',selected_category,'jjjj')
        l = [i.format()['id'] for i in questions]

        if questions:
            from collections import Counter
            res = [k for k, v in (Counter(l) - Counter(previous_questions)).items() for _ in range(v)]
            print(res)

            print('\n-----------\n')
            print(questions,l)
            print('\n-----------\n')
            end = len(l)
            print('the current auestions list is',questions,'=--=',l)
            if end == 1 or end < 1:
                random_int = 0
            else:
                random_int = random.sample(range(0, end), 1)[0]

            random_question = Question.query.get(l[random_int]).format()
            print(random_question)
            difficulty = random_question['difficulty']
            return jsonify({
                "category": selected_category,
                "question":random_question,
                "difficulty": difficulty
            })
        else:
            print('---------',questions,'-----',selected_category)
            return unprocessable(422,'your selected category field')



    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error code": error,
            "message": " resource was Not found!"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error,title='your'):
        return jsonify({
            "success": False, 
            "error code": 422,
            "message": " resource was unprocessable!"
        }), 422

    # handle pagination function
    def paginate(array,page):
        length = len(array)
        start = (page - 1) * 10
        end = start+10
        new_array = array[start:end]
        return new_array

    return app

