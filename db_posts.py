__author__ = 'workhorse'
from project import db
from project.models import BlogPost



#insert
db.session.add(BlogPost("New local test", "I\'m good", user_id=3))
db.session.add(BlogPost("new local test2", "I\'m smelly",3))
db.session.add(BlogPost("New local test3", "set up local Postgresqldb_create.py",4 ))
db.session.commit()