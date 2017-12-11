import os
import sys
import json
import re
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("edu.uic.cs.cs594.propensityscore.py")
sc = SparkContext(conf = conf)

# load tweets
input_rdd = sc.textFile(sys.argv[1])
structured_rdd = input_rdd.map(lambda string: json.loads(string)).cache()

retweets_rdd = structured_rdd.filter(lambda tweet: tweet["is_manual_retweet"] or tweet["is_retweet_button"])

authors_rdd = retweets_rdd.map(lambda tweet: (tweet["author"], tweet["retweeted_user"]))\
			.groupByKey()\
			.mapValues(lambda values: set(values))

output_rdd = authors_rdd.map(lambda kv: str(kv[0]) + ":" + ",".join(str(v) for v in kv[1]))
output_rdd.saveAsTextFile("bias_tweets/retweeted_users")
