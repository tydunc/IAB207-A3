from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from .models import Events
from .forms import CreateEventForm
from . import db
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user

event_bp = Blueprint('events', __name__, url_prefix='/events')

@event_bp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Events).where(Events.id==id))
    if not event:
       abort(404)
    return render_template('events/event.html', event=event)

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
    
    new_event = Events(title=title, desc=desc, image=image, date=date, month=month, nightclub=nightclub, event_type=event_type, age_range=age_range, user_id=user_id)
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