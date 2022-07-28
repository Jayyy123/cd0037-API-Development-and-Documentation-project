import os
from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category,db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.new_category = Category(type='entertainment')
            self.new_question = Question(question='what project is this?',answer='a project to build an api',category='1',difficulty='1')
            # create all tables
            self.db.create_all()
            self.db.session.add_all([self.new_category,self.new_question])
            self.db.session.commit()
        
        
    def tearDown(self):
        """Executed after reach test"""
        # with self.app.app_context():
        #     self.old_question = Question.query.first()
        #     self.db.session.delete(self.old_question)
        #     self.db.session.commit()
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # GET 
    def test_get_categories(self):
        query = self.client().get('/categories')
        # print((json.loads(query.data)['success']))
        response = json.loads(query.data)
        categories = [i.format() for i in Category.query.all()]

        self.assertEqual(query.status_code,200)
        self.assertEqual(response['success'],True)
        self.assertEqual(response['categories'],categories)


    def test_get_questions(self):
        query = self.client().get('/questions?page=1')
        # print((json.loads(query.data)['success']))
        response = json.loads(query.data)
        questions = [i.format() for i in Question.query.all()][:10]
        # print(questions[0:10])
        print(response)

        self.assertEqual(query.status_code,200)
        self.assertEqual(response['success'],True)
        self.assertEqual(response['questions'],questions)
        self.assertEqual(response['total_questions'],len(questions))


    # POST
    def test_create_question(self):
        res = self.client().post('/questions/create',json={'question':'what file is this?','answer':'the test file','category': 1,'difficulty':1})
        response = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(response['status'],200)
        self.assertEqual(response['message'],"New Question has been inserted successfully")

    # SEARCH
    def test_search_question(self):
        res = self.client().post('/questions/search',json={'searchTerm':'project'})
        response = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(response['success'],True)
        self.assertEqual(response['questions'][0]['question'],'what project is this?')


    # DELETE
    def test_delete_question(self):
        id = Question.query.all()[0].format()['id']

        query = self.client().delete(f'/questions/{id}')
        response = json.loads(query.data)

        self.assertEqual(query.status_code,200)
        self.assertEqual(response['success'],True)


    # errors
    def test_404_questions_not_found_error(self):
        query = self.client().get('/questions?page=1000')
        response = json.loads(query.data)
        # print(response)

        self.assertEqual(query.status_code,404)
        self.assertEqual(response['success'],False)
        self.assertEqual(response['message']," resource was Not found!")

    def test_422_empty_search(self):
        res = self.client().post('/questions/search',json={'searchTerm':''})
        response = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(response['success'],False)
        self.assertEqual(response['message'],' resource was unprocessable!')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()