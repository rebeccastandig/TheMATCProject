#Welcome to [The Manually Annotated Twitter Corpus Project](http://www.thematcproject.org)
###The Manually Annotated Twitter Corpus Project (a.k.a. The MATC Project) is a crowdsourced part of speech tagging game that results in a corpus of words sourced from Twitter. 

The whole idea behind [The MATC Project](http://www.thematcproject.org) is to allow linguistic data to be annotated by people with little or no training in linguistics.

There's two parts to The MATC Project: Tres Tigres, and The TwitUrban Dictionary.

##General Information
####[Tres Tigres](http://www.thematcproject.org/game) is the crowdsourcing game that manually annotates the linguistic data.

Tres Tigres collects all tweets in English from the sample Public stream via Twitter's streaming API. Tres Tigres then checks each word in a tweet against the Wordnik corpus (which pulls from The American Heritage Dictionary, WordNet, Wiktionary, and a variety of other sources). 

If a word isn't in the Wordnik corpus (and isn't a user name, emoticon, et cetera), it gets tagged with a part of speech by users in Tres Tigres.

Once a word has been tagged with a part of speech through Tres Tigres, it goes into The TwitUrban Dictionary.

####[The TwitUrban Dictionary](http://www.thematcproject.org/corpus) is the manually annotated corpus of the words pulled from Twitter. 

It is constantly updating, and it is available for download free of charge. You can also browse it online.

##Technical Information
####The MATC Project is a web application that uses Redis, Python, Twitter's Streaming API, Wordnik's API, Celery, Flask, Jinja, JavaScript, and the D3 JavaScript library.

###Pull Tweets
#####[celery_client.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/celery_client.py), [twython_streaming.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/twython_streaming.py)

First, Celery (a queueing system for Python) pulls English tweets from the Public Twitter stream via Twitter's Streaming API. To access the Twitter Streaming API, I used the Twython module for Python. 

###Clean Tweets 
#####[celery_tasks.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/celery_tasks.py), [tweet_cleaner.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/tweet_cleaner.py)

Each tweet is added the Redis ToGo database. These tweets are then sent via Celery to tweet_cleaner.py, which checks each word in a tweet against a variety of criteria. 

If a word is a user name, emoticon, number, meta word (such as 'RT'), non-word (such as 'haha'), url, or contains non-English letters, it is ignored.

###Check Words Against A Dictionary
#####[celery_tasks.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/celery_tasks.py), [wordnik_api.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/wordnik_api.py)

The words that make it through tweet_cleaner.py are then sent to wordnik_api.py. There, each word in a tweet is checked against the Wordnik corpus (which pulls from The American Heritage Dictionary, WordNet, Wiktionary, and a variety of other sources).

###Put Words & Tweets In The Database
#####[celery_tasks.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/celery_tasks.py), [model.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/model.py)

Using model.py, any words that are not found in Wordnik are added to the Redis Cloud database, along with the tweet they were found in. 

###Tagging Words
#####[app.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/app.py), [model.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/model.py)

The front end of The MATC Project was created using Flask (a web framework for Python) and Jinja (to communicate between Python and HTML/JavaScript).

Once a user has registered with The MATC Project through Flask, they can play Tres Tigres (the part of speech tagging game). Users are shown a random word and a tweet associated with the word. 

They are also shown an assortment of sentences with different parts of speech removed. They are asked to click on the sentence that the word fits into. Based on which sentence they click, it is tagged with a different part of speech. (JavaScript is used in order to retrieve which sentence they have clicked.)

Each word must be tagged at least 5 times with a specific part of speech before it is given a final part of speech tag in the Redis Cloud database. In addition to saving the word and the part of speech tag, the tweet the word came from is saved and corresponds to the part of speech it was tagged with.

###Adding Words To The Corpus
#####[app.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/app.py), [model.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/model.py)

Once a word is given a final part of speech tag, it is added to The TwitUrban Dictionary (the corpus). The TwitUrban Dictionary is accessed online (or via downloading it). All of the tags and words are stored in the Redis Cloud database.

###Visualizing The Tagged Words
#####[app.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/app.py), [model.py](https://github.com/rebeccastandig/TheMATCProject/blob/master/model.py)

You can also access visualizations of The TwitUrban Dictionary online. Using the D3 JavaScript library, words tagged as a certain part of speech are shown in word bubbles. The size of each word bubble is dependent upon how many tweets the word was tagged as that part of speech in.

##[Click here to go to The MATC Project](http://www.thematcproject.org)

