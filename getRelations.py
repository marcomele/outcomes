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

def showProgress(progress, count, limit = False):
	sys.stderr.write("\r[[" + str(round(float(progress) / count, 2)) + "%] [")
	for i in xrange(10):
		if i < progress / count:
			sys.stderr.write("==")
		else:
			sys.stderr.write("  ")
	sys.stderr.write("] [RARE LIMIT EXCEEDED] " if limit else "]                     ")

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
	errors = ""
	with open(idfile, "r") as uids:
		for uid in uids:
			uid = uid.split("\n")[0]
			users[uid] = []
			count += 1
	progress = 0
	unirel = 0
	outing = "data/" + category + "-" + subcat + "/followings"
	print "saving followings in " + outing
	outer = "data/" + category + "-" + subcat + "/followers"
	print "saving followers in " + outer
	with open(outing, "w") as outfollowing:
		with open(outer, "w") as outfollowers:
			for user in users:
				while True:
					try:
						followings, followers = api.friends_ids(id=user), api.followers_ids(id=user)
						outfollowing.write(user + "\t" + ",".join(followings) + "\n")
						outfollowers.write(user + "\t" + ",".join(followers) + "\n")
						showProgress(progress, count)
						break
					except tweepy.RateLimitError as r:
						showProgress(progress, count, True)
						time.sleep(15 * 60)
					except tweepy.TweepError as e:
						errors += str(e) + "\n"
				progress += 1
	print "\r[100%] [COMPLETED]                                 "
	print "\n" + errors
	exit(0)
