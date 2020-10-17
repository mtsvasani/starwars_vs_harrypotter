import tweepy
from tweepy import OAuthHandler
import re
import sw_or_hp
import random
import time

COMMON_REPLIES = ['I think ', 'This may refer to ', 'My training says ', 'I may be wrong but ', 'Let me guess ',
'May be ', '', "I'll say "]

ckey = #consumer key
csecret = #consumer secret
atoken = #access token
asecret = #access secret


 # first id 1269473584130461696

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
my_api = tweepy.API(auth, wait_on_rate_limit=True)

file_name = 'last_seen_id.txt'

# the file last_seen_id.txt saves the id of the last seen tweet and gets updated everytime a tweet is read

def retrive_last_seen_id(file_name):
	f = open(file_name, 'r')
	last_seen_id = int(f.read().strip())
	f.close()
	return  last_seen_id

def store_last_seen_id(last_seen_id, file_name):
	f = open(file_name, 'w')
	f.write(str(last_seen_id))
	f.close()
	return

def reply_to_tweets():

	last_seen_id = retrive_last_seen_id(file_name)

	mentions = my_api.mentions_timeline(last_seen_id, tweet_mode='extended')

	for mention in reversed(mentions):
		print(str(mention.id) + ' - ' + mention.full_text)
		last_seen_id = mention.id
		store_last_seen_id(last_seen_id, file_name)
		if '#guess_this' in mention.full_text.lower():
			tweet = mention.full_text.lower()
			tweet = tweet.replace('@guessing_kid', '').replace('#guess_this', '')
			tweet = re.sub(r'[^A-Za-z]', ' ', tweet)
			reply_to = mention.author.screen_name
			prediction = sw_or_hp.guess_movie(tweet)
			my_api.update_status(f'@{reply_to} ' + random.choice(COMMON_REPLIES) + prediction.title() , mention.id)
			print('tweet_sent')

while True:
	try:
		reply_to_tweets()
	except Exception as e:
		print(str(e))
	time.sleep(5)