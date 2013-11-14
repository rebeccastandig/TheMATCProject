import redis
import hashlib

r_server = redis.StrictRedis(host="localhost", port=6379, db=1)

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

def set_sent_pos_tag(sentence, pos):
	# sets sent_(POS)_tag
	# sentence & pos must be strings
	sent_pos_tag = 'sent_%s_tag'%pos
	tag_pos = 'tag_%s'%pos
	r_server.rpush(sent_pos_tag, sentence)
	r_server.rpush(sent_pos_tag, tag_pos)

def set_user(user):
	# sets user_(name)
	# user must be string
	user_name = 'user_%s'%user
	user_name_pw = 'user_%s_pw'%user
	user_name_pts = 'user_%s_pts'%user
	r_server.rpush(user_name, user)
	r_server.rpush(user_name, user_name_pw)
	r_server.rpush(user_name, user_name_pts)

def set_user_pw(user, pw):
	# sets user_(name)_pw
	# user & pw must be strings
	user_name_pw = 'user_%s_pw'%user
	password = md5_hash(pw)
	r_server.set(user_name_pw, password)


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
		else:
			r_server.rpush(word_word_tweets, tweet)

def add_user_pts(user, pts):
	# sets & adds user_(name)_pts
	# user must be string
	# pts must be number, can be negative to decrease
	user_name_pts = 'user_%s_pts'%user
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
	add_all_words(word_list)
	for word in word_list:
		set_word(word)
		add_word_tweets(word, tweet)
	print "success"

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
	password = get_string_num(user_info[1])
	authenticated = False
	if user_name == user_info[0]:
		if md5_hash(pw) == password:
			authenticated = True
	return authenticated


def main():
    pass

if __name__ == "__main__":
    main()