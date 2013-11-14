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
	name = request.form.get('name')
	pw = request.form.get('pw')
	verify_pw = request.form.get('verify_pw')

	if (pw == verify_pw) and name:
		if model.check_if_user(name) == True:
			flash('You\'re already registered. Please sign in.')
			# need to create this
			return redirect(url_for('signin'))
		else:
			model.set_user(name)
			model.set_user_pw(name, pw)
			flash('Thanks for registering! Please sign in to continue.')
			return redirect(url_for('signin'))
	elif pw != verify_pw:
		flash('Passwords must match.')
		return redirect(url_for('register'))
	else:
		flash('All fields are required.')
		return redirect(url_for('register'))

@app.route("/signin")
def signin():
	# need to create this
	return render_template('signin.html')

@app.route("/signin", methods=['POST'])
def sign_in():
	# need to deal with hashing
	name = request.form.get('name')
	pw = request.form.get('pw')

	# need to write fn in model
	if model.auth_login(name, pw):
		pass
