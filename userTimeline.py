from __future__ import division
try:
	import json
except ImportError:
	import simplejson as json
from pprint import pprint
from dateutil.parser import parse
from dateutil.tz import *
from datetime import *
import os
import sys
import random

def err(str):
	sys.stderr.write(str)

def matchToken(words, timestamp):
	global token
	global timeline
	match = 1
	for token in tokens:
		for unigram in token.split("_"):
			match = 0
			for word in words:
				if word == unigram:
					match = 1
		timeline[token]["value"] += match
		if match:
			if not timeline[token]["first"]:
				timeline[token]["first"] = timeline[token]["last"] = timestamp
			else:
				timeline[token]["last"] = timestamp

def matchExperience(words, experience, timestamp):
	global timeline
	for token in experience:
		match = 1
		for unigram in token.split(" "):
			match = 0 if unigram not in words else match
		timeline["event"]["value"] += match
		if match and not timeline["event"]["timestamp"]:
			timeline["event"]["timestamp"] = timestamp

try:
	tokenfilename = sys.argv[1]
	folder = sys.argv[2]
except IndexError:
	err("missing argument\n")
	exit()

err("reading tokens... ")
with open(tokenfilename, "r") as tokenfile:
	tokens = [token[:-1] for token in tokenfile.readlines()]
err("done\n")

experience = ["belly fat", "tummy fat"]
timeline = {}
with open(folder + "/../firsts.csv", "w") as firsts:
	firsts.write("user")
	for token in tokens:
		firsts.write("," + token)
	firsts.write(",label\n")
	with open(folder + "/../lasts.csv", "w") as lasts:
		lasts.write("user")
		for token in tokens:
			lasts.write("," + token)
		lasts.write(",label\n")
		count = 0
		for filename in os.listdir(folder):
			for token in tokens:
				timeline[token] = {
				"value" : 0,
				"first" : None,
				"last": None
				}
				timeline["event"] = {
				"value" : 0,
				"timestamp" : None
				}
			timeline["user"] = filename
			with open(folder + "/" + filename, "r") as userfile:
				for line in userfile:
					tweet = json.loads(line)
					matchToken(tweet["text"], tweet["created_at"])
					matchExperience(tweet["text"], experience, tweet["created_at"])
					# break
			if not timeline["event"]["value"]:
				randomTime = 0
				atLeastOne = 0
				for token in tokens:
					if timeline[token]["value"]:
						atLeastOne = 1
						break
				while True and atLeastOne:
					x = random.randrange(0, len(tokens), 1)
					if timeline[tokens[x]]["value"]:
						randomTime = timeline[tokens[x]]["first"]
						break
			firsts.write(filename)
			for token in tokens:
				e = 1 if timeline[token]["value"] and (timeline[token]["first"] <= timeline["event"]["timestamp"] if timeline["event"]["value"] else randomTime) else 0
				firsts.write("," + str(e))
			firsts.write("," + (str(1) if timeline["event"]["value"] else str(0)) + "\n")
			lasts.write(filename)
			for token in tokens:
				e = 1 if timeline[token]["value"] and (timeline[token]["last"] >= timeline["event"]["timestamp"] if timeline["event"]["value"] else randomTime) else 0
				lasts.write("," + str(e))
			lasts.write("," + (str(1) if timeline["event"]["value"] else str(0)) + "\n")
			count += 1
			err("user " + str(count) + "\r")
err("\n")
