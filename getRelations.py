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
import os

def getcredentials():
	credentials = {
		"ACCESS_TOKEN" : None,
		"ACCESS_SECRET" : None,
		"CONSUMER_KEY" : None,
		"CONSUMER_SECRET" : None
	}
	for key in credentials:
		f = open(key + ".key", "r")
		credentials[key] = f.readline().split("\n")[0]
	return credentials

def authenticate(credentials):
	return OAuth1(credentials["ACCESS_TOKEN"],
		credentials["ACCESS_SECRET"],
		credentials["CONSUMER_KEY"],
		credentials["CONSUMER_SECRET"])

def showProgress(progress, count, limit = False, error = ""):
	sys.stderr.write("\r[%03d/%d]" % (progress, count))
	if limit:
		sys.stderr.write(" rate limit exceeded, waiting...")
	elif error:
		sys.stderr.write(" [ERROR] " + error + "\n")
	else:
		sys.stderr.write(" fetched                         \n")

if __name__ == '__main__':
	# create authentication object
	credentials = getcredentials()
	auth = tweepy.OAuthHandler(credentials["CONSUMER_KEY"], credentials["CONSUMER_SECRET"])
	auth.set_access_token(credentials["ACCESS_TOKEN"], credentials["ACCESS_SECRET"])

	api = tweepy.API(auth, wait_on_rate_limit = True)

	category = "society"
	subcat = "issues"
	idfile = "data/" + category + "-" + subcat + "/uids"
	users = []
	count = 0
	errors = ""
	with open(idfile, "r") as uids:
		for uid in uids:
			user = uid.split("\n")[0]
			if user:
				users.append(user)
				count += 1
	progress = 0
	outing = "data/" + category + "-" + subcat + "/followings"
	print "saving followings in " + outing
	outer = "data/" + category + "-" + subcat + "/followers"
	print "saving followers in " + outer
	with open(outing, "w") as outfollowing:
		with open(outer, "w") as outfollowers:
			for user in users:
				try:
					followings, followers = api.friends_ids(id=user), api.followers_ids(id=user)
					outfollowing.write(user + "\t" + ",".join(list(str(following) for following in followings)) + "\n")
					outfollowers.write(user + "\t" + ",".join(list(str(follower) for follower in followers)) + "\n")
					showProgress(progress, count)
				except tweepy.TweepError as e:
					errors = str(e)
					showProgress(progress, count, error = errors)
				progress += 1
	print "\n[COMPLETED]"
	os.system("notify-send getRelations.py Task\ completed")
	exit(0)
