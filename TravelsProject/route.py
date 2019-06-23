import os
import secrets
from PIL import Image
from flask import render_template,url_for,redirect,flash, request
from TravelsProject.models import User, Bus
from TravelsProject.form import RegistrationForm, LoginForm, UpdateAccountForm, BusInfoForm, AvailableBusesForm, BookingConfirmationForm
from TravelsProject import app,db,bcrypt
from flask_login import login_user
from flask_login import current_user, logout_user, login_required
from sqlalchemy import and_



@app.route("/")
@app.route("/home",methods=['GET','POST'])
def home():
	form=BusInfoForm()
	fromstation=['Guntur','vijaywada','Rajahmundry','Aadanki','Vizag','Hyderabad','banglore']
	tostation=['Guntur','Vijaywada','Rajahmundry','Aadanki','Vizag','Hyderabad','banglore']
	if form.is_submitted():
		#form1=AvailableBusesForm()
		startpoint=request.form['fromstation']
		endpoint=request.form['tostation']
		#buses=Bus.query.filter(and_(Bus.startpoint=='vijaywada',Bus.endpoint=='banglore')).all()
		return redirect(url_for('availablebuses',startpoint=startpoint,droppoint=endpoint))
		#buses=Bus.query.filter(and_(Bus.startpoint==startpoint,Bus.endpoint==endpoint)).all()
		#return render_template('availablebuses.html',title='availablebuses',buses=buses,form1=form1)
		#flash(f'form submitted successfully')
	return render_template('home.html',form=form,fromstation=fromstation,tostation=tostation)
	
@app.route("/about")
def about():
	return render_template('about.html')
	
@app.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user,remember=form.remember.data)
			next_page=request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash(f'Login unsuccessful','danger')
	return render_template('login.html',form=form)
	
@app.route("/register",methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=RegistrationForm()
	if form.validate_on_submit():
		username = request.form['username']
		email = request.form['email']
		password=request.form['password']
		hashed_pw=bcrypt.generate_password_hash(password).decode('utf-8')
		data=User(username=username,email=email,password=hashed_pw)
		db.session.add(data)
		db.session.commit()
		flash(f'Account created successfully. Now you are able to login','success')
		return redirect(url_for('login'))
	return render_template('register.html',form=form)
	
@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))
	
@app.route("/account",methods=['GET','POST'])
@login_required
def account():
	form=UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file=save_picture(form.picture.data)
			current_user.image_file=picture_file
		current_user.username=form.username.data
		current_user.email=form.email.data
		db.session.commit()
		flash('Your account is updated','success')
		return redirect(url_for('account'))
	elif request.method== 'GET':
		form.username.data=current_user.username
		form.email.data=current_user.email
	image_file=url_for('static',filename='profilepics/'+ current_user.image_file)
	return render_template('account.html',title='Account',image_file=image_file,form=form)

def save_picture(form_picture):
		random_hex= secrets.token_hex(8)
		_,f_ext=os.path.split(form_picture.filename)
		picture_fn=random_hex+f_ext
		picture_path=os.path.join(app.root_path,'static/profilepics',picture_fn)
		output_size=(125,125)
		i=Image.open(form_picture)
		i.thumbnail(output_size)
		i.save(picture_path)
		return picture_fn
		
@app.route("/bookings",methods=['GET','POST'])
@login_required
def bookings():
		form=AvailableBusesForm()
		#bus=Bus.query.filter(and_(and_(Bus.startpoint=='vijaywada',Bus.endpoint=='banglore')),(and_(Bus.starttime='19:30:00',Bus.droptime='7:30:00'))).all()
		bus=Bus.query.filter(and_(Bus.startpoint=='vijaywada',Bus.endpoint=='banglore')).first()
		return render_template('bookingconfirmation.html')
		
@app.route("/availablebuses/<startpoint>/<droppoint>",methods=['GET','POST'])
def availablebuses(startpoint,droppoint):
		#startpoint=request.args.get('startpoint',None)
		#endpoint=request.args.get('droppoint',None)
		form=AvailableBusesForm()
		#form1=BusInfoForm()
		#startpoint=request.form1['fromstation']
		#start=form1.fromstation.data
		#endpoint=form1.tostation.data
		buses=Bus.query.filter(and_(Bus.startpoint==startpoint,Bus.endpoint==droppoint)).all()
		if form.is_submitted():
			regno=request.form.get('regno')
			#return render_template('bookingconfirmation.html',title='bookingconfirmation',form=form,regno=regno)
			return redirect(url_for('bookingconfirmation',regno=regno))
		return render_template('availablebuses.html',form=form,buses=buses)
		
@app.route("/bookingconfirmation/<regno>",methods=['GET','POST'])
def bookingconfirmation(regno):
	form=BookingConfirmationForm()
	bus=Bus.query.filter(Bus.regno==regno).first()
	if form.is_submitted():
		bus=Bus.query.filter(Bus.regno==regno).first()
		fare=int(request.form['noofpassengers'])*int(bus.fare)
		return render_template('bookingconfirmation.html',form=form,fare=fare,bus=bus)
	
	return render_template('bookingconfirmation.html',bus=bus,form=form)
	
	
	


	
