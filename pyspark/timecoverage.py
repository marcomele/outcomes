import os
import sys
import json
import re
from pyspark import SparkConf, SparkContext
from operator import add

conf = SparkConf().setAppName("edu.uic.cs.cs594.propensityscore.py")
sc = SparkContext(conf = conf)

# load tweets
input_rdd = sc.textFile(sys.argv[1]).map(lambda string: json.loads(string))
datetime_rdd = input_rdd.map(lambda tweet: str(tweet["datetime"]))
datestring_rdd = datetime_rdd.map(lambda date: "-".join(date.split(" ")[:3]))
count_rdd = datestring_rdd.map(lambda date: (date, 1)).reduceByKey(lambda x, y: x + y)

# output
count_rdd.saveAsTextFile("bias_tweets/date_count")
