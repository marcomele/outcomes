import os
import sys
import json
import re
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("edu.uic.cs.cs594.fakenews.preprocessing.py")
sc = SparkContext(conf = conf)

# load tweets
input_rdd = sc.textFile(sys.argv[1])
structured_rdd = input_rdd.map(lambda string: json.loads(string))

# word count
words_rdd = structured_rdd.flatMap(lambda tweet: tweet["text"].split(" "))

count_rdd = words_rdd.map(lambda word: (word, 1)).reduceByKey(lambda a,b: a + b)



# output
# output_rdd = tokens_rdd.map(lambda tweet: json.dumps(tweet))
count_rdd.saveAsTextFile(sys.argv[1].split("/")[0] + "/output_count")
