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
				return render_template("register.html")
			elif pw_is_alphanum == False:
				flash('Invalid password. Alphanumeric characters only (A-Z, a-z, 0-9).')
				return render_template("register.html")
			elif 5 > len(name) or 15 < len(name):
				flash('Invalid user name. User name must be between 5 and 15 characters.')
				return render_template("register.html")
			elif 6 > len(pw) or 15 < len(pw):
				flash('Invalid password. Password must be between 6 and 15 characters.')
				return render_template("register.html")
			elif pw != verify_pw:
				flash('Passwords must match.')
				return render_template("register.html")
			elif (pw == verify_pw) and name:
				if model.check_if_user(name) == True:
					flash('You\'re already registered. Please sign in.')
					return redirect(url_for('signin'))
				else:
					model.set_user(name)
					model.set_user_pw(name, pw)
					flash('Thanks for registering! You\'re now signed in.')
					session['user'] = name
					return redirect(url_for('index'))
			else:
				flash('All fields are required.')
				return render_template("register.html")
	elif not session:
		return render_template("register.html")
	else:
		# if there's a session
		flash('You\'re already signed in.')
		return redirect(url_for('index'))
	

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
						return redirect(url_for('index'))
					else:
						flash('Your user name and/or password didn\'t match our records. Please try signing in again.')
						return render_template('signin.html')
		else:
			flash('Your user name and/or password didn\'t match our records. Please try signing in again.')
			return render_template('signin.html')
	elif not session:
		return render_template('signin.html')
	else:
		# if there's a session
		flash('You\'re already signed in.')
		return redirect(url_for('index'))

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
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('browse.html', logged_in=logged_in, not_you=not_you)
	else:
		return render_template('browse.html')

@app.route("/corpus/browse/pos")
def corpus_pos_list():
	tag_list = model.get_pos()
	first_half = tag_list[:len(tag_list)/2]
	second_half = tag_list[len(tag_list)/2:]
	if session:
		logged_in = 'Logged in as: %s.'%session['user']
		not_you = 'Not %s?'%session['user']
		return render_template('browse_list_pos.html', logged_in=logged_in, corpus_list=tag_list, not_you=not_you, first_half=first_half, second_half=second_half)
	else:
		return render_template('browse_list_pos.html', corpus_list=tag_list, first_half=first_half, second_half=second_half)
	
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
	tag_pos = 'tag_%s'%tag
	word_list = model.get_words_by_tag(tag_pos)
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

#### Visualization Functionality ####
@app.route("/vis")
def vis():
	# lists all pos, you can choose which one you want to visualize
	return render_template("vis.html")

@app.route("/vis/N")
def vis_n():
	words = model.final_tags_pos("N")
	return render_template("vis_pos.html", words=words, pos='N')

@app.route("/vis/O")
def vis_o():
	words = model.final_tags_pos("O")
	return render_template("vis_pos.html", words=words, pos='O')

@app.route("/vis/P")
def vis_p():
	words = model.final_tags_pos("P")
	return render_template("vis_pos.html", words=words, pos='P')

@app.route("/vis/M")
def vis_m():
	words = model.final_tags_pos("M")
	return render_template("vis_pos.html", words=words, pos='M')

@app.route("/vis/PV")
def vis_pv():
	words = model.final_tags_pos("PV")
	return render_template("vis_pos.html", words=words, pos='PV')

@app.route("/vis/NV")
def vis_nv():
	words = model.final_tags_pos("NV")
	return render_template("vis_pos.html", words=words, pos='NV')

@app.route("/vis/Z")
def vis_z():
	words = model.final_tags_pos("Z")
	return render_template("vis_pos.html", words=words, pos='Z')

@app.route("/vis/OP")
def vis_op():
	words = model.final_tags_pos("OP")
	return render_template("vis_pos.html", words=words, pos='OP')

@app.route("/vis/J")
def vis_j():
	words = model.final_tags_pos("J")
	return render_template("vis_pos.html", words=words, pos='J')

@app.route("/vis/A")
def vis_a():
	words = model.final_tags_pos("A")
	return render_template("vis_pos.html", words=words, pos='A')

@app.route("/vis/S")
def vis_s():
	words = model.final_tags_pos("S")
	return render_template("vis_pos.html", words=words, pos='S')

@app.route("/vis/I")
def vis_i():
	words = model.final_tags_pos("I")
	return render_template("vis_pos.html", words=words, pos='I')

@app.route("/vis/D")
def vis_d():
	words = model.final_tags_pos("D")
	return render_template("vis_pos.html", words=words, pos='D')

@app.route("/vis/V")
def vis_v():
	words = model.final_tags_pos("V")
	return render_template("vis_pos.html", words=words, pos='V')

@app.route("/vis/C")
def vis_c():
	words = model.final_tags_pos("C")
	return render_template("vis_pos.html", words=words, pos='C')

@app.route("/vis/E")
def vis_e():
	words = model.final_tags_pos("E")
	return render_template("vis_pos.html", words=words, pos='E')

@app.route("/vis/PD")
def vis_pd():
	words = model.final_tags_pos("PD")
	return render_template("vis_pos.html", words=words, pos='PD')

@app.route("/vis/EV")
def vis_ev():
	words = model.final_tags_pos("EV")
	return render_template("vis_pos.html", words=words, pos='EV')

@app.route("/vis/SC")
def vis_sc():
	words = model.final_tags_pos("SC")
	return render_template("vis_pos.html", words=words, pos='SC')


#### End Visualization Functionality ####

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT'))
