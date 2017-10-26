try:
	import json
except ImportError:
	import simplejson as json
import ast
import re
from pprint import pprint
import sys
import time
from dateutil.parser import parse
from dateutil.tz import *
from datetime import *
import os

def printKey(dictionary, key, depth = 0):
	print "\t" * depth + key
	if isinstance(dictionary[key], dict):
		for subkey in dictionary[key]:
			printKey(dictionary[key], subkey, depth + 1)

def process(tweet):
	tweet["created_at"] = str(parse(tweet["created_at"]).astimezone(tzutc()))
	del tweet["entities"]
	return tweet

try:
	category = sys.argv[1]
	subcategory = sys.argv[2]
except IndexError:
	print "arguments missing"
	exit()
nusers = 0
ntweets = 0
users = {}
directory = "data/" + category + "-" + subcategory
print "reading file..."
with open(directory + "/formatted", "r") as tweets:
	for line in tweets:
		tweet = ast.literal_eval(line)
		tweet = process(tweet)
		ntweets += 1
		user = tweet["user"]
		if not user in users:
			users[user] = []
			nusers += 1
		users[user].append(tweet)
		sys.stderr.write("users: " + str(nusers) + "\ttweets:" + str(ntweets) + "\r")
sys.stderr.write("\nsaving timelines...\n")
ntimelines = 0
for user in users:
	timeline = sorted(users[user], key = lambda t : t["created_at"])
	#del users[user] ----- can't change size during iteration ----
	ntimelines += 1
	with open(directory + "/" + str(user), "w") as userfile:
		for tweet in timeline:
			userfile.write(json.dumps(tweet))
			userfile.write("\n")
	sys.stderr.write("[timeline] " + str(ntimelines) + "/" + str(nusers) + ", [" + str(round(100 * float(ntimelines) / float(nusers),2)) + "%]                        \r")
sys.stderr.write("\nDone.\n")
