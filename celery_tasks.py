#!/usr/bin/python
# -*- coding: <utf-8> -*-

from celery import Celery
import model
import wordnik_api
import tweet_cleaner

celery = Celery('twython_streaming', backend=os.environ.get('REDISTOGO_URL'),  broker=os.environ.get('REDISTOGO_URL')

@celery.task
def parse_tweets(tweet):
	if len(tweet) > 0:
		keep_tweet = tweet
		tweet = tweet[0].split()
		cleaned_tweet = tweet_cleaner.clean_tweet(tweet)
		words = []
		final_words = []
		for word in cleaned_tweet:
			if len(word) > 2:
				checking_words = tweet_cleaner.check_words(word)
				if checking_words != 0:
					words.append(checking_words)
		for word in words:
			# stripping word twice to account for people's weird punctuation errors
			word = tweet_cleaner.strip_word(word)
			word = tweet_cleaner.strip_word(word)
			if len(word) > 2:
				checking_words = tweet_cleaner.check_words(word)
				if checking_words != 0:
					final_words.append(checking_words)
	words_in_game = []
	if len(final_words) > 0:
		for word in final_words:
			if word > 0:
		 		# check Wordnik
				results = wordnik_api.check_all(word)
				if results != None:
					# if Wordnik never returned a result > 0, put it into the game
					words_in_game.append(word)
		if len(words_in_game) > 0:
			model.set_game_words_tweets(words_in_game, keep_tweet)