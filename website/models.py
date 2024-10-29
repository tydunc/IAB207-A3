from . import db
from datetime import datetime
from flask_login import UserMixin
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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

# Define the Events model (table)
class Events(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(100), nullable=False)  # Store the image file path
    date = db.Column(db.Integer, nullable=False)       # Store the selected date of the event
    month = db.Column(db.String(3), nullable=False)    # Store the selected month ('Jan', 'Feb')
    nightclub = db.Column(db.String(50), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    age_range = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Time and price
    time = db.Column(db.String(7), nullable=False)
    price = db.Column(db.Float(2), nullable=False)
    tickets = db.Column(db.Integer, nullable=False)

# Define the Bookings model (table)
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

# Adding the Review model (table)
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(100), nullable=False, default='Anonymous')
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Linking to the User model
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)  # Linking to the Events model

    def __repr__(self):
        return f"<Review {self.id}>"