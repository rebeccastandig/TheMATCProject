import redis
import hashlib
import random

r_server = redis.StrictRedis(host="redistogo:a115bdd0d5837ac2394d911e7aa5d541@grideye.redistogo.com", port=9612)

def md5_hash(password):
    return hashlib.md5(password).hexdigest()

def get_list(key):
	# returns list via key
	# returns empty list if key hadn't been created prior to checking
	return r_server.lrange(key, 0, -1)

def get_num_list(key):
	# returns len(list), retrieved via key
	# returns 0 if key hadn't been created prior to checking
	return r_server.llen(key)

def get_string_num(key):
	# returns string via key.
	# value of key can be either string or number
	# doesn't return anything if key hadn't been created prior to checking
	return r_server.get(key)

#### Basic Setting Values ####

def set_word(word):
	# sets word_(word)
	# word must be string
	word_word = "word_%s"%word
	r_server.set(word_word, word)

def set_tag(pos):
	# sets tag_(POS)
	# pos must be string
	tag_pos = 'tag_%s'%pos
	r_server.set(tag_pos, pos)

def set_sent_pos_tag(pos, sentences):
	# sets sent_(POS)_tag
	# pos must be string
	# sentence(s) must be list in ['sent', 'sent2'] format
	sent_pos_tag = 'sent_%s_tag'%pos
	tag_pos = 'tag_%s'%pos
	r_server.rpush(sent_pos_tag, tag_pos)
	for sentence in sentences:
		r_server.rpush(sent_pos_tag, sentence)
	

def set_user(user):
	# sets user_(name)
	# user must be string
	user_name = 'user_%s'%user
	user_name_pw = 'user_%s_pw'%user
	user_name_pts = 'user_%s_pts'%user
	r_server.rpush(user_name, user)
	r_server.rpush(user_name, user_name_pw)
	r_server.rpush(user_name, user_name_pts)
	r_server.incrby(user_name_pts, 0)
	add_all_users(user)
	add_all_points(user)

def set_user_pw(user, pw):
	# sets user_(name)_pw
	# user & pw must be strings
	user_name_pw = 'user_%s_pw'%user
	password = md5_hash(pw)
	r_server.set(user_name_pw, password)

#### End Basic Setting Values ####

#### Basic Setting & Appending ####

def add_all_words(game_word_list):
	# sets & appends to words.
	# requires game words to be in a list, in '(word)' format
	prior_word_list = get_list('words')
	for word in game_word_list:
		word_word = 'word_%s'%word
		if word_word in prior_word_list:
			pass
		else:
			r_server.rpush('words', word_word)

def add_all_tags(pos_tag_list):
	# sets & appends to tags.
	# requires POS_tags to be in a list, in '(POS)' format
	prior_tags_list = get_list('tags')
	for pos in pos_tag_list:
		tag_pos = 'tag_%s'%pos
		if tag_pos in prior_tags_list:
			pass
		else:
			r_server.rpush('tags', tag_pos)

def add_all_users(user):
	# sets & appends to users.
	# user must be string
	prior_users_list = get_list('users')
	user_name = 'user_%s'%user
	if user_name in prior_users_list:
		pass
	else:
		r_server.rpush('users', user_name)

def add_all_points(user):
	# sets & appends to points
	# user must be string
	prior_points_list = get_list('points')
	user_name_pts = 'user_%s_pts'%user
	if user_name_pts in prior_points_list:
		pass
	else:
		r_server.rpush('points', user_name_pts)

def add_all_sentences(pos_list):
	# sets & appends to sentences
	# pos must be list, in '(POS)' format
	prior_sent_list = get_list('sentences')
	for pos in pos_list:
		sent_pos_tag = 'sent_%s_tag'%pos
		if sent_pos_tag in prior_sent_list:
			pass
		else:
			r_server.rpush('sentences', sent_pos_tag)

def add_word_tweets(word, tweets):
	# sets & appends to word_(word)_tweets
	# tweets must be list, in '(tweet)' format
	# word must be string
	word_word_tweets = "word_%s_tweets"%word
	prior_tweet_list = get_list(word_word_tweets)
	for tweet in tweets:
		if tweet in prior_tweet_list:
			pass
		elif tweet == "":
			pass
		else:
			r_server.rpush(word_word_tweets, tweet)

