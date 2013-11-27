from flask import Flask, render_template, request, flash, redirect, url_for, session, Markup, Response
import model
import os

app = Flask(__name__)
app.secret_key = os.environ.get('flask_secretkey')

#### Basic Functionality ####

@app.route("/")
def index():
	if not session:
		return render_template('index.html')
	else:
		greeting = 'Hello %s!'%session['user']
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('index.html', greeting=greeting, logged_in=logged_in, not_you=not_you)

@app.route("/register", methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
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
					flash('Thanks for registering! You\'re now signed in.')
					session['user'] = name
					ip_address = request.remote_addr
					last_url = model.get_last_url(ip_address)
					if last_url != "/signin" and last_url != "/register":
						# redirect back to where they came from
						return redirect(last_url)
					else:
						return redirect(url_for('index'))
			else:
				flash('All fields are required.')
				return redirect(url_for('register'))
	elif not session:
		url = request.referrer
		ip_address = request.remote_addr
		model.keep_url(url, ip_address)
		return render_template("register.html")
	else:
		# if there's a session
		flash('You\'re already signed in.')
		return redirect(request.referrer)
	

@app.route("/signin", methods=['GET', 'POST'])
def signin():
	if request.method =='POST':
		name = request.form.get('name')
		pw = request.form.get('pw')

		if name and pw:
			if len(name) > 0 and len(pw) > 0:
				name_is_alphanum = model.check_alphanum(name)
				pw_is_alphanum = model.check_alphanum(pw)
				if name_is_alphanum == True and pw_is_alphanum == True:
					if model.auth_login(name, pw) == True:
						session['user'] = name
						ip_address = request.remote_addr
						last_url = model.get_last_url(ip_address)
						if last_url != "/signin" and last_url != "/register":
							return redirect(last_url)
						else:
							return redirect(url_for('index'))
					else:
						flash('Your user name and/or password didn\'t match our records. Please try signing in again.')
						return redirect(url_for('signin'))
		else:
			flash('Your user name and/or password didn\'t match our records. Please try signing in again.')
			return redirect(url_for('signin'))
	elif not session:
		url = request.referrer
		ip_address = request.remote_addr
		model.keep_url(url, ip_address)
		return render_template('signin.html')
	else:
		# if there's a session
		flash('You\'re already signed in.')
		return redirect(request.referrer)

@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('index'))

@app.route("/about")
def about_tt():
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('about.html', logged_in=logged_in, not_you=not_you)
	else:
		return render_template('about.html')

@app.route("/about/tt")
def abt_tt():
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('about_tt.html', logged_in=logged_in, not_you=not_you)
	else:
		return render_template('about_tt.html')

@app.route("/about/matc")
def abt_matc():
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('about_matc.html', logged_in=logged_in, not_you=not_you)
	else:
		return render_template('about_matc.html')

@app.route("/about/ttud")
def abt_ttud():
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('about_ttud.html', logged_in=logged_in, not_you=not_you)
	else:
		return render_template('about_ttud.html')

@app.route("/about/faqs")
def abt_faqs():
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('about_faqs.html', logged_in=logged_in, not_you=not_you)
	else:
		return render_template('about_faqs.html')

@app.route("/corpus")
def corpus():
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('corpus.html', logged_in=logged_in, not_you=not_you)
	else:
		return render_template('corpus.html')

@app.route("/contact")
def contact_me():
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('contact_me.html', logged_in=logged_in, not_you=not_you)
	else:
		return render_template('contact_me.html')

@app.route("/linguists")
def linguist_info():
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('info_for_linguists.html', logged_in=logged_in, not_you=not_you)
	else:
		return render_template('info_for_linguists.html')

@app.route("/guide")
def guide():
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('pos_guide.html', logged_in=logged_in, not_you=not_you)
	else:
		return render_template('pos_guide.html')


#### End Basic Functionality ####

#### Corpus Functionality ####

## None of these will work until people tag in the game ##

# check if i need to redo any of these fns since i re-ordered pos tag thing?

@app.route("/corpus/download")
def corpus_download():
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('corpus_download_main.html', logged_in=logged_in, not_you=not_you)
	else:
		return render_template('corpus_download_main.html')

@app.route("/corpus/download/pos")
def corpus_download_pos():
	corpus = model.get_corpus_pos()
	return Response(corpus, mimetype='text/csv')

