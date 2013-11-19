#!/usr/bin/python
# -*- coding: <utf-8> -*-

import twython_streaming
from celery_tasks import parse_tweets

# These are the API keys for Twitter
APP_KEY = 'secret'
APP_SECRET = 'secret'

OAUTH_TOKEN = 'secret'
OAUTH_TOKEN_SECRET = 'secret'


stream = twython_streaming.Streamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

tweet = stream.statuses.filter(track='twitter', language='en')

result = parse_tweets(tweet)

result.get()