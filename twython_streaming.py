from twython import TwythonStreamer

APP_KEY = 'secret'
APP_SECRET = 'secret'

OAUTH_TOKEN = 'secret'
OAUTH_TOKEN_SECRET = 'secret'

class Streamer(TwythonStreamer):
    def on_success(self, data):
    	if 'text' in data:
	        status_text = data['text'].encode('utf-8')
	        
	    	if 'entities' in data:
		    	entities = data['entities']

		    	if 'hashtags' in entities:
		    		hashtags = entities['hashtags']
			    	hashtag_length = 0
			    	hashtag_text = []
			    	if len(hashtags) > 0:
				    	while hashtag_length <= len(hashtags)-1:
				    		text = hashtags[hashtag_length]['text']
				    		hashtag_length += 1
				    		hashtag_text.append(text)

				if 'urls' in entities:
					urls = entities['urls']
					url_length = 0
					url_text = []
					if len(urls) > 0:
						while url_length <= len(urls)-1:
							url = urls[url_length]['url']
							url_length += 1
							url_text.append(url)

				if 'user_mentions' in entities:mentions = entities['user_mentions']
			    	mention_length = 0
			    	mention_names = []
			    	if len(mentions) > 0:
			    		while mention_length <= len(mentions)-1:
			    			screen_name = mentions[mention_length]['screen_name']
			    			mention_length += 1
			    			mention_names.append(screen_name)
							
				if 'symbols' in entities:
					symbols = entities['symbols']
					symbol_length = 0
					symbol_text = []
			    	if len(symbols) > 0:
			    		while symbol_length <= len(symbols)-1:
			    			text = symbols[symbol_length]['text']
			    			symbol_length += 1
			    			symbol_text.append(text)

		    	if 'media' in entities:
		    		media = entities['media']
			    	media_length = 0
			    	media_url = []
			    	if len(media) > 0:
			    		while media_length <= len(media)-1:
			    			url = media[media_length]['url']
			    			media_length += 1
			    			media_url.append(url)
				# here is where i package it all together!
				tweet = [status_text, hashtag_text, url_text, mention_names, media_url, symbol_text]
				return tweet

    def tweets(self):
    	self.statuses.filter(track='twitter', language='en')

    def on_error(self, status_code, data):
        print status_code

stream = Streamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def get_tweets():
	stream.tweets()

def main():
	pass

if __name__ == "__main__":
    main()