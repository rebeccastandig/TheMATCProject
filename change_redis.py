import os
import redis
import model

cloud = redis.from_url(os.environ.get('REDISCLOUD_URL'))
togo = redis.from_url(os.environ.get('REDISTOGO_URL'))

all_user_pts = togo.keys(pattern='user_*_pts')
all_user_pws = togo.keys(pattern='user_*_pw')
all_final_tags = togo.keys(pattern='final_*')
# need to just check for pw and pts
all_user_anything = togo.keys(pattern='user*')
all_sent = togo.keys(pattern='sent*')
all_tagged = togo.keys(pattern='tagged_*')
all_tweet = togo.keys(pattern='tweet*')
all_tag_word = togo.keys(pattern='tag_word*')

# tag pos just reset in cloud
# for word_word just use model

for key in all_user_pts:
	value = togo.get(key)
	if value:
		cloud.set(key, value)

for key in all_user_pws:
	value = togo.get(key)
	if value:
		cloud.set(key, value)

for key in all_final_tags:
	value = togo.lrange(key, 0, -1)
	if value:
		for item in value:
			cloud.rpush(key, item)

for key in all_user_anything:
	if key[-2:] == 'pw' or key[-3:] == 'pts':
		pass
	else:
		value = togo.lrange(key, 0, -1)
		if value:
			for item in value:
				cloud.rpush(key, item)

for key in all_sent:
	value = togo.lrange(key, 0, -1)
	if value:
		for item in value:
			cloud.rpush(key, 0, -1)

for key in all_tagged:
	value = togo.lrange(key, 0, -1)
	if value:
		for item in value:
			cloud.rpush(key, 0, -1)

for key in all_tweet:
	value = togo.lrange(key, 0, -1)
	if value:
		for item in value:
			cloud.rpush(key, 0, -1)

for key in all_tag_word:
	value = togo.lrange(key, 0, -1)
	if value:
		for item in value:
			cloud.rpush(key, 0, -1)

points = togo.lrange('points', 0, -1)
for item in points:
	cloud.rpush('points', item)

model.set_tag("N")
model.set_tag("O")
model.set_tag("P")
model.set_tag("M")
model.set_tag("PV")
model.set_tag("NV")
model.set_tag("Z")
model.set_tag("OP")
model.set_tag("J")
model.set_tag("A")
model.set_tag("S")
model.set_tag("I")
model.set_tag("D")
model.set_tag("V")
model.set_tag("C")
model.set_tag("E")
model.set_tag("PD")
model.set_tag("EV")
model.set_tag("SC")
model.set_tag("U")

words = togo.lrange('words', 0, -1)
for word_word in words:
	actual_word = word_word.lstrip('word_')
	cloud.set(word_word, actual_word)
	cloud.rpush('words', word_word)