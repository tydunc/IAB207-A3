from . import db
from datetime import datetime
from flask_login import UserMixin

#class User(db.Model, UserMixin):

class Event:
    def __init__(self, name, description, image_url, nightclub):
        self.name = name
        self.description = description
        self.image = image_url
        self.nightclub = nightclub
        self.comments = list()

    def __repr__(self):
        return f'Name: {self.name}, Currency: {self.nightclub}'

#class Comment(db.Model):

#class Order(db.Model):