def add_user_pts(user_name_pts, pts):
	# sets & adds user_(name)_pts
	# user must be string 'user_(name)_pts'
	# pts must be number, can be negative to decrease
	r_server.incrby(user_name_pts, pts)
	# leaving pts open so i can write diff function that will discriminate when to add 10 vs 5

def add_user_tag_word(user, word, tag):
	# sets & appends to user_(name)_tag_word_(word)
	# user & word must be strings
	# tag must be string in 'tag_(POS)' format
	user_name_tag_word_word = 'user_%s_tag_word_%s'%(user, word)
	prior_tag_list = get_list(user_name_tag_word_word)
	if tag in prior_tag_list:
		pass
	else:
		r_server.rpush(user_name_tag_word_word, tag)

def add_tag_word_tag_pos(word, pos, user):
	# sets & appends to tag_word_(word)_tag_(POS)
	# word & pos must be strings
	# user must be string in 'user_(name)' format
	tag_word_word_tag_pos = 'tag_word_%s_tag_%s'%(word, pos)
	prior_user_list = get_list(tag_word_word_tag_pos)
	if user in prior_user_list:
		pass
	else:
		r_server.rpush(tag_word_word_tag_pos, user)

def add_tweet_tag_word_tag_pos(word, pos, tweet_list):
	# sets & appends to tweet_tag_word_(word)_tag_(POS)
	# word & pos must be string
	# tweet(s) must be in a list, in '(tweet)' format
	tweet_tag_word_word_tag_pos = 'tweet_tag_word_%s_tag_%s'%(word, pos)
	prior_tweet_list = get_list(tweet_tag_word_word_tag_pos)
	for tweet in tweet_list:
		if tweet in prior_tweet_list:
			pass
		else:
			r_server.rpush(tweet_tag_word_word_tag_pos, tweet)

def add_tagged_words_pos(pos, word_list):
	# sets & appends to tagged_words_tag_(POS)
	# pos must be string
	# word(s) must be in a list, in 'word_(word)' format
	tagged_words_tag_pos = 'tagged_words_tag_%s'%pos
	prior_word_list = get_list(tagged_words_tag_pos)
	for word in word_list:
		if word in prior_word_list:
			pass
		else:
			r_server.rpush(tagged_words_tag_pos, word)

def add_user_words_tagged(user, word_list):
	# sets & appends to user_(name)_words_tagged
	# user must be string
	# word(s) must be list, in 'tag_word_(word)_tag_(POS)' format
	user_name_words_tagged = 'user_%s_words_tagged'%user
	prior_word_list = get_list(user_name_words_tagged)
	for word in word_list:
		if word in prior_word_list:
			pass
		else:
			r_server.rpush(user_name_words_tagged, word)

def add_final_tag(word, tag_list):
	# sets & appends to final_tag_word_(word)
	# word must be string
	# tag(s) must be list, in 'tag_(POS)' format
	final_tag_word_word = 'final_tag_word_%s'%word
	prior_tag_list = get_list(final_tag_word_word)
	for tag in tag_list:
		if tag in prior_tag_list:
			pass
		else:
			r_server.rpush(final_tag_word_word, tag)

def set_num_tweets_final_tag_pos(word, pos):
	# sets final_tag_word_(word)_tag_(POS)
	# word & pos must be string
	# checks len(tweet_tag_word_(word)_tag_(POS))
	final_tag_word_word_tag_pos = 'final_tag_word_%s_tag_%s'%(word, pos)
	tweet_tag_word_word_tag_pos = 'tweet_tag_word_%s_tag_%s'%(word, pos)
	num_tweets = get_num_list(tweet_tag_word_word_tag_pos)
	r_server.set(final_tag_word_word_tag_pos, num_tweets)

def set_game_words_tweets(word_list, tweet):
	# ***need to check to make sure no words are '(pos)_tweets' or anything like that before adding to word list.***
	add_all_words(word_list)
	for word in word_list:
		set_word(word)
		add_word_tweets(word, tweet)
	print "success"

#### End Basic Setting & Appending ####

#### Flask Uses ####

def check_if_user(user):
	# checks to see if user_(name) exists for user.
	# returns True or False
	user_name = 'user_%s'%user
	return r_server.exists(user_name)

def check_alphanum(string):
	# checks if a string is A-Z, a-z, 0-9 characters only; ord() must be b/t 48 and 122
	for item in string:
		alphanum = True
		if ord(item) < 48:
			alphanum = False
			return alphanum
		elif ord(item) > 122:
			alphanum = False
			return alphanum
	return alphanum


