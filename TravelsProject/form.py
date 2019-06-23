from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from TravelsProject.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from flask_datepicker import datepicker
from wtforms.fields.html5 import DateField,TimeField



class RegistrationForm(FlaskForm):
	username=StringField('Username', validators=[DataRequired(),Length(min=2,max=50)])
	email=StringField('Email',validators=[DataRequired(),Email()])
	password=PasswordField('Password',validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
	submit=SubmitField('SignUp')
	
	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username is already taken.Try another one')
			
	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is already taken.Try another one')
	
class LoginForm(FlaskForm):
	email=StringField('Email',validators=[DataRequired(),Email()])
	password= PasswordField('Password',validators=[DataRequired()])
	remember= BooleanField('Remember me')
	submit= SubmitField('Login')
	
class UpdateAccountForm(FlaskForm):
	username=StringField('Username', validators=[DataRequired(),Length(min=2,max=50)])
	email=StringField('Email',validators=[DataRequired(),Email()])
	picture= FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
	submit=SubmitField('Update')
	
	def validate_username(self,username):
		if username.data!=current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username is already taken.Try another one')
			
	def validate_email(self,email):
		if email.data!=current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email is already taken.Try another one')

class BusInfoForm(FlaskForm):
		fromstation=StringField('From',validators=[DataRequired()])
		tostation=StringField('To',validators=[DataRequired()])
		date=DateField('Date of Journey',format='%d-%m-%y',validators=[DataRequired()])
		submit=SubmitField('Submit')
		
		def validate_station(self,fromstation,tostation):

			if form.fromstation.data==form.tostation.date:
				raise ValidationError('Fromstation should not be equal to Tostation')
		
class AvailableBusesForm(FlaskForm):
	regno=StringField('Regno')
	startpoint=StringField('Startpoint')
	endpoint=StringField('Endpoint')
	model=StringField('Model')
	fare=StringField('Fare')
	starttime=TimeField('Starttime')
	droptime=TimeField('Droptime')
	seatsleft=StringField('Seatsleft')
	submit=SubmitField('Book now')
	
class BookingConfirmationForm(FlaskForm):
	regno=StringField('Regno')
	startpoint=StringField('Startpoint')
	endpoint=StringField('Endpoint')
	model=StringField('Model')
	fare=StringField('Fare')
	starttime=TimeField('Starttime')
	droptime=TimeField('Droptime')
	seatsleft=StringField('Seatsleft')
	noofpassengers=StringField('Number of Passengers')
	submit=SubmitField('Book now')
	
	
	
	
	
		
		
