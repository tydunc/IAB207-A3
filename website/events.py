from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event

event_bp = Blueprint('event', __name__, url_prefix='/events')

@event_bp.route('/<id>')
def show(id):
    event = get_event()
    return render_template('events/event.html', event=event)

@event_bp.route('/create')
def create():
  return render_template('events/create.html')

def get_event():
  # creating the description of Brazil
  e_desc = """Event description. Lorem ipsum dolor sit amet,
    consectetur adipiscing elit, sed do eiusmod tempor incididunt
    ut labore et dolore magna aliqua. Ut enim ad minim veniam,
    quis nostrud exercitation ullamco laboris nisi ut aliquip ex
    ea commodo consequat. Duis aute irure dolor in reprehenderit
    in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa
    qui officia deserunt mollit anim id est laborum."""
   # an image location
  image_loc = '/static/img/pexels-maumascaro-788824.jpg'
  event = Event('UQ HATEFEST', e_desc,image_loc, 'PROHIBITION NIGHTCLUB')
  return event