def clean_tweet(tweet_after_split):
	return split_commas(split_sgl_qt(split_dbl_qt(split_ques(split_excl(split_periods(tweet_after_split))))))


def split_periods(tweet_after_split):
	new_tweet = []
	for word in tweet_after_split:
		split_words = word.split('..')
		for word in split_words:
			if word == '':
				pass
			else:
				new_tweet.append(word)
	return new_tweet

def split_excl(split_tweet):
	new_tweet = []
	for word in split_tweet:
		split_words = word.split('!!')
		for word in split_words:
			if word == '':
				pass
			else:
				new_tweet.append(word)
	return new_tweet

def split_ques(split_tweet):
	new_tweet = []
	for word in split_tweet:
		split_words = word.split('??')
		for word in split_words:
			if word == '':
				pass
			else:
				new_tweet.append(word)
	return new_tweet

def split_dbl_qt(split_tweet):
	new_tweet = []
	for word in split_tweet:
		split_words = word.split('\"')
		for word in split_words:
			if word == '':
				pass
			else:
				new_tweet.append(word)
	return new_tweet

def split_sgl_qt(split_tweet):
	new_tweet = []
	for word in split_tweet:
		split_words = word.split('\'')
		for word in split_words:
			if word == '':
				pass
			else:
				new_tweet.append(word)
	return new_tweet

def split_commas(split_tweet):
	new_tweet = []
	for word in split_tweet:
		split_words = word.split(',,')
		for word in split_words:
			if word == '':
				pass
			else:
				new_tweet.append(word)
	return new_tweet

def strip_word(word):
	word = word.rstrip(',\"\'!.?-:<;~`-_=+[]{}()')
	word = word.lstrip(',\"\'!.?-:<;~`-_=+[]{}()')
	return word





