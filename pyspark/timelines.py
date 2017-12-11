import os
import sys
import json
import re
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("edu.uic.cs.cs594.propensityscore.py")
sc = SparkContext(conf = conf)

# load tweets
users_rdd = sc.textFile(sys.argv[1])
all_tweets_rdd = sc.textFile(sys.argv[2]).map(lambda string: json.loads(string))
users = users_rdd.collect()
filter_tweets_rdd = all_tweets_rdd.filter(lambda tweet: tweet["author"] in users)

output_rdd = filter_tweets_rdd.map(lambda tweet: json.dumps(tweet))

# output
output_rdd.saveAsTextFile("bias_tweets/population_tweet")
