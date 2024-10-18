from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    background = 'bg-1'
    return render_template('index.html', background=background)

@main_bp.route('/bookings')
def bookings():
    return render_template('bookings.html')