def auth_login(user_name, pw):
	name_key = 'user_%s'%user_name
	user_info = get_list(name_key)
	
	authenticated = False
	if user_info:
		if user_name == user_info[0]:
			password = get_string_num(user_info[1])
			if md5_hash(pw) == password:
				authenticated = True
				return authenticated
	else:
		return authenticated

def get_corpus_pos():
	# sec 1 of corpus = list of words tagged w/pos
	#  so it'll be a dictionary with the key == POS, value == list of words

	corpus = {}
	tag_list = get_list('tags')
	for tag in tag_list:
		key = 'tagged_words_%s'%tag
		# returns ['word_(word)','word_(diff word)']
		tagged_words = get_list(key)
		# returns '(pos)' or '(diff pos)'
		tag_name = get_string_num(tag)
		word_list = []
		if len(tagged_words) > 0:
			for word_word in tagged_words:
				# returns '(word)'
				word = get_string_num(word_word)
				word_list.append(word)
			corpus[tag_name] = word_list
	return corpus
	

def get_corpus_words():
	# sec 2 of corpus = list of POS for words
	# so it'll be a dict with the key == word, value == list of POS

	corpus = {}
	word_list = get_list('words')
	for word_word in word_list:
		key = 'final_tag_%s'%word_word
		# returns ['tag_(pos)', 'tag_(diff pos)']
		tag_list = get_list(key)
		# returns '(word)'
		word = get_string_num(word_word)
		pos_list = []
		if len(tag_list) > 0:
			for tag_tag in tag_list:
				# returns '(tag)'
				tag = get_string_num(tag_tag)
				pos_list.append(tag)
			corpus[word] = pos_list
	return corpus 

def get_pos():
	# returns list of tags ['tag_NP', 'tag_V', etc]
	tag_list = get_list('tags')
	tags = []
	for tag in tag_list:
		# returns ['(pos)','(pos)']
		pos = get_string_num(tag)
		tags.append(pos)
	tags.sort()
	return tags

def get_words():
	# returns list of words ['word', 'glvod', etc]
	word_list = get_list('words')
	words = []
	for word_word in word_list:
		key = 'final_tag_%s'%word_word
		tag_list = get_list(key)
		if len(tag_list) > 0:
			word = get_string_num(word_word)
			words.append(word)
	words.sort()
	return words

def get_tags_by_word(word):
	key = 'final_tag_word_%s'%word
	# returns list of tags ['tag_NP', 'tag_V', etc]
	tag_list = get_list(key)
	tags = []
	for tag_item in tag_list:
		tag = get_string_num(tag_item)
		tags.append(tag)
	tags.sort()
	return tags
	
def get_words_by_tag(tag):
	key = 'tagged_words_tag_%s'%tag
	# returns list of words ['word_gvold', 'word_blah', etc]
	word_list = get_list(key)
	words = []
	for word_item in word_list:
		word = get_string_num(word_item)
		words.append(word)
	words.sort()
	return words

#### Game Functions ####

def get_words_tweets_game():
	# get sentences and tags assoc - done
	# get random word from 'words', then get 'word'
	# also get tweets associated with that word
	# choose random tweet to return
	# also return tweet list, just in case

	# returns list of words ['word_glvod', 'word_cruls', etc]
	words = get_list('words')
	word_list = []
	for word_word in words:
		# returns '(word)'
		word = get_string_num(word_word)
		# word_list will look like ['word', 'diff word', etc]
		word_list.append(word)

	random_num = random.randint(0, (len(word_list)-1))
	word_for_game = word_list[random_num]

	word_word_tweets = 'word_%s_tweets'%word_for_game

	tweet_list = get_list(word_word_tweets)
	random_num_again = random.randint(0, len(tweet_list)-1)
	tweet_for_game = tweet_list[random_num_again]

	return word_for_game, tweet_for_game, tweet_list

def get_pos_sentences():
	sentences = get_list('sentences')
	list_of_sents = []
	for sent_pos_tag in sentences:
		tag_and_sentences = get_list(sent_pos_tag)
		list_of_sents.append(tag_and_sentences)

	# list_of_sents looks like [['tag_(POS)', "sent 1", "sent2"], ['tag_(diff POS)', 'sent1', 'sent2']]
	return list_of_sents

