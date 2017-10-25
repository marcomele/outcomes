try:
	import json
except ImportError:
	import simplejson as json
from twitter import *
import time
try:
	from urllib.parse import parse_qs
except ImportError:
	from urlparse import parse_qs
import tweepy

def getcredentials():
	credentials = {
		"ACCESS_TOKEN" : None,
		"ACCESS_SECRET" : None,
		"CONSUMER_KEY" : None,
		"CONSUMER_SECRET" : None
	}
	for key in credentials:
		f = open(key + ".key", "r")
		credentials[key] = f.readline()[0:-1]
	return credentials

def authenticate(credentials):
	return OAuth1(credentials["ACCESS_TOKEN"],
		credentials["ACCESS_SECRET"],
		credentials["CONSUMER_KEY"],
		credentials["CONSUMER_SECRET"])

if __name__ == '__main__':
	# create authentication object
	credentials = getcredentials()
	auth = tweepy.OAuthHandler(credentials["CONSUMER_KEY"], credentials["CONSUMER_SECRET"])
	auth.set_access_token(credentials["ACCESS_TOKEN"], credentials["ACCESS_SECRET"])

	api = tweepy.API(auth)

	category = "health"
	subcat = "pharmacy"
	filename = "mergedData/" + category + "-" + subcat + "_ids.txt"
	with open(filename, "r") as inputFile:
		for tweetID in inputFile:
			while True:
				try:
					status = api.get_status(tweetID)
					with open("output", "a") as outputFile:
						outputFile.write(str(json.loads(json.dumps(status._json))))
					print tweetID
					break
				except tweepy.RateLimitError as r:
					print "rate limit reached, waiting..."
					time.sleep(60)
				except tweepy.TweepError as e:
					print e
					break
