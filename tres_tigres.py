from flask import Flask, render_template, request, flash, redirect, url_for, session
import model

app = Flask(__name__)
app.secret_key ='secret'

#### Basic Functionality ####

@app.route("/")
def index():
	return render_template('index.html')

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
		# add this for user name too
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
			session['user'] = name
			# do something with session here
			return redirect(url_for('index'))
	else:
		flash('Your user name and/or password didn\'t match our records. Please try signing in again.')
		return redirect(url_for('signin'))

@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('index'))

@app.route("/about")
def about_tt():
	return render_template('about.html')

@app.route("/about/tt")
def abt_tt():
	return render_template('about_tt.html')

@app.route("/about/matc")
def abt_matc():
	return render_template('about_matc.html')

@app.route("/about/ttud")
def abt_ttud():
	return render_template('about_ttud.html')

@app.route("/about/faqs")
def abt_faqs():
	return render_template('about_faqs.html')

@app.route("/corpus")
def corpus():
	return render_template('corpus.html')

@app.route("/contact")
def contact_me():
	return render_template('contact_me.html')

@app.route("/linguists")
def linguist_info():
	return render_template('info_for_linguists.html')
@app.route("/guide")
def guide():
	return render_template('pos_guide.html')

@app.route("/guide/download")
def dl_guide():
	return render_template('download_guide.html')

#### End Basic Functionality ####

#### Corpus Functionality ####

## None of these will work until people tag in the game ##

@app.route("/corpus/download")
def corpus_download():
	return render_template('corpus_download_main.html')

@app.route("/corpus/download/pos")
def corpus_download_pos():
	corpus = model.get_corpus_pos()
	# need to be able to dl this
	return render_template('corpus_download.html', corpus = corpus)


@app.route("/corpus/download/words")
def corpus_download_words():
	# need to be able to dl this
	corpus = model.get_corpus_words()
	return render_template('corpus_download.html', corpus = corpus)

@app.route("/corpus/browse")
def corpus_browse():
	# i'd like to add searching ability too
	return render_template('browse.html')

@app.route("/corpus/browse/pos")
def corpus_pos_list():
	tag_list = model.get_pos()
	# display clickable list of pos tags used in corpus
	return render_template('browse_list_pos.html', corpus_list = tag_list)
	
@app.route("/corpus/browse/words")
def corpus_words_list():
	word_list = model.get_words()
	# display clickable list of words in corpus
	return render_template('browse_list_words.html', corpus_list = word_list)

@app.route("/corpus/browse/pos/<tag>")
def corpus_pos(tag):
	word_list = model.get_words_by_tag(tag)
	# display clickable list of words assoc with that tag
	return render_template('browse_words_by_pos.html', word_list = word_list, tag = tag)
	pass

@app.route("/corpus/browse/words/<word>")
def corpus_word(word):
	tag_list = model.get_tags_by_word(word)
	# display clickable list of tags assoc with that word
	return render_template('browse_pos_by_word.html', tag_list = tag_list, word = word)

#### End Corpus Functionality ####


#### Game Functionality ####

@app.route("/tres_tigres")
def game():
	# just for now:
	return redirect(url_for('index'))

#### End Game Functionality ####

if __name__ == "__main__":
    app.run(debug = True)
