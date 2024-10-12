from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_booking.db'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User model (table)
class User(db.Model):
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
