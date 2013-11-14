from flask import Flask, render_template, request, flash, redirect, url_for, session
import model

app = Flask(__name__)
app.secret_key ='secret'

@app.route("/")
def index():
	pass

@app.route("/register")
def register():
	# need to create this template
	return render_template("register.html")

@app.route("/register", methods=['POST'])
def new_user():
	# deal with user name __
	name = request.form.get('name')
	pw = request.form.get('pw')
	verify_pw = request.form.get('verify_pw')
	name_is_alphanum = model.check_alphanum(name)
	pw_is_alphanum = model.check_alphanum(pw)

	if name_is_alphanum == False:
		flash('Invalid user name. Alphanumeric characters only (A-Z, a-z, 0-9).')
		return redirect(url_for('register'))
	elif pw_is_alphanum == False:
		flash('Invalid password. Alphanumeric characters only (A-Z, a-z, 0-9).')
		return redirect(url_for('register'))
	elif 6 > len(pw) or 15 < len(pw):
		flash('Invalid password. Password must be between 6 and 15 characters.')
		return redirect(url_for('register'))
	elif pw != verify_pw:
		flash('Passwords must match.')
		return redirect(url_for('register'))
	elif (pw == verify_pw) and name:
		if model.check_if_user(name) == True:
			flash('You\'re already registered. Please sign in.')
			return redirect(url_for('signin'))
		else:
			model.set_user(name)
			model.set_user_pw(name, pw)
			flash('Thanks for registering! Please sign in to continue.')
			return redirect(url_for('signin'))
	else:
		flash('All fields are required.')
		return redirect(url_for('register'))

@app.route("/signin")
def signin():
	# need to create this
	return render_template('signin.html')

@app.route("/signin", methods=['POST'])
def sign_in():
	name = request.form.get('name')
	pw = request.form.get('pw')
	name_is_alphanum = model.check_alphanum(name)
	pw_is_alphanum = model.check_alphanum(pw)

	if name_is_alphanum == True and pw_is_alphanum == True:
		if model.auth_login(name, pw) == True:
			flash('Sign in successful!')
			# need to create this
			return redirect(url_for('home'))
	else:
		flash('Your user name and/or password didn\'t match our records. Please try signing in again.')
		return redirect(url_for('signin'))

