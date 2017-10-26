from __future__ import division
try:
	import json
except ImportError:
	import simplejson as json
from pprint import pprint
from dateutil.parser import parse
from dateutil.tz import *
from datetime import *
import ast
import re
import sys
import time
import os
import nltk, re, pprint, string
from nltk import word_tokenize
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def printKey(dictionary, key, depth = 0):
	print "\t" * depth + key
	if isinstance(dictionary[key], dict):
		for subkey in dictionary[key]:
			printKey(dictionary[key], subkey, depth + 1)

#try:
#	category = sys.argv[1]
#	subcategory = sys.argv[2]
#except IndexError:
#	print "arguments missing"
#	exit()
#directory = "data/" + category + "-" + subcategory

with open("sampleTweet", "r") as sampleTweet:
	for line in sampleTweet:
		tweet = json.loads(line)
		print "**** original ****"
		print tweet["text"]
		# print "**** not urls ****"
		# tweet["text"] = re.sub(r'http\S+', '', tweet["text"])
		print "**** no entis ****"
		for entityType in tweet["entities"]:
			if entityType == "user_mentions":
				for i in xrange(len(tweet["entities"][entityType])):
					tweet["text"] = tweet["text"].replace(tweet["entities"][entityType][i]["screen_name"], '')
			elif entityType == "urls":
				for i in xrange(len(tweet["entities"][entityType])):
					for both in ["url", "expanded_url"]:
						tweet["text"] = tweet["text"].replace(tweet["entities"][entityType][i][both], '')
		tweet["text"] = tweet["text"].replace("#", '')
		print tweet["text"]
		print "**** no html& ****"
		tweet["text"] = re.sub(r'\&\S+;', '', tweet["text"])
		print tweet["text"]
		print "**** no punct ****"
		regex = re.compile('[%s]' % re.escape(string.punctuation))
		text = regex.sub('', tweet["text"])
		print text
		print "**** lemmatiz ****"
		# get all tokens
		word_punct_tokenizer = WordPunctTokenizer()
		tokens = word_punct_tokenizer.tokenize(text)
		lem = WordNetLemmatizer()
		ps = PorterStemmer()
		words = [lem.lemmatize(ps.stem(w.lower())) for w in tokens]
		print words
		print "**** stopwrds ****"
		words = list(filter(lambda word: word not in stopwords.words('english'), words))
		print words
		print "******************"
