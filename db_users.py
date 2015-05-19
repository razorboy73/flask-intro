__author__ = 'workhorse'
from project import db
from project.models import User

#create the db and the tables


#insert
db.session.add(User("Josh","joshadamkerbel@gmail.com", "Swingline1"))
db.session.add(User("admin","ad@min.com", "admin"))

db.session.commit()