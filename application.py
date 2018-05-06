from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from passlib.hash import sha256_crypt
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from form import RegistrationForm, LoginForm
from models import *
from API import *
import datetime
import pytz


login_manager = LoginManager()
login_manager.init_app(app)

# That is how loginmanager knows where to get user's info to fill in
@login_manager.user_loader
def load_user(user_id):
	return  UserInfo.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
	return redirect(url_for('login'))

@app.route("/")
def home():
	return render_template('welcome.html')

@app.route('/stopwatch', methods = ['GET', 'POST'])
def stopwatch():
	if request.method == 'POST':
		return jsonify(dict(user=current_user.username))
	elif current_user.is_authenticated:
		activities = current_user.activities_list
		return render_template('stopwatch.html', activities=activities)
	return render_template('stopwatch.html')


# idea: /<username>
# parameter = username
# <!-- {{url_for('progress'), username = current_user.username }} -->
# Update activity Name
# Move to another activity
@app.route('/stopwatch/create-activity', methods = ['GET'])
@login_required
def CreateActivity():

	# Check for input
	new_act = request.args.get("new_act")
	new_act_type = request.args.get("new_act_type")
	new_act_type = new_act_type.split(",")

	if new_act is not None and new_act_type is not None:
		new_act = new_act.strip("!@#$%^&*(){}[]\\\'\" ,.;:`~<>=+-|")
		# See if activity already exist
		existing_activity = Activity.query.filter_by(title=new_act, user_id= current_user.id).first()
		# only add the types
		if existing_activity:
			act = []
			# Insert types into db
			for Type in new_act_type:
				new_type = Activity_Type(activity_type_title=Type, related_activity=existing_activity.id)
				save(new_type)
				act.append(dict(act_type=Type))
		elif not existing_activity:
			# Insert the activity into db
			activity = Activity(title= new_act,user_id= current_user.id)
			save(activity)
			act = []
			# Insert types into db
			for Type in new_act_type:
				new_type = Activity_Type(activity_type_title=Type, related_activity=activity.id)
				save(new_type)
				act.append(dict(act_type=Type))
		return jsonify(act)
	# NOTE: change the return type or how JS responds
	return jsonify([])

@app.route('/stopwatch/add-activity-type', methods = ['GET'])
@login_required
def AddActivityType():
	pass

@app.route('/stopwatch/del-activity-type', methods = ['GET'])
@login_required
def DelActivityType():
	pass

@app.route('/stopwatch/delete-activity', methods = ['GET'])
@login_required
def DeleteActivity():
	# Get activities to delete from the getJson function
	# Get the activity to delete
	# delete all the related durations and then types and then the activity it's self
	rm_act = request.args.get("rm_act")
	rm_act_type = request.args.get("rm_act_type")

	act = Activity.query.filter_by(title=rm_act, user_id=current_user.id).first()
	if rm_act_type is None:
#	print ("this is the title: {}").format(thetitle)
	# Get the activity and check for any entries in duration
		if act:
			type_check = Activity_Type.query.filter_by(related_activity=act.id).all()
			# Select durations associated with activity first to delete
			for types in type_check:
				if types.durations is not None:
					for dur in types.durations:
						delete(dur)
				delete(types)
			delete(act)
	else:
		Act_type = Activity_Type.query.filter_by(activity_type_title=rm_act_type,related_activity=act.id).first()
		for dur in Act_type.durations:
			delete(dur)
		delete(Act_type)

			#print("this is the act_id: {}").format(act.id)
			# delete the activity
	return jsonify([])

@app.route('/stopwatch/update-activity-types', methods = ['GET'])
@login_required
def UpdateTypes():
	activity = request.args.get("act")

	# query the related types
	act = Activity.query.filter_by(user_id=current_user.id,title=activity).first()
	types = Activity_Type.query.filter_by(related_activity=act.id).all()

	act_types = []
	# Return the types list
	for actype in types:
		act_types.append(dict(act_type=actype.activity_type_title))
	return jsonify(act_types)

# The problem is that when the table is empty the id
@app.route('/stopwatch/add-duration', methods = ['GET'])
@login_required
def AddDuration():
	acti = str(request.args.get("activity_title"))
	acti_type = request.args.get("activity_type_title")
	dur    = request.args.get("neededtime")
	converted_time_db = convertMilli(dur,clean = False)
	converted_time_view = convertMilli(dur,clean = True)

	# Catch if if time is 0 empty
	if converted_time_db == '0 . 0':
		return jsonify([])
	act = Activity.query.filter_by(title=acti,user_id=current_user.id).first()

	if act:
		act_type= Activity_Type.query.filter_by(activity_type_title=acti_type,related_activity=act.id).first()
		if act_type:
			new_dur = Duration(duration= converted_time_db, create_DateTime= datetime.datetime.now(pytz.timezone('Africa/Cairo')),activity_type_id=act_type.id)
			save(new_dur)
			dt = new_dur.create_DateTime
			dtime = str(dt.strftime("%A, %d. %B %Y | %I:%M %p")).split('|')
		#	dtimestart = dt
			dur_toreturn = dict(time=converted_time_view, d=dtime[0],t=dtime[1], dur_id=new_dur.id,
			comment=new_dur.comment,acti_type=acti_type,acti=acti)
			return jsonify(dur_toreturn)
	return jsonify([])

