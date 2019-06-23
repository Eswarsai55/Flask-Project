from TravelsProject import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
	
class User(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(20),unique=True,nullable=False)
	email=db.Column(db.String(120),unique=True,nullable=False)
	image_file=db.Column(db.String(120),nullable=False,default='default.jpg')
	password=db.Column(db.String(60),nullable=False)
	bookings=db.relationship('Bookings',backref='userinfo', lazy=True)
	
	def __repr__(self):
	 return f"User('{self.username}','{self.email}')"
	 
	 
class Bus(db.Model):
	regno=db.Column(db.String(20),primary_key=True,nullable=False,autoincrement=False)
	modelname=db.Column(db.String(20),nullable=False)
	modeltype=db.Column(db.String(30),nullable=False,default='Seater')
	image_file=db.Column(db.String(120),nullable=False,default='default.jpg')
	#route=db.Column(db.String(100),nullable=False)
	startpoint=db.Column(db.String(20),nullable=False)
	endpoint=db.Column(db.String(20),nullable=False)
	seatsavailable=db.Column(db.Integer,nullable=False)
	starttime=db.Column(db.Time,nullable=False)
	droptime=db.Column(db.Time,nullable=False)
	date=db.Column(db.Date,nullable=False)
	fare=db.Column(db.Integer,nullable=False)
	bookings=db.relationship('Bookings',backref='businfo', lazy='dynamic')
	
	
	
	def __repr__(self):
	 return f"Bus('{self.regno}','{self.modelname}','{self.seatsavailable}','{self.startpoint}','{self.endpoint}')"
	 
class Bookings(db.Model):
	ticketno=db.Column(db.Integer,primary_key=True)
	userid=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	busregno=db.Column(db.String(20),db.ForeignKey('bus.regno'),nullable=False)
	
