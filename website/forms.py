from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, SelectField, RadioField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# creates the login information
class LoginForm(FlaskForm):
    email=StringField("Email Address", validators=[InputRequired('Enter valid email')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    first_name=StringField("First Name", validators=[InputRequired()])
    surname=StringField("Last Name", validators=[InputRequired()])
    email=StringField("Email Address", validators=[Email("Please enter a valid email")])
    contact_number=IntegerField("Phone", validators=[InputRequired(), Length(10)])
    street_address=StringField("Address")
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

#form for create event
class CreateEventForm(FlaskForm):
    title=StringField("Event title", validators=[InputRequired()])
    desc=TextAreaField("Description", validators=[InputRequired()])
    image=FileField("Event Image", validators=[
        FileRequired(message = 'Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')
    ])
    date=RadioField('Label', choices=[('1'),('2'),('3'),('4'),('5'),('6'),('7'),('8'),('9'),('10'),('11'),('12'),('13'),('14'),('15'),('16'),('17'),('18'),('19'),('20'),('21'),('22'),('23'),('24'),('25'),('26'),('27'),('28'),('29'),('30'),('31')])
    month=SelectField('Month', choices=[('jan', 'Jan'), ('feb', 'Feb'), ('mar', 'Mar'), ('apr', 'Apr'), ('may', 'May'), ('jun', 'Jun'), ('jul', 'Jul'), ('aug', 'Aug'), ('sep', 'Sep'), ('oct', 'Oct'), ('nov', 'Nov'), ('dec', 'Dec')])
    nightclub=SelectField("Nightclub", choices=[('proho', 'Prohibition'), ('met', 'The MET'), ('retro', 'Retros'), ('beat', 'The Beat Megaclub')])
    event_type=SelectField("Event Type", choices=[('theme', 'Themed Party'), ('rave', 'Rave'), ('dj', 'DJ Set')])
    age_range=SelectField("Age range", choices=[('all', 'All ages'), ('un18', 'Under 18s'), ('ov18', 'Over 18s')])