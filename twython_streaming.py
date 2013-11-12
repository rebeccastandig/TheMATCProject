from twython import TwythonStreamer
from celery_tasks import parse_tweets


class Streamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            tweet = data['text'].encode('utf-8').split('\n')
            parse_tweets.delay(tweet)
        # this returns each tweet as a list

    def on_error(self, status_code, data):
        print status_code
	

def main():
	pass

if __name__ == "__main__":
    main()