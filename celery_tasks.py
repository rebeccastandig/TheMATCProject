from celery import Celery
from wordnik import *
import model
import wordnik_api
import tweet_cleaner

celery = Celery('twython_streaming', backend='redis://localhost:6379/1',  broker='redis://localhost:6379/0')

@celery.task
def parse_tweets(tweet):
	if len(tweet) > 0:
		keep_tweet = tweet
		tweet = tweet[0].split(' ')
		cleaned_tweet = tweet_cleaner.clean_tweet(tweet)
		length = 0
		words = []
		meta = ['RT', 'RTs', 'RT\'s', 'R/T', 'rt', 'rt\'s', 'rts', 'r/t', 'HT', 'H/T','ht', 'h/t', 'MT', 'M/T', 'mt', 'm/t', 'CR', 'C/R', 'cr', 'c/r']
		non_words = ['jeje', 'haha', 'mwah', 'bwah', 'muah', 'buah', 'http', 'teeh', 'jeej']
		beg_num= ['@', '$', '#', ':', ';', '>', '^','0','1','2','3','4','5','6','7','8','9']
		while length < len(cleaned_tweet)-1:
			for word in cleaned_tweet:
				# stripping word twice to account for people's weird punctuation errors
				word = tweet_cleaner.strip_word(word)
				word = tweet_cleaner.strip_word(word)
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
					elif ':-D' in word:
						# do this for 0.0 o.o O.O -_- :-P :-) ;-P ;-) etc too
						word = 0
						length += 1
					elif len(word) > 0:
						if word[-1] == 's' and word[-2] == '\'':
							word = 0
							length += 1
						if word != 0:
							for letter in word:
								if ord(letter) > 128:
									word = 0
									length += 1
					elif len(word) > 1:
						if word[1] in beg_num:
							word = 0
							length += 1
					length += 1
					words.append(word)
	words_in_game = []
	if len(words) > 0:
		for word in words:
			if word > 0:
				# check Wordnik
				results = wordnik_api.check_all(word)
				if results != None:
					# if Wordnik never returned a result > 0, put it into the game
					words_in_game.append(word)
		if len(words_in_game) > 0:
			model.set_game_words_tweets(words_in_game, keep_tweet)