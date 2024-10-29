from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime

# Initialize the database instance
db = SQLAlchemy()

#Some functions we'll use later
def inactive(date, month):
   months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
   curr = datetime.today().strftime('%Y-%m-%d')
   eventDate = datetime.strptime(f'{date}/{months.index(month)+1}/{curr[:4]}', "%d/%m/%Y")
   if datetime.now().date() > eventDate.date():
      return True
   else:
      return False

def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

# Create a function that creates a web application
def create_app():
  
    app = Flask(__name__)  # This is the name of the module/package that is calling this app
    
    # Set the secret key and debug mode (remember to turn off debug mode in production)
    app.debug = True
    app.secret_key = 'somesecretkey'
    
    # Set the app configuration for the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_booking.db'  # Use one database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress SQLAlchemy warning
     
    # Initialize db with Flask app
    db.init_app(app)
    
    # Initialize Bootstrap5 for styling
    Bootstrap5(app)
    
    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # Define a user loader function that takes a user ID and returns a User object
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id == user_id))
    
    # Register blueprints for the views and events modules
    from . import views
    app.register_blueprint(views.main_bp)
    
    from . import events
    app.register_blueprint(events.event_bp)
    
    # Register blueprint for authentication (uncomment if needed)
    from . import auth
    app.register_blueprint(auth.auth_bp)
    
    # Return the app instance
    return app
