import os
import sys
import json
import re
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("edu.uic.cs.cs594.propensityscore.py")
sc = SparkContext(conf = conf)

def istreatment(datetime):
	date = str(datetime).split(" ")
	return date[1] == "Sep" and 1 <= int(date[2]) <= 25

def clean(word):
	w = word.lower()
	re.sub(r'\n', ' ', w)
	re.sub(r'\r', ' ', w)
	re.sub(r'http\S+', '', w)
	re.sub(r'\u[0-9]+', '', w)
	re.sub(r'#', '', w)
	re.sub(r'@', '', w)
	re.sub(r'-', ' ', w)
	re.sub(r'.', ' ', w)
	re.sub(r'"', '', w)
	try:
		w = str(w)
	except UnicodeError:
		pass
	return w

# load tweets
tweets_rdd = sc.textFile(sys.argv[1]).map(lambda string: json.loads(string))
treatment_rdd = tweets_rdd.filter(lambda tweet: istreatment(tweet["datetime"]))
print treatment_rdd.count()
#words_rdd = treatment_rdd.flatMap(lambda tweet: tweet["text"].split(" ")).map(lambda word: clean(word))#.filter(lambda word: word)

#word_count_rdd = words_rdd.map(lambda word: (word, 1)).reduceByKey(lambda x, y: x + y)
#relevant_words_rdd = word_count_rdd.filter(lambda t: 7000 <= t[1] <= 60000)
#relevant_words_rdd
#word_count_rdd.sortBy(lambda keyValue: keyValue[1], ascending = False).saveAsTextFile("bias_tweets/treatment_words")# = word_count_rdd.collect()

#user_words_rdd = treatment_rdd.map(lambda tweet: (tweet["author"], tweet["text"])).groupByKey().flatMapValue()


# output
#output_rdd.saveAsTextFile("bias_tweets/population_tweet")
