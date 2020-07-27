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
        self.database_name = "capestone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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

    def test_add_actor_422(self):
        actor = {
            'name': 'Farhan',
            'gender': 'Male'
        }    
        response = self.client().post('/actors', json = actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request cannot be processed')    

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
    
    def test_add_movie(self):
        movie = {
            'title': 'Dil Bechara',
            'releaseDate': '2020-10-10'
        }      
        response = self.client().post('/movies', json = movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['movies'])

    def test_add_movie_400(self): 
        response = self.client().post('/movies', json = {})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')  
     

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

    def test_edit_actor(self):
        actor = Actors.query.order_by(Actors.id.desc()).first()
        id = actor.id
        edit_actor ={
            'name': 'Peter Parker',
            'age': 28
        }            
        response = self.client().patch(f'/actors/{id}', json = edit_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_edit_actor_404(self):
        id = 2222    
        edit_actor ={
            'age': 29
        }            
        response = self.client().patch(f'/actors/{id}', json = edit_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')   

    def test_edit_actor_400(self):
        actor = Actors.query.order_by(Actors.id.desc()).first()
        id = actor.id
        response = self.client().patch(f'/actors/{id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')   

    def test_edit_movie(self):
        movie = Movies.query.order_by(Movies.id.desc()).first()
        id = movie.id
        edit_movie ={
            'releaseDate': '2020-10-3'
        }            
        response = self.client().patch(f'/movies/{id}', json = edit_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_edit_movie_404(self):
        id = 2222    
        edit_movie ={
            'releaseDate': '2020-10-4'
        }              
        response = self.client().patch(f'/movies/{id}', json = edit_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')   

    def test_edit_actor_400(self):
        movie = Movies.query.order_by(Movies.id.desc()).first()
        id = movie.id
        response = self.client().patch(f'/movies/{id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')  

    def test_delete_actor(self):
        actor = Actors.query.order_by(Actors.id.desc()).first()
        id = actor.id 
        response = self.client().delete(f'/actors/{id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_actor_404(self):
        id = 1000
        response = self.client().delete(f'/actors/{id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie(self):
        movie = Movies.query.order_by(Movies.id.desc()).first()
        id = movie.id 
        response = self.client().delete(f'/movies/{id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    
    def test_delete_movie_404(self):
        id = 1000
        response = self.client().delete(f'/movies/{id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')   

   

if __name__ == "__main__":
    unittest.main()


