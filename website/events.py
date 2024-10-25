from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from .models import Events, Bookings, User
from .forms import CreateEventForm, BookEvent
from . import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user

event_bp = Blueprint('events', __name__, url_prefix='/events')

#Ordinal function
def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

@event_bp.route('/<id>')
def show(id):
    bookingForm = BookEvent()
    event = db.session.scalar(db.select(Events).where(Events.id==id))
    creator = db.session.scalar(db.select(User).where(User.id == event.user_id))
    #Convert date to ordinal
    event.date = ordinal(event.date)
    
    if not event:
       abort(404)
    return render_template('events/event.html', event=event, form=bookingForm, creator=creator)

@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  create = CreateEventForm()
  if 'submit' in request.form:
    db_file_path = check_upload_file(create)
    
    title = create.title.data
    desc = create.desc.data
    image = db_file_path
    date = create.date.data
    month = create.month.data
    nightclub = create.nightclub.data
    event_type = create.event_type.data
    age_range = create.age_range.data
    user_id = current_user.id
    
    #Time and price
    time = create.hour.data + ':' + create.minute.data + create.ampm.data
    price = create.price.data

    new_event = Events(title=title, desc=desc, image=image, date=date, month=month, nightclub=nightclub, event_type=event_type, age_range=age_range, user_id=user_id, time=time, price=price)
    db.session.add(new_event)
    db.session.commit()
    
    flash('Successfully created new event', 'success')
    # Always end with redirect when form is valid
    return redirect(url_for('events.create'))
  return render_template('events/create.html', form=create)

def check_upload_file(form):
  # get file data from form  
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/img/', secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/' + secure_filename(filename)
  # save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

#Booking event
@event_bp.route('/<id>/book', methods=['GET', 'POST'])
@login_required
def book(id):
  bookingForm = BookEvent()
  if bookingForm.validate_on_submit():
    #price feature needs to be added
    booked_date = datetime.now()
    price = db.session.scalar(db.select(Events.price).where(Events.id==id))
    quantity = bookingForm.quantity.data
    user_id = current_user.id
    booking = Bookings(price=price, quantity=quantity, booked_date=booked_date, event_id=id, user_id=user_id)

    db.session.add(booking)
    db.session.commit()
  return redirect(url_for('events.bookings', id=id))


@event_bp.route('/bookings')
@login_required
def bookings():
    booked = db.session.query(Bookings, Events).filter(Events.id == Bookings.event_id, Bookings.user_id == current_user.id).all()
    return render_template('bookings.html', bookings=booked)