@app.route('/stopwatch/remove-duration', methods = ['GET'])
@login_required
def removeDuration():
	dur_id = int(request.args.get("but"))
	toremove = Duration.query.get(dur_id);
	delete(toremove)
	return jsonify([])

@app.route('/stopwatch/show-activity-durations', methods = ['GET'])
@login_required
def showDurations():
	# Get the activity
	act_title = request.args.get("act_title")
	# Get the activity searched for from select
	act_name = Activity.query.filter_by(title=act_title).first()
	# Get all the related activity types
	act_types = Activity_Type.query.filter_by(related_activity=act_name.id).all()
	# Get all its durations
	#	dtimestart = dt
	durs = []
	# Make array of dicts for JS to display
	for Type in act_types:
		for dur in Type.durations:
			# format the time
			dt = dur.create_DateTime
			dtime = str(dt.strftime("%A, %d. %B %Y | %I:%M %p")).split('|')
			durs.append(dict(time=dur.duration, d=dtime[0], t=dtime[1], dur_id=dur.id, comment=dur.comment,acti_type=Type.activity_type_title,acti=act_title))
	return jsonify(durs)
@app.route('/stopwatch/show-type-durations', methods=['GET'])
@login_required
def showTypeDurations():
	act_type_title  = request.args.get("act_type")
	act_title = request.args.get("act_title")
	if act_type_title is not None and act_title is not None:
		act_name = Activity.query.filter_by(title=act_title).first()
		# Get all the related activity types
		act_type = Activity_Type.query.filter_by(related_activity=act_name.id,activity_type_title=act_type_title).first()
		durs = []
		act_durs = act_type.durations
		for dur in act_durs:
			dt = dur.create_DateTime
			dtime = str(dt.strftime("%A, %d. %B %Y | %I:%M %p")).split('|')
			durs.append(dict(time=dur.duration, d=dtime[0], t=dtime[1], dur_id=dur.id, comment=dur.comment,acti_type=act_type_title,acti=act_title))
		return jsonify(durs)
	return jsonify([])

@app.route('/stopwatch/duration-comment', methods = ['POST'])
@login_required
def Durationcomment():
	""" Add comments to a specific duration and update it when changed """
	# get the comment text
	commentText = request.form["commenttext"]
	dur_id = request.form["dur_id"]

	# access the duration by id
	the_duration = Duration.query.get(dur_id)
	the_duration.comment = commentText
	db.session.commit()
	return jsonify()


@app.route('/history', methods = ['GET','POST'])
@login_required
def History():
	All_info = UserInfo.query.get(current_user.id)
	activities = []
	activity_types = []
	durations = []
	if All_info.activities_list is not None:
		for activity in All_info.activities_list:
			activities.append(dict(act_id=activity.id,acti=activity.title))
			if activity.activity_types is not None:
				for activity_type in activity.activity_types:
					activity_types.append(dict(act_type_id=activity_type.id,act_type=activity_type.activity_type_title))
					if activity_type.durations is not None:
						for dur in activity_type.durations:
							dt = dur.create_DateTime
							dtime = str(dt.strftime("%A, %d. %B %Y | %I:%M %p")).split('|')
							dformated = str(dt.strftime("%Y-%m-%d"))
							durations.append(dict(time=dur.duration, d=dtime[0],dformated=dformated , t=dtime[1], dur_id=dur.id, comment=dur.comment,acti=activity.title,act_type=activity_type.activity_type_title))
	#return jsonify(activities,activity_types,durations)
	return render_template("History.html",activities=activities,act_types=activity_types,durations=durations)





@app.route('/progress', methods = ['GET','POST'])
@login_required
def progress():

	return render_template('progress.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():

	form = RegistrationForm(request.form)

	if request.method == 'POST' and form.validate_on_submit():
		username = form.username.data
		pwd      = sha256_crypt.hash(form.password.data)
		email    = form.email.data
		error_messages = []

		# check if the username is unique
		existing_username = UserInfo.query.filter_by(username=username).first()
		# check if any other user has the same password
		# Get the user by email and see if there is one
		existing_email = UserInfo.query.filter_by(email=email).first()

		if existing_username:
			error_messages.append("username taken try another one")
		if existing_email:
			error_messages.append("This e-mail belongs to another user")

		if existing_username or existing_email:
			return render_template('register.html', form=form, errors=error_messages)

		# If username and email are both new add the new user
		elif not existing_username and not existing_email:
		# Insert new user to db
			new_user = UserInfo(username=username,password=pwd,email=email)
			save(new_user)
			return redirect(url_for('login'), code= 307)
	return render_template('register.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():

	form = LoginForm(request.form)

	if form.validate_on_submit():
		# Get user's data
		username = form.username.data
		pwd = form.password.data

		existing_user = UserInfo.query.filter_by(username=username).first()
		verified = None
		# See if user exists in db
		if existing_user:
			# if the user exists verify his password
			verified = sha256_crypt.verify(pwd, existing_user.password)
			if verified:
				login_user(existing_user)
				return redirect(url_for('stopwatch'))
		if not existing_user or not verified :
			return render_template('login.html', form=form, pwd_verified = verified, user_verified = existing_user)

		flash('user not found')
		return redirect(url_for('register'))

	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))



if __name__ == '__main__':
	app.run(debug=True)
