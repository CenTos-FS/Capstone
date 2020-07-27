import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db,Movies,Actors
from auth import AuthError, requires_auth

#Number of actors and movies visible in a page
DATA_PER_PAGE = 10

def paginate_data(request, selection):
  '''Returns 10 actors/movies per page '''
  pageNo = request.args.get('page', 1, type=int)
  start = (pageNo - 1) * DATA_PER_PAGE
  end = start + DATA_PER_PAGE
  formatted_data = [data.format() for data in selection]
  page_wise_data = formatted_data[start:end]
  return page_wise_data


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,PATCH,DELETE,OPTIONS')
    return response

  
  @app.route('/actors', methods=['GET'])
  def get_actors():
    '''Returns list of actors per page 10 with total 
       number of actors '''
    actors = Actors.query.all() 
    if len(actors) == 0:
        abort(404)

    current_actors = paginate_data(request, actors)
    if len(current_actors) == 0:
        abort(404)

    return jsonify({
        "success": True,
        "actors": current_actors,
        "total_actors": len(actors)
      })
      
    

  @app.route('/movies', methods=['GET'])
  def get_movies():
    '''Returns list of movies per page 10 with 
       total number of movies'''
    movies = Movies.query.all()
    if len(movies)==0:
        abort(404)

    current_movies = paginate_data(request, movies)
    if len(current_movies) == 0:
        abort(404)

    return jsonify({
        "success": True,
        "movies": current_movies,
        "total_movies": len(movies)
      })    
      
 

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actors(jwt):
    data = request.get_json()
    try:
       if ((data.get('name') is None) and
          (data.get('age') is None) and
          (data.get('gender') is None)):
            abort(400)
       actor = Actors(name = data.get('name'),
                       age = data.get('age'),
                       gender = data.get('gender'))
       actor.insert()
       current_actors = paginate_data(request, Actors.query.all())
       return jsonify({
          'success': True,
          'created': actor.id,
          'actors': current_actors,
          'total_actors': len(Actors.query.all())
        })             
      
    except:
       abort(422)
              
  
  @app.route('/movies', methods=['POST'])
  @requires_auth("post:movies")
  def add_movies(jwt):
    data = request.get_json()
    if data.get('title') is None:
        abort(400)

    movie = Movies(title = data.get('title'),
                        releaseDate = data.get('releaseDate'))
    movie.insert()
    current_movies = paginate_data(request, Movies.query.all())
    return jsonify({
          "success": True,
          "created": movie.id,
          "movies" : current_movies,
          "total_movies": len(Movies.query.all())
       })        
        

                

  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth("delete:actors")
  def delete_actor(jwt,id):
    actor = Actors.query.filter(Actors.id == id).one_or_none() 
    if actor is None:
        abort(404)
    else:
        actor.delete()

    current_actors = paginate_data(request, Actors.query.all())
    return jsonify({
          'success': True,
          'deleted': id,
          'actors': current_actors,
          'total_actors': len(Actors.query.all())
        })    
        
          
   
  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(jwt,id):
    movie = Movies.query.filter(Movies.id == id).one_or_none() 
    if movie is None:
        abort(404)
    else:
        movie.delete()

    current_movies = paginate_data(request, Movies.query.all())
    return jsonify({
          'success': True,
          'deleted': id,
          'movies': current_movies,
          'total_movies': len(Movies.query.all())
        })           

    

  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth("patch:actors")
  def edit_actors(jwt,piid):
    actor = Actors.query.filter(Actors.id == id).one_or_none()
    if actor is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400)

    name = data.get('name', actor.name)
    age = data.get('age', actor.age)
    gender = data.get('gender', actor.gender)
    actor.name = name
    actor.age = age
    actor.gender = gender
    actor.update()

    return jsonify({
          'success': True,
          'updated': actor.id,
          'actor': [actor.format()]
        })   
  
       

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def edit_movies(id):
    movie = Movies.query.filter(Movies.id == id).one_or_none()
  
    if movie is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400)

    movie.title = data.get('title', movie.title)
    movie.releaseDate = data.get('releaseDate', movie.releaseDate)

    movie.update()   

    return jsonify({
          'success': True,
          'updated': movie.id,
          'movie': [movie.format()]
        }) 
         
 

  @app.errorhandler(404)
  def non_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource not found'
    }),404    

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request'
    }),400

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Request cannot be processed'
    }),422   

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
      'success': False,
      'error': error.status_code,
      'message': error.error['description']
    })  

  return app  

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)