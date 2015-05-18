__author__ = 'workhorse'
from app import db
from models import BlogPost

#create the db and the tables
db.create_all()

#insert
db.session.add(BlogPost("Good", "I\'m good"))
db.session.add(BlogPost("Smell", "I\'m smelly"))
db.session.commit()