import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db,Movies,Actors

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
    return jsonify({
      "success": True,
      "movies": current_movies,
      "total_movies": len(movies)
    })     

  @app.route('/actors', methods=['POST'])
  def add_actors():
    data = request.get_json()
    if ((data.get('name') is None) and
       (data.get('age') is None) and
       (data.get('gender') is None)):
         abort(422)
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
  
  @app.route('/movies', methods=['POST'])
  def add_movies():
    data = request.get_json()
    if ((data is None) and 
         (data.get('title') is None)):
         abort(422)

    movie = Movies(title = data.get('title'),
                    releaseDate = data.get('releaseDate'))
    movie.insert()
    current_movies = paginate_data(request, Movies.query.all())
    return jsonify({
      "success": True,
      "created": movie.id,
      "movies" : current_movies,
      "total_movies": len(Movies.query.all)
    })                     

  @app.route('/actors/<int:id>', methods=['DELETE'])
  def delete_actor(id):
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
  def delete_movies(id):
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
  return app

  @app.route('/actors/<int:id>', methods=['PATCH'])
  def edit_actors(id):
    actor = Actors.query.filter(Actors.id == id).one_or_none()
    if actor is None:
      abort(404)

    data = request.get_json()
    if data is None:
      abort(422)

    actor.name = data.get('name', actor.name)
    actor.age = data.get('age', actor.age)
    actor.gender = data.get('gender', actor.gender)

    db.session.update(actor)
    db.session.commit()

    return jsonify({
      'success': True,
      'updated': actor.id,
      'actor': [actor.format()]
    })    

  @app.route('/movies/<int:id>', methods=['PATCH'])
  def edit_movies(id):
    movie = Movies.query.filter(Movies.id == id).one_or_none()
    if movie is None:
      abort(404)

    data = request.get_json()
    if data is None:
      abort(422)

    movie.title = data.get('title', movie.title)
    movie.releaseDate = data.get('releaseDate', movie.releaseDate)

    db.session.update(movie)
    db.session.commit()         

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)