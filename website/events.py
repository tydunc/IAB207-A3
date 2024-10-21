from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from .forms import CreateEventForm
from . import db 

event_bp = Blueprint('event', __name__, url_prefix='/events')

@event_bp.route('/<int:id>')  #original line: @event_bp.route('/<id>')
def show(id):
    event = get_event()
    return render_template('events/event.html', event=event)

@event_bp.route('/create', methods=['GET', 'POST'])  #original line: @event_bp.route('/create')
def create():
  form = CreateEventForm() #original line: create = CreateEventForm()
  if (form.validate_on_submit()==True):
     new_event = Event (
        title = form.title.data,
        desc = form.desc.data,
        imaage = form.image.data.filename,
        date = form.date.data,
        month = form.month.data,
        nightclub = form.nightclub.data,
        event_type = form.event_type.data,
        age_range = form.age_range.data
     )

     db.session.add(new_event)
     db.session.commit()

     return redirect(url_for('event.show', id=new_event.id))
  
  return render_template('events/create.html', form=form) #original line: return render_template('events/create.html', form=create)
  #need to change this once a new page is created that summarises the new event created by the user

def get_event(): #is this one still needed then?
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

