from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=4, max=25, message='Username must be between 4 and 25 characters.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.')
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=4, max=25, message='Username must be between 4 and 25 characters.')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Invalid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=6, message='Password must be at least 6 characters long.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password.'),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')


from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired

class MaintenanceForm(FlaskForm):
    bus_id = HiddenField('Bus ID', default='A')  # Set default bus ID here if needed
    tires = SelectField('Tires Status', choices=[('Good', 'Good'), ('Needs Attention', 'Needs Attention')], validators=[DataRequired()])
    brakes = SelectField('Brakes Status', choices=[('Good', 'Good'), ('Needs Attention', 'Needs Attention')], validators=[DataRequired()])
    oil = SelectField('Oil Level', choices=[('Full', 'Full'), ('Low', 'Low'), ('Needs Change', 'Needs Change')], validators=[DataRequired()])
    engine = SelectField('Engine Status', choices=[('Running Smoothly', 'Running Smoothly'), ('Minor Issues', 'Minor Issues'), ('Needs Repair', 'Needs Repair')], validators=[DataRequired()])
    lights = SelectField('Lights Status', choices=[('Working', 'Working'), ('Needs Attention', 'Needs Attention')], validators=[DataRequired()])
    engine_performance = SelectField('Engine Performance', choices=[('Good', 'Good'), ('Needs Attention', 'Needs Attention')], validators=[DataRequired()])
    transmission_fluid = SelectField('Transmission Fluid', choices=[('Full', 'Full'), ('Low', 'Low'), ('Needs Change', 'Needs Change')], validators=[DataRequired()])
    battery_charger = SelectField('Battery Charger Test', choices=[('Working', 'Working'), ('Needs Repair', 'Needs Repair')], validators=[DataRequired()])
    brake_pads = SelectField('Brake Pads Inspection', choices=[('Good', 'Good'), ('Worn', 'Worn'), ('Needs Replacement', 'Needs Replacement')], validators=[DataRequired()])
    comments = TextAreaField('Additional Comments', default='', validators=[DataRequired()])
    submit = SubmitField('Submit Update')


class QueryForm(FlaskForm):
    bus_id = StringField('Bus ID', validators=[DataRequired()])
    issue = TextAreaField('Issue', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DailyMaintenanceForm(FlaskForm):
    bus_id = StringField('Bus ID', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    notes = TextAreaField('Maintenance Notes', validators=[DataRequired()])
    submit = SubmitField('Submit')


class MonthlyMaintenanceForm(FlaskForm):
    bus_id = StringField('Bus ID', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    maintenance_type = StringField('Maintenance Type', validators=[DataRequired()])
    notes = TextAreaField('Maintenance Notes', validators=[DataRequired()])
    submit = SubmitField('Submit')



class DriverQueryForm(FlaskForm):
    bus_id = StringField('Bus ID')
    issue_details = StringField('Issue Details')
    submit = SubmitField('Submit')