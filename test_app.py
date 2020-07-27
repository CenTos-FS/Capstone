import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies
import config

class CapstoneTestCases(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = config.SQLALCHEMY_DATABASE_URI
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actor(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actor_404(self):
        response = self.client().get('/actors?page=1000')   
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found') 

    def test_get_movies(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_404(self):
        response = self.client().get('/movies?page=1000')   
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')  

    def test_add_actor(self):
        actor = {
            'name': 'Kizzi',
            'age': 29,
            'gender': 'Female'
        }      
        response = self.client().post('/actors', json = actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['actors'])

    def test_add_actor_400(self):
        actor = {
            'name': 'Farhan',
            'gender': 'Male'
        }    
        response = self.client().post('/actors', json = actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_add_movie(self):
        movie = {
            'title': 'Dil Bechara',
            'releaseDate': date.today()
        }      
        response = self.client().post('/movies', json = movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['movies'])

    def test_add_movie_400(self):
        movie = {
            'releaseDate': date.today()
        }    
        response = self.client().post('/movies', json = movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')  

    def test_delete_actor(self):
        actor = Actors.query.order_by(Actors.id.desc()).first()
        id = actor.id 
        response = self.client().delete('/actors/'+id)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_actor_404(self):
        id = 1000
        response = self.client().delete('/actors/'+id)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['deleted']) 
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie(self):
        movie = Movies.query.order_by(Actors.id.desc()).first()
        id = movie.id 
        response = self.client().delete('/movies/'+id)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_movie_404(self):
        id = 1000
        response = self.client().delete('/movies/'+id)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['deleted']) 
        self.assertEqual(data['message'], 'Resource not found')           


