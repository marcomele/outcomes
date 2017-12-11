import os
import sys
import json
import re
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("edu.uic.cs.cs594.propensityscore.py")
sc = SparkContext(conf = conf)

def datestring(datetime):
	date = str(datetime).split(" ")
	month = {
		"Jan" : "01",
		"Feb" : "02",
		"Mar" : "03",
		"Apr" : "04",
		"May" : "05",
		"Jun" : "06",
		"Jul" : "07",
		"Aug" : "08",
		"Sep" : "09",
		"Oct" : "10",
		"Nov" : "11",
		"Dec" : "12"
	}
	return "-".join([month[date[1]], date[2]])

def tweetarray(tweet):
	isTreated = "campaign" in tweet["text"]
	tr_ts = datestring(tweet["datetime"]) if isTreated else "Z"
	eff_ts_1 = datestring(tweet["datetime"]) if "debate" in tweet["text"] else "Z"
	eff_ts_2 = "00" if eff_ts_1 == "Z" else datestring(tweet["datetime"])
	return [isTreated, tr_ts, eff_ts_1, eff_ts_2]

def reducearray(left, right):
	return [left[0] or right[0], min(left[1], right[1]), min(left[2], right[2]), max(left[3], right[3])]

def binary(array):
	isTreated = array[0]
	eff_before = isTreated and array[2] != "Z" and array[2] < array[1] or not isTreated and array[2] != "Z" and array[2] < "09-01"
	eff_after = isTreated and array[3] != "00" and array[3] > array[1] or not isTreated and array[3] != "00" and array[3] > "09-25"
	return [1 if eff_before else 0, 1 if isTreated else 0, 1 if eff_after else 0] 

# load tweets
tweets_rdd = sc.textFile(sys.argv[1]).map(lambda string: json.loads(string))
repr_rdd = tweets_rdd.map(lambda tweet: (tweet["author"], tweet))\
			.mapValues(lambda tweet: tweetarray(tweet))\
			.reduceByKey(lambda left, right: reducearray(left, right))

output_rdd = repr_rdd.mapValues(lambda array: binary(array))\
			.map(lambda kv: str(kv[0]) + "," + ",".join(str(i) for i in kv[1]))

# output
output_rdd.saveAsTextFile("bias_tweets/arrays")
