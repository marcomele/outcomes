try:
	import json
except ImportError:
	import simplejson as json
import ast
import re
from pprint import pprint
from threading import Thread, Lock

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

category = "society"
subcategory = "issues"

with open("data/" + category + "-" + subcategory + "/output") as sampleOutput:
	for line in sampleOutput:
		for literal in getOneTweet(line):
			print literal[:20] + literal[-20:]
			try:
				tweet = ast.literal_eval(literal)
				#print tweet["text"]
			except SyntaxError:
				print "bad formatted file --- all dictionaries must be newline separatad"
			break
