from flask import Blueprint, render_template, request, redirect, url_for, abort
from .models import Events
from .forms import CreateEventForm
from . import db

event_bp = Blueprint('events', __name__, url_prefix='/events')

@event_bp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Events).where(Events.id==id))
    if not event:
       abort(404)
    return render_template('events/event.html', event=event)

@event_bp.route('/create')
def create():
  create = CreateEventForm()
  return render_template('events/create.html', form=create)