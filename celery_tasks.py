from celery import Celery
from wordnik import *

# these are the API keys for Wordnik
apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'secret'
client = swagger.ApiClient(apiKey, apiUrl)


celery = Celery('twython_streaming', backend='redis://localhost:6379/1',  broker='redis://localhost:6379/0')

@celery.task
def parse_tweets(tweet):
	if len(tweet) > 0:
		keep_tweet = tweet
		tweet = tweet[0].split(' ')
		length = 0
		words = []
		meta = ['RT', 'RTs', 'RT\'s', 'R/T', 'rt', 'rt\'s', 'rts', 'r/t', 'HT', 'H/T','ht', 'h/t', 'MT', 'M/T', 'mt', 'm/t']
		non_words = ['jeje', 'haha', 'mwah', 'bwah', 'muah', 'buah', 'http', 'teeh', 'jeej']
		beg_num= ['@', '$', '#', ':', ';', '>', '^','0','1','2','3','4','5','6','7','8','9']
		while length < len(tweet)-1:
			for word in tweet:
				word = word.rstrip(',\"\'!.?-:<;~`-_=+[]{}()')
				word = word.lstrip(',\"\'!.?-:<;~`-_=+[]{}()')
				if len(word) > 0:
					if word[0] in beg_num:
						word = 0
						length += 1
					elif word[1] in beg_num:
						word = 0
						length += 1
					elif word in meta:
						word = 0
						length += 1
					elif word[:4] in non_words:
						word = 0
						length += 1
					elif len(word) < 2:
						word = 0
						length += 1
					elif '&' in word:
						word = 0
						length += 1
					elif len(word) > 0:
						for letter in word:
							if ord(letter) > 128:
								word = 0
								length += 1
					length += 1
					words.append(word)
	wordApi = WordsApi.WordsApi(client)
	words_in_game = []
	for word in words:
		if word > 0:
			# checks the word, unadulterated
			in_dict = wordApi.searchWords(word)
			results = in_dict.totalResults
			# results == 0 if not in wordnik
			if results < 1:
				# checks the capitalized version of the word ('Monday' vs 'monday'). Also accounts for words that were all caps.
				lower_all_word = word.lower()
				upper_word = lower_all_word[0].upper() + lower_all_word[1:]
				in_dict = wordApi.searchWords(upper_word)
				results = in_dict.totalResults
				if results < 1:
					# checks words like asap, even if written in all caps
					lower_all_word = word.lower()
					in_dict = wordApi.searchWords(lower_all_word)
					results = in_dict.totalResults
					if results < 1:
						# checks words like iPad, even if written IPAD.
						lowered = word[0].lower() + word[1].upper() + word[2:].lower()
						in_dict = wordApi.searchWords(lowered)
						results = in_dict.totalResults
						if results < 1:
							# checks acronyms in all caps (changes aids to AIDS)
							all_caps = word.upper()
							in_dict = wordApi.searchWords(all_caps)
							results = in_dict.totalResults
							if results < 1:
								# if Wordnik never returned a result > 0, put it into the game
								words_in_game.append(word)
	print "game words: ", words_in_game, "\n tweet: ", keep_tweet
