import twython_streaming
from celery_tasks import parse_tweets

APP_KEY = 'secret'
APP_SECRET = 'secret'

OAUTH_TOKEN = 'secret'
OAUTH_TOKEN_SECRET = 'secret'

stream = twython_streaming.Streamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

tweet = stream.statuses.filter(track='twitter', language='en')

result = parse_tweets(tweet)

print result.get()