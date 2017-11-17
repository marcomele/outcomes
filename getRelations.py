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
	errors = ""
	with open(idfile, "r") as uids:
		for uid in uids:
			uid = uid.split("\n")[0]
			users[uid] = []
			count += 1
	progress = 0
	unirel = 0
	for user in users:
		while True:
			try:
				followings, followers = str(api.friends_ids(id=user)), str(api.followers_ids(id=user))
				for following in followings:
					try:
						if following in users:
							users[user].append(following)
							unirel += 1
					except KeyError:
						continue
				for follower in followers:
					try:
						users[follower].append(user)
						unirel += 1
					except KeyError:
						continue
				sys.stderr.write("\r[[" + str(round(progress / count, 2)) + "%] [")
				for i in xrange(10):
					if i < progress / count:
						sys.stderr.write("==")
					else:
						sys.stderr.write("  ")
				sys.stderr.write("]           ")
				break
			except tweepy.RateLimitError as r:
				sys.stderr.write("\r[" + str(round(progress / count, 2)) + "%] [RATE LIMIT EXCEEDED --- WAITING]            ")
				time.sleep(60)
			except tweepy.TweepError as e:
				errors += e + "\n"
		progress += 1
	print "\r[100%] [COMPLETED]                                 "
	print str(unirel) + " unidirectional relation" + ("s found" if unirel != 1 else " found")
	output = "data/" + category + "-" + subcat + "/relations"
	print "saving relations in " + output
	with open(output, "w") as out:
		for user in users:
			out.write(user + "\t" + ",".join(users[user]) + "\n")
	print "done."
	print "\n" + errors
	exit(0)
