import twython_streaming
from celery_tasks import parse_tweets
import os

# These are the API keys for Twitter
APP_KEY = os.environ.get('twitter_APP_KEY')
APP_SECRET = os.environ.get('twitter_APP_SECRET')

OAUTH_TOKEN = os.environ.get('twitter_OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.environ.get('twitter_OAUTH_TOKEN_SECRET')


stream = twython_streaming.Streamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

tweet = stream.statuses.filter(track='twitter', language='en')

result = parse_tweets(tweet)

result.get()