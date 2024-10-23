from flask import Blueprint, render_template
from .models import Events
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    background = 'bg-1'
    events = db.session.scalars(db.select(Events)).all()
    return render_template('index.html', background=background, events=events)