from . import db
from datetime import datetime
from flask_login import UserMixin

# Define the User model (table)
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Make sure to hash passwords in practice
    contact_number = db.Column(db.String(15), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'User {self.first_name} {self.surname}'

class Event:
    def __init__(self, name, description, image_url, nightclub):
        self.name = name
        self.description = description
        self.image = image_url
        self.nightclub = nightclub
        self.comments = list()

    def __repr__(self):
        return f'Name: {self.name}, Currency: {self.nightclub}'

class Comments(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    def __repr__(self):
        return f"<Comment {self.comment_text[:20]} by User {self.user_id}>"

class Bookings(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float(2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    booked_date = db.Column(db.DateTime, default=datetime.now())
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Booking: {self.quantity} tickets booked at {self.booked_date}"