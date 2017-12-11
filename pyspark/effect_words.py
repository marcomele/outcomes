import os
import sys
import json
import re
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("edu.uic.cs.cs594.propensityscore.py")
sc = SparkContext(conf = conf)

def istreatment(datetime):
	date = str(datetime).split(" ")
	return (date[1] == "Sep" and 26 <= int(date[2])) or date[1] == "Oct" or date[1] == "Nov"

def clean(text):
	t = text.lower()
	t = re.sub(r'\n', ' ', t)
	t = re.sub(r'\r', ' ', t)
	t = re.sub(r'http\S+', ' ', t)
	t = re.sub(r'\u[0-9]+', ' ', t)
	t = re.sub(r'#', ' ', t)
	t = re.sub(r'@', ' ', t)
	t = re.sub(r'-', ' ', t)
	t = re.sub(r'\.', ' ', t)
	t = re.sub(r'"', ' ', t)
	try:
		t = str(t)
	except UnicodeError:
		pass
	return t

# load tweets
tweets_rdd = sc.textFile(sys.argv[1]).map(lambda string: json.loads(string))
treatment_rdd = tweets_rdd.filter(lambda tweet: istreatment(tweet["datetime"])).cache()
words_rdd = treatment_rdd.flatMap(lambda tweet: clean(tweet["text"]).split(" ")).filter(lambda word: len(word) > 3)

word_count_rdd = words_rdd.map(lambda word: (word, 1)).reduceByKey(lambda x, y: x + y)
word_count_rdd.sortBy(lambda keyValue: keyValue[1], ascending = False).saveAsTextFile("bias_tweets/effect_words")