@app.route("/corpus/download/words")
def corpus_download_words():
	corpus = model.get_corpus_words()
	return Response(corpus, mimetype='text/csv')
	
@app.route("/corpus/browse")
def corpus_browse():
	# i'd like to add searching ability too
	# for searching, they'd just have to search like 'word_whatever they're searching for' etc
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('browse.html', logged_in=logged_in, not_you=not_you)
	else:
		return render_template('browse.html')

@app.route("/corpus/browse/pos")
def corpus_pos_list():
	tag_list = model.get_pos()
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('browse_list_pos.html', logged_in=logged_in, corpus_list=tag_list, not_you=not_you)
	else:
		return render_template('browse_list_pos.html', corpus_list=tag_list)
	
@app.route("/corpus/browse/words")
def corpus_words_list():
	word_list = model.get_words()
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('browse_list_words.html', logged_in=logged_in, corpus_list=word_list, not_you=not_you)
	else:
		return render_template('browse_list_words.html', corpus_list=word_list)

@app.route("/corpus/browse/pos/<tag>")
def corpus_pos(tag):
	word_list = model.get_words_by_tag(tag)
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('browse_words_by_pos.html', logged_in=logged_in, word_list=word_list, tag=tag, not_you=not_you)
	else:
		return render_template('browse_words_by_pos.html', word_list=word_list, tag=tag)

@app.route("/corpus/browse/words/<word>")
def corpus_word(word):
	tag_list = model.get_tags_by_word(word)
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('browse_pos_by_word.html', logged_in=logged_in, tag_list=tag_list, word=word, not_you=not_you)
	else:
		return render_template('browse_pos_by_word.html', tag_list=tag_list, word=word)

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

		tweet_for_game = unicode(tweet_for_game, 'utf-8', errors='replace')

		for tweet in tweet_list:
			tweet = unicode(tweet, 'utf-8', errors='replace')

		pos_sents_tags = model.break_pos_sents(model.get_pos_sentences())
		first_half = pos_sents_tags[:len(pos_sents_tags)/2]
		second_half = pos_sents_tags[len(pos_sents_tags)/2:]

		logged_in = 'Logged in as: %s.'%user
		not_you = 'Not %s?'%session['user']

		return render_template('game.html', word = word_for_game, tweet = Markup(tweet_for_game).unescape(), user_points=user_points, tweet_list=tweet_list, first_half=first_half, second_half=second_half, logged_in=logged_in, user=user, not_you=not_you)
	

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

@app.route("/game/more_tweets", methods=['POST'])
def new_tweet():
	word = request.form.get('word')
	tweet = request.form.get('tweet')
	tweet_list = model.get_another_tweet(word, tweet)
	tweets_gotten = request.form.get('tweets_gotten')
	if tweets_gotten > 0:
		if len(tweet_list) >= tweets_gotten:
			new_tweet = tweet_list[-tweets_gotten]
			if new_tweet == tweet:
				return "There are no more tweets with \"%s\" in them."%word
			else:
				new_tweet = unicode(new_tweet, 'utf-8', errors='replace')
				return render_template('moretweets.html', tweet=Markup(new_tweet).unescape())
		else:
			new_tweet = "There are no more tweets with \"%s\" in them."%word
			return render_template('moretweets.html', tweet=new_tweet)
	else:
		new_tweet = "There are no more tweets with \"%s\" in them."%word
		return render_template('moretweets.html', tweet=new_tweet)

@app.route("/game/howto")
def howto():
	return render_template("tutorial.html")

@app.route("/game/posreference")
def photoref():
	return render_template("photoreference.html")


@app.route("/game/more_tweets/new")
def more_tweets(tweet):
	return render_template('moretweets.html', tweet=tweet)

@app.route("/game/points")
def show_points():
	if not session:
		scores = model.get_top_scores()
		return render_template("top_points.html", scores=scores )
	if session['user']:
		user = session['user']
		scores = model.get_top_scores()
		user_name_pts = "user_%s_pts"%user
		user_score = model.get_string_num(user_name_pts)
		logged_in = 'Logged in as: %s.'%user
		not_you = 'Not %s?'%session['user']
		return render_template("user_and_top_points.html", scores=scores, user_score=user_score, user=user, logged_in=logged_in, not_you=not_you)


#### End Game Functionality ####

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT'))