def break_pos_sents(list_of_sents):
	pos_sentences = []
	for pos in range(len(list_of_sents)):
		random_index = random.randint(1, len(list_of_sents[pos][1:])-1)
		sentence = list_of_sents[pos][random_index]
		tag = list_of_sents[pos][0]
		pos_sentences.append((tag, sentence))
	return pos_sentences


def get_another_tweet(word, tweet):
	# word and tweet must string
	word_word_tweets = 'word_%s_tweets'%word
	tweet_list = get_list(word_word_tweets)
	return tweet_list


def tag_word_game(word, pos, user, tweet):
	# pos comes in as tag_(POS)
	# tags a word from the game with tag_POS

	# user_(name)_tag_word_(word)
	add_user_tag_word(user, word, pos)

	# tag_word_(word)_tag_(POS)
	add_tag_word_tag_pos(word, pos, user)

	# tweet_tag_word_(word)_tag_(POS)
	add_tweet_tag_word_tag_pos(word, pos, [tweet])

	# user_(name)_words_tagged
	tag_word_tag_pos = 'tag_word_%s_%s'%(word, pos)
	add_user_words_tagged(user, [tag_word_tag_pos])


def add_pts_game(word, pos, user):
	# word, pos, and user must be strings
	# adds 10 pts to every user once tag verified 5x
	# adds 5 pts to every new user who continues to verify tag thereafter
	# also adds words to their final tags if verified

	if pos != 'U':
		tag_word_word_tag_pos = "tag_word_%s_tag_%s"%(word, pos)
		users_tagged_as_pos = get_list(tag_word_word_tag_pos)
		if len(users_tagged_as_pos) == 5:
			# give each user 10 pts
			for user_name in users_tagged_as_pos:
				user_name_pts = "user_%s_pts"%user_name
				add_user_pts(user_name_pts, 10)
			word_word = "word_%s"%word
			word_list = [word_word]
			tag_tag = "tag_%s"%pos
			tag_list = [tag_tag]
			add_tagged_words_pos(pos, word_list)
			add_final_tag(word, tag_list)

		elif len(users_tagged_as_pos) > 5:
			# give each user 5 pts
			for user_name in users_tagged_as_pos:
				user_name_pts = "user_%s_pts"%user_name
				add_user_pts(user_name_pts, 5)
	else:
		# don't give them any points if not verified yet
		pass
	

def get_top_scores():
	# gets the top 25 scores, in order (highest to lowest)

	points_list = get_list('points')
	top_list = []

	if len(points_list) > 25:
		# create the first 25 points to compare all other points to
		for user_name_pts in points_list[:25]:
			their_pts = int(get_string_num(user_name_pts))
			user_name = user_name_pts.rstrip('pts').lstrip('user').rstrip('_').lstrip('_')
			top_list.append((their_pts, user_name))
			
		top_list.sort()
		top_list.reverse()
		# looking at the sorted list from highest to lowest
		for user_name_pts in points_list[25:]:
			their_pts = int(get_string_num(user_name_pts))
			num_times_added = 0
			for scores in top_list:
				if their_pts > scores[0] and num_times_added == 0:
					user_name = user_name_pts.rstrip('pts').lstrip('user').rstrip('_').lstrip('_')
					if user_name != scores[1]:
						top_list.append((their_pts, user_name))
						num_times_added += 1
						
		top_list.sort()
		top_list.reverse()

		if len(top_list) > 25:
			top_list = top_list[:25]
			return top_list
		else:
			return top_list
	else:
		# if the len(points_list) <= 25
		for user_name_pts in points_list:
			their_pts = int(get_string_num(user_name_pts))
			user_name = user_name_pts.rstrip('pts').lstrip('user').rstrip('_').lstrip('_')
			top_list.append((their_pts, user_name))
		top_list.sort()
		top_list.reverse()
		return top_list


#### End Game Functions ####

#### URL Functions ####

def keep_url(session_url, ip_address):
	# save the url with ip_address as the key
	r_server.set(ip_address, session_url)
	

def get_last_url(ip_address):
	# use ip_address as the key to get the last url, then del the key
	last_url = r_server.get(ip_address)
	r_server.delete(ip_address)
	return last_url

#### End URL Functions #####

#### End Flask Uses ####





def main():
    pass

if __name__ == "__main__":
    main()