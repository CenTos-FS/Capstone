from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

database_path = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy()

def setup_db(app, database_path = database_path):
    '''Binds flask application and SQLAlchemy service '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    db.app = app
    db.init_app(app)
    db.create_all()

#Movies Model
class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    releaseDate = db.Column(db.DateTime)

    def __init__(self,title,releaseDate):
        self.title = title
        self.releaseDate = releaseDate

    def insert(self):
        db.session.add(self)
        db.session.commit() 

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()      

    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'releaseDate' : self.releaseDate
        }           

#Actors Model
class Actors(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()    

    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender 
        }        





