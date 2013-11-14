def clean_tweet(tweet_after_split):
	return split_slashes(split_commas(split_sgl_qt(split_dbl_qt(split_ques(split_excl(split_periods(tweet_after_split)))))))


def split_periods(tweet_after_split):
	final_tweet = []
	new_tweet = []
	for word in tweet_after_split:
		split_words = word.split('..')
		for word in split_words:
			if word == '':
				pass
			else:
				new_tweet.append(word)
	for word in new_tweet:
		split_words = word.split('.')
		for word in split_words:
			if word == '':
				pass
			else:
				final_tweet.append(word)
	return final_tweet

def split_excl(split_tweet):
	new_tweet = []
	final_tweet = []
	for word in split_tweet:
		split_words = word.split('!!')
		for word in split_words:
			if word == '':
				pass
			else:
				new_tweet.append(word)
	for word in new_tweet:
		split_words = word.split('!')
		for word in split_words:
			if word == '':
				pass
			else:
				final_tweet.append(word)
	return final_tweet

def split_ques(split_tweet):
	new_tweet = []
	final_tweet = []
	for word in split_tweet:
		split_words = word.split('??')
		for word in split_words:
			if word == '':
				pass
			else:
				new_tweet.append(word)
	for word in new_tweet:
		split_words = word.split('?')
		for word in split_words:
			if word == '':
				pass
			else:
				final_tweet.append(word)
	return final_tweet

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
	final_tweet = []
	for word in split_tweet:
		split_words = word.split(',,')
		for word in split_words:
			if word == '':
				pass
			else:
				new_tweet.append(word)
	for word in new_tweet:
		split_words = word.split(',')
		for word in split_words:
			if word == '':
				pass
			else:
				final_tweet.append(word)
	return final_tweet

def split_slashes(split_tweet):
	final_tweet = []
	new_tweet = []
	for word in split_tweet:
		split_words = word.split('\\\\')
		for word in split_words:
			if word == '':
				pass
			else:
				new_tweet.append(word)
	for word in new_tweet:
		split_words = word.split('\\')
		for word in split_words:
			if word == '':
				pass
			else:
				final_tweet.append(word)
	return final_tweet

def strip_word(word):
	word = word.rstrip(',\"\'\\!.?-:<;~`-_=+[]{}()')
	word = word.lstrip(',\"\'\\!.?-:<;~`-_=+[]{}()')
	return word

def check_beg_nums(word):
	beg_num = ['@', '$', '#', ':', ';', '>', '&', '^','0','1','2','3','4','5','6','7','8','9']
	if word[0] in beg_num:
		word = 0
	if word != 0:
		for element in beg_num:
			if element in word:
				word = 0
				break
	return word

def check_meta(word):
	if word != 0:
		meta = ['RT', 'RTs', 'RT\'s', 'R/T', 'rt', 'rt\'s', 'rts', 'r/t', 'HT', 'H/T','ht', 'h/t', 'MT', 'M/T', 'mt', 'm/t', 'CR', 'C/R', 'cr', 'c/r']
		if word in meta:
			word = 0
		if word != 0:
			for element in meta:
				if element in word:
					word = 0
					break
	return word

def check_non_words(word):
	if word != 0:
		non_words = ['jeje', 'haha', 'mwah', 'bwah', 'muah', 'buah', 'http', 'teeh', 'jeej']
		if word[:4] in non_words:
			word = 0
		if word != 0:
			if len(word) > 4:
				for element in non_words:
					if element in word:
						word = 0
						break
	return word

def check_emoticons(word):
	if word != 0:
		emoticons = [':-D', ':-)', ':-(', ':-P', ';-D', ';-P', ':\'-(', ':\'(', '-_-', 'o.o', 'O.o', '0.o', 'O.O', '0.0', 'o.O', 'o.0']
		if word in emoticons:
			word = 0
		if len(word) > 3:
			for element in emoticons:
				if element in word:
					word = 0
					break
	return word

def check_possessives(word):
	if word != 0:
		if word[-1] == 's' and word[-2] == '\'':
			word = 0
		elif word[-1] == 's' and word[-2] == '\"':
			word = 0
	return word

def check_letters(word):
	if word != 0:
		for letter in word:
			if ord(letter) > 128:
				word = 0
				break
	return word

def check_mult_lett(word):
	if word != 0:
		length = 0
		while length < len(word)-2:
			# blahhh
			# blaaaah
			# bbbllah
			if word[length] == word[length+1] and word[length] == word[length+2]:
				word = 0
				break
			else:
				length += 1
	return word

def check_words(word):
	return check_mult_lett(check_letters(check_possessives(check_emoticons(check_non_words(check_meta(check_beg_nums(word)))))))


