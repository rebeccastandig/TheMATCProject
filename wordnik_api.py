from wordnik import *

# these are the API keys for Wordnik
apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'secret'
client = swagger.ApiClient(apiKey, apiUrl)

wordApi = WordsApi.WordsApi(client)

def get_results(word):
	in_dict = wordApi.searchWords(word)
	results = in_dict.totalResults
	return results

def check_normal(word):
	# checks the word, unadulterated
	results = get_results(word)
	if results == 0:
		return word
	else:
		return None

def check_cap(word):
	# checks the capitalized version of the word ('Monday' vs 'monday'). Also accounts for words that were all caps.
	if word != None:
		lower_word = word.lower()
		upper_first = lower_word[0].upper() + lower_word[1:]
		results = get_results(upper_first)
		if results == 0:
			return word
		else:
			return None

def check_lower(word):
	# checks words like asap, even if written in all caps
	if word != None:
		lower_word = word.lower()
		results = get_results(lower_word)
		if results == 0:
			return word
		else:
			return None
	
def check_acronym(word):
	# checks acronyms in all caps (changes aids to AIDS)
	if word != None:
		upper_word = word.upper()
		results = get_results(upper_word)
		if results == 0:
			return word
		else:
			return None

def check_iPad(word):
	# checks words like iPad, even if written IPAD.
	if word != None:
		lowered = word[0].lower() + word[1].upper() + word[2:].lower()
		results = get_results(lowered)
		if results == 0:
			return word
		else: 
			return None

def check_all(word):
	return check_iPad(check_acronym(check_lower(check_cap(check_normal(word)))))




