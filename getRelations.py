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
import sys

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

	category = "society"
	subcat = "issues"
	idfile = "data/" + category + "-" + subcat + "/uids"
	users = {}
	count = 0
	with open(idfile, "r") as uids:
		for uid in uids:
			uid = uid.split("\n")[0]
			users[uid] = count
			count += 1
	relations = [[0 for x in range(count)] for x in range(count)]
	print relations
	for user in users:
		following, followers = api.friends_ids(id=user), api.followers_ids(id=user)
		print following
		print followers
		break
	exit(0)
	try:

		print result
	except tweepy.TweepError as e:
		print e

		# except tweepy.RateLimitError as r:
		#	print "rate limit reached, waiting..."
		#	time.sleep(60)
		#		except tweepy.TweepError as e:
		#			print e
		#			break
