from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from .models import Events, Bookings, User, Review
from .forms import CreateEventForm, BookEvent
from . import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user
from PIL import Image

event_bp = Blueprint('events', __name__, url_prefix='/events')

# Ordinal function
def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

@event_bp.route('/<id>')
def show(id):
    bookingForm = BookEvent()
    event = db.session.scalar(db.select(Events).where(Events.id == id))
    creator = db.session.scalar(db.select(User).where(User.id == event.user_id))
    # Convert date to ordinal
    event.date = ordinal(event.date)

    # Fetch reviews for this event
    reviews = Review.query.filter_by(event_id=id).order_by(Review.date_posted.desc()).all()
    
    if not event:
        abort(404)
    return render_template('events/event.html', event=event, form=bookingForm, creator=creator, reviews=reviews)

@event_bp.route('/<id>/add_review', methods=['POST'])
@login_required
def add_review(id):
    if request.method == 'POST':
        rating = request.form['rating']
        review_text = request.form['review']
        author = request.form.get('author', current_user.first_name + " " + current_user.surname)  # Set author to current user's name
        
        # Create new review object and associate it with the event and user
        new_review = Review(rating=rating, review_text=review_text, author=author, user_id=current_user.id, event_id=id)
        db.session.add(new_review)
        db.session.commit()
        
        return redirect(url_for('events.show', id=id))

@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  action = url_for('events.create')
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
  return render_template('events/create.html', form=create, action=action)


#Edit event
@event_bp.route('/<id>/edit', methods=['GET','POST'])
@login_required
def edit(id):
  action = url_for('events.edit', id=id)
  event = db.session.query(Events).filter(Events.id == id).all()[0]
  if event.user_id != current_user.id:
     flash('Error: Logged in user is not the creator for this event')
     return redirect(url_for('events.show', id=id))
  else:
    #set the time values
    setattr(event, 'hour', event.time[:-5])
    setattr(event, 'minute', event.time[-4:-2])
    setattr(event, 'ampm', event.time[-2:])

    #prefill the form
    edit = CreateEventForm(request.form, obj=event)
    image = event.image[12:]
    edit.populate_obj(event)
    #Submit the data
    if 'submit' in request.form:
       print('Method type: ', request.method)
       event.title = edit.title.data
       event.desc = edit.desc.data
       event.date = edit.date.data
       event.month = edit.month.data
       event.nightclub = edit.nightclub.data
       event.event_type = edit.event_type.data
       event.age_range = edit.age_range.data
       event.time = edit.hour.data + ':' + edit.minute.data + edit.ampm.data
       event.price = edit.price.data

       db.session.commit()
       flash('Successfully updated event details')
       return redirect(url_for('events.show', id=id))
  return render_template('events/create.html', form=edit, image=image, action=action)

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

# Booking event
@event_bp.route('/<id>/book', methods=['GET', 'POST'])
@login_required
def book(id):
    bookingForm = BookEvent()
    if bookingForm.validate_on_submit():
        # price feature needs to be added
        booked_date = datetime.now()
        price = db.session.scalar(db.select(Events.price).where(Events.id == id))
        quantity = bookingForm.quantity.data
        user_id = current_user.id
        booking = Bookings(price=price, quantity=quantity, booked_date=booked_date, event_id=id, user_id=user_id)

        db.session.add(booking)
        db.session.commit()
    return redirect(url_for('events.bookings', id=id))

@event_bp.route('/bookings')
@login_required
def bookings():
    user_events = db.session.query(Events).filter(Events.user_id == current_user.id)
    booked = db.session.query(Bookings, Events).filter(Events.id == Bookings.event_id, Bookings.user_id == current_user.id).all()
    return render_template('bookings.html', bookings=booked, user_events=user_events)