from flask_wtf import FlaskForm
import datetime
from wtforms import BooleanField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	
	username = StringField('Enter username', validators=[
		Length(min= 4, max= 30, message='name must be between 4 and 30 characters'),
	]) 
	# why do I put brackets around the validator ?
	email = StringField('Enter your email address', validators = [
		InputRequired(),
		Email(message='Doesn\'t look like an Email')
	])
	password = PasswordField('Enter a Password',validators = [
		InputRequired(),
		EqualTo('confirm', message='Passwords must match.')
	])
	confirm =  PasswordField('Repeat the Password',validators = [InputRequired()])
	
class LoginForm(FlaskForm):
	
	username = StringField('Enter username', validators=[
	Length(min= 4, max= 30, message='name must be between 4 and 30 characters'),
	]) 
	
	password = PasswordField('Enter your Password',validators = [
		InputRequired(),
	])
	
	