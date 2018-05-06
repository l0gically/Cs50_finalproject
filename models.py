### ERROR: application doesn't detect updates on the tables

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
import pytz


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# DB related
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////home/logic1010/Desktop/Developing/projects/Cs50_finalproject/final_project.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class UserInfo(UserMixin, db.Model):
	__tablename__ = "userinfo"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True, nullable= False)
	# Question: Why should a field be nullable
	password = db.Column(db.String(80), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable= False)
	activities_list = db.relationship("Activity", backref= "user", lazy=True) #lazy= True

	def __repr__(self):
		return '<UserInfo %r>' % self.username

# We want to create multipule activities and for each activity
# a New table will be created
class Activity(db.Model):
	__tablename__ = "activity" #get from the user
	id = db.Column(db.Integer, primary_key=True)
	# Creates the one to one relation between the activity and the user
	title = db.Column(db.String, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("userinfo.id"), nullable= False)
	activity_types = db.relationship("Activity_Type", backref="activity", lazy= True)

	def __repr__(self):
		return '<Activity %r>' % self.title

class Activity_Type(db.Model):
	__tablename__ = "activity_type"
	id = db.Column(db.Integer, primary_key=True)
	# the one activity this type is related with
	related_activity = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=False)
	# Name of the activity type
	activity_type_title = db.Column(db.String, nullable= False)
	durations = db.relationship("Duration", backref="activity_type", lazy=True)
	
	
class Duration(db.Model):
	__tablename__ = "duration"
	id = db.Column(db.Integer, primary_key=True)
	# It should be an Float when accessed it will be formated
	duration = db.Column(db.String, nullable=False)
	activity_type_id = db.Column(db.Integer, db.ForeignKey("activity_type.id"), nullable=False)
	# upgrade to pytz timezone lib
	create_DateTime = db.Column(db.DateTime,default=datetime.datetime.now(pytz.timezone('Africa/Cairo')))
	# Add comment column for user's comments
	comment = db.Column(db.Text, nullable=True)

db.create_all()
db.session.commit()
# saif = UserInfo(username='saif',password='password',email='example@saif.com')
# act1 = Activity(title='running',user_id=saif.id)
# saif.activities_list[act1.id-1].durations
# user.activites_list[activity_id].durations
# gets you the durations of the activity of the user