from flask import Blueprint, render_template, request, url_for, redirect
from .models import Events
from . import db
from sqlalchemy import text

main_bp = Blueprint('main', __name__)

#Ordinal function
def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

@main_bp.route('/')
def index():
    background = 'bg-1'
    events = db.session.scalars(db.select(Events)).all()
    for e in events:
        e.date = ordinal(e.date)
    return render_template('index.html', background=background, events=events)

@main_bp.route('/search')
def search():
    background = 'bg-1'
    queries = ['event_type', 'age_range', 'nightclub']
    search = ''
    for query in queries:
        if request.args[query] != '*':
            i = request.args[query]
            search += f"Events.{query} == '{i}' AND "
    if search != '':
        events = db.session.scalars(db.select(Events).where(text(search[:-4]))).all()
        for e in events:
            e.date = ordinal(e.date)
        return render_template('index.html', background=background, events=events)
    else:
        return redirect(url_for('main.index'))