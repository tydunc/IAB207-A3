from flask import Blueprint, render_template, request, url_for, redirect
from .models import Events
from . import db, ordinal, inactive
from sqlalchemy import text

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    background = 'bg-1'
    events = db.session.scalars(db.select(Events)).all()
    for e in events:
        e.inactive = inactive(e.date,e.month)
        print(e.inactive)
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