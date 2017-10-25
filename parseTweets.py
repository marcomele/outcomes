try:
	import json
except ImportError:
	import simplejson as json
import ast
import re
from pprint import pprint
import sys
import shelve

def printKey(dictionary, key, depth = 0):
	print "\t" * depth + key
	if isinstance(dictionary[key], dict):
		for subkey in dictionary[key]:
			printKey(dictionary[key], subkey, depth + 1)

def getOneTweet(line):
	while True:
		try:
			[first, reminder] = line.split("}{", 1)
			yield first + "}"
			line = "{" + reminder
		except ValueError:
			yield line
			break
try:
	category = sys.argv[1]
	subcategory = sys.argv[2]
except IndexError:
	print "arguments missing"
	exit()
count = 0
with open("data/" + category + "-" + subcategory + "/formatted", "w") as formattedOutput:
	with open("data/" + category + "-" + subcategory + "/output", "r") as sampleOutput:
		for line in sampleOutput:
			for literal in getOneTweet(line):
				try:
					rawTweet = ast.literal_eval(literal)
					tweet = {
						"text" : rawTweet["text"],
						"id" : rawTweet["id"],
						"entities" : rawTweet["entities"],
						"user" : rawTweet["user"]["id"],
						"created_at" : rawTweet["created_at"]
						}
					formattedOutput.write(str(tweet) + "\n")
					count += 1
					sys.stderr.write("\rprogress: " + str(count))
				except SyntaxError:
					print "bad formatted file --- all dictionaries must be newline separatad"
