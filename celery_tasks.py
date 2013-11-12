from celery import Celery
from wordnik import *

apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'secret'

client = swagger.ApiClient(apiKey, apiUrl)


celery = Celery('twython_streaming', backend='redis://localhost:6379/1',  broker='redis://localhost:6379/0')

@celery.task
def parse_tweets(tweet):
	if len(tweet) > 0:
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
			in_dict = wordApi.searchWords(word)
			results = in_dict.totalResults
			# results == 0 if not in wordnik
			if results < 1:
				# this checks the capitalized version of the word in wordnik ('Monday' vs 'monday')
				lower_all_word = word.lower()
				upper_word = lower_all_word[0].upper() + lower_all_word[1:]
				in_dict = wordApi.searchWords(upper_word)
				results = in_dict.totalResults
				if results < 1:
					# this checks words like ipad
					lower_all_word = word.lower()
					in_dict = wordApi.searchWords(lower_all_word)
					results = in_dict.totalResults
					if results < 1:
						lower_first = word[0].lower() + word[1:]
						in_dict = wordApi.searchWords(lower_first)
						results = in_dict.totalResults
						if results < 1:
							words_in_game.append(word)
	print "game words: ", words_in_game
