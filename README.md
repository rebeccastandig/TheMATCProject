#Welcome to The Manually Annotated Twitter Corpus Project
###The Manually Annotated Twitter Corpus Project (a.k.a. The MATC Project) is a crowdsourced part of speech tagging game that results in a corpus of words sourced from Twitter. 

The whole idea behind The MATC Project is to allow linguistic data to be annotated by people with little or no training in linguistics.

There's two parts to The MATC Project: Tres Tigres, and The TwitUrban Dictionary.

[www.thematcproject.org | Click here]


##General Information
####Tres Tigres is the crowdsourcing game that manually annotates the linguistic data.

Tres Tigres collects all tweets in English from the sample Public stream via Twitter's streaming API (accessed using the Twython module in Python). Tres Tigres then checks each word in a tweet against the Wordnik corpus (which pulls from The American Heritage Dictionary, WordNet, Wiktionary, and a variety of other sources). 

If a word isn't in the Wordnik corpus (and isn't a user name, emoticon, et cetera), it gets tagged with a part of speech by users in Tres Tigres.

Once a word has been tagged with a part of speech through Tres Tigres, it goes into The TwitUrban Dictionary.

####The TwitUrban Dictionary is the manually annotated corpus of the words pulled from Twitter. 

It is constantly updating, and it is available for download free of charge. You can also browse it online.


