from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    #the validation of form is fine, HTTP request is POST
    if (register.validate_on_submit()==True):

        first_name = register.first_name.data
        surname = register.surname.data
        email = register.email.data
        contact_number = register.contact_number.data
        street_address = register.street_address.data
        pwd = register.password.data

        password = generate_password_hash(pwd)

        new_user = User(first_name=first_name, surname=surname, email=email, password=password, contact_number=contact_number, street_address=street_address)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.index'))
    else:
        return render_template('user.html', form=register, heading='Register')

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        email = login_form.email.data
        pwd = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.email==email))
        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user.password, pwd): # takes the hash and cleartext password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))