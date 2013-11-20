from flask import Flask, render_template, request, flash, redirect, url_for, session
import model
import random

app = Flask(__name__)
app.secret_key ='secret'

#### Basic Functionality ####

@app.route("/")
def index():
	# do something with session user in greeting
	return render_template('index.html')

@app.route("/register")
def register():
	# do something about if already signed in
	return render_template("register.html")

@app.route("/register", methods=['POST'])
def new_user():
	name = request.form.get('name')
	pw = request.form.get('pw')
	verify_pw = request.form.get('verify_pw')

	if len(name) > 0 and len(pw) > 0 and len(verify_pw) > 0:
		name_is_alphanum = model.check_alphanum(name)
		pw_is_alphanum = model.check_alphanum(pw)
		if name_is_alphanum == False:
			flash('Invalid user name. Alphanumeric characters only (A-Z, a-z, 0-9).')
			return redirect(url_for('register'))
		elif pw_is_alphanum == False:
			flash('Invalid password. Alphanumeric characters only (A-Z, a-z, 0-9).')
			return redirect(url_for('register'))
		elif 6 > len(name) or 15 < len(name):
			flash('Invalid user name. User name must be between 6 and 15 characters.')
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
	# do something about if they're already signed in
	return render_template('signin.html')

@app.route("/signin", methods=['POST'])
def sign_in():
	name = request.form.get('name')
	pw = request.form.get('pw')

	if name and pw:
		if len(name) > 0 and len(pw) > 0:
			name_is_alphanum = model.check_alphanum(name)
			pw_is_alphanum = model.check_alphanum(pw)
			if name_is_alphanum == True and pw_is_alphanum == True:
				if model.auth_login(name, pw) == True:
					flash('Sign in successful!')
					session['user'] = name
					return redirect(url_for('index'))
				else:
					flash('Your user name and/or password didn\'t match our records. Please try signing in again.')
					return redirect(url_for('signin'))
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
	# for searching, they'd just have to search like 'word_whatever they're searching for' etc
	return render_template('browse.html')

@app.route("/corpus/browse/pos")
def corpus_pos_list():
	tag_list = model.get_pos()
	return render_template('browse_list_pos.html', corpus_list = tag_list)
	
@app.route("/corpus/browse/words")
def corpus_words_list():
	word_list = model.get_words()
	return render_template('browse_list_words.html', corpus_list = word_list)

@app.route("/corpus/browse/pos/<tag>")
def corpus_pos(tag):
	word_list = model.get_words_by_tag(tag)
	return render_template('browse_words_by_pos.html', word_list = word_list, tag = tag)
	pass

@app.route("/corpus/browse/words/<word>")
def corpus_word(word):
	tag_list = model.get_tags_by_word(word)
	return render_template('browse_pos_by_word.html', tag_list = tag_list, word = word)

#### End Corpus Functionality ####


#### Game Functionality ####

@app.route("/game")
def game():
	if not session:
		return render_template('login_tt.html')
	if session['user']:
		game_info = model.get_words_tweets_game()
		word_for_game = game_info[0]
		tweet_for_game = game_info[1]
		tweet_list = game_info[2]
		user = session['user']
		user_name_pts = "user_%s_pts"%user
		user_points = model.get_string_num(user_name_pts)
		try:
			unicode(tweet_for_game, 'ascii')
		except UnicodeError:
			tweet_for_game = unicode(tweet_for_game, 'utf-8')
		else:
			pass

		for tweet in tweet_list:
			try:
				unicode(tweet, 'ascii')
			except UnicodeError:
				tweet = unicode(tweet, 'utf-8')
			else:
				pass
		pos_sents_tags = model.break_pos_sents(model.get_pos_sentences())

		return render_template('game.html', word = word_for_game, tweet = tweet_for_game, tags_sentences = pos_sents_tags, user_points=user_points)
	

@app.route("/game", methods=['POST'])
def play_game():
	tag = request.form.get('tag')
	word = request.form.get('word')
	tweet = request.form.get('tweet')
	user = session['user']
	if tag and word:
		# set the tag for the user and the tweet
		model.tag_word_game(word, tag, user, tweet)
		# add points and set final tag if needed
		model.add_pts_game(word, tag, user)
		# retrieve how many points user has
		user_name_pts = "user_%s_pts"%user
		num_points = model.get_string_num(user_name_pts)
		return str(num_points)
		# return redirect(url_for('game'))


@app.route("/game/more_tweets", methods=['POST'])
def new_tweet():
	word = request.form.get('word')
	tweet = request.form.get('tweet')
	tweet_list = model.get_another_tweet(word, tweet)
	if tweet_list:
		if len(tweet_list) > 1:
			new_tweet = tweet_list.pop()
			if new_tweet == tweet:
				return "There are no more tweets with %s in them."%word
			else:
				try:
					unicode(new_tweet, 'ascii')
				except UnicodeError:
					new_tweet = unicode(new_tweet, 'utf-8')
				return render_template('moretweets.html', tweet=new_tweet)
		else:
			new_tweet = "There are no more tweets with %s in them."%word
			return render_template('moretweets.html', tweet=new_tweet)

	else:
		new_tweet = "There are no more tweets with %s in them."%word
		return render_template('moretweets.html', tweet=new_tweet)



@app.route("/game/more_tweets/new")
def more_tweets(tweet):
	return render_template('moretweets.html', tweet=tweet)

@app.route("/game/points")
def show_points():
	if not session:
		scores = model.get_top_scores()
		return render_template("top_points.html", user_list = scores[0], points = scores[1] )
	if session['user']:
		user = session['user']
		scores = model.get_top_scores()
		user_name_pts = "user_%s_pts"%user
		user_score = model.get_string_num(user_name_pts)
		return render_template("user_and_top_points.html", user_list=scores[0], points=scores[1], user_score=user_score, user_name=user)


#### End Game Functionality ####

if __name__ == "__main__":
    app.run(debug = True)
