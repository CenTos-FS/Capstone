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
    actors = Actors.query.all()
    
    if len(actors) == 0:
      abort(404)

    current_actors = paginate_data(request, actors)
    return jsonify({
      "success": True,
      "actors": current_actors,
      "total_actors": len(actors)
    })

    




  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)