from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

# Create Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_booking.db'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

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
        return f'<User {self.first_name} {self.surname}>'

#define the bookings table    
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
    
#I just created this events class so the foreign keys with booking would work
class Events(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    imaage = db.Column(db.String(100), nullable=False) #Store the image file path
    date = db.Column(db.Integer, nullable=False)       #Store the selected date of the event
    month = db.Column(db.String(3), nullable=False)    #Store the selected month ('Jan','Feb')
    nightclub = db.Column(db.String(50), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    age_range = db.Column(db.String(50), nullable=False)

#comments table
class Comments(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    def __repr__(self):
        return f"<Comment {self.comment_text[:20]} by User {self.user_id}>"


# Create the database and tables immediately when app starts
with app.app_context():
    db.create_all()

# Define a simple route
@app.route('/')
def index():
    return "User table created for event booking!"

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
