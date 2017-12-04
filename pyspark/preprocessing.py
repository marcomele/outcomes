import os
import sys
import json
import re
from pyspark import SparkConf, SparkContext

def clean(tweet):
    text = tweet["text"]
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\&\S+;', '', text)
    text.replace('#', '')
    tweet["text"] = text
    return tweet

conf = SparkConf().setAppName("edu.uic.cs.cs594.fakenews.preprocessing.py")
sc = SparkContext(conf = conf)

# load tweets
input_rdd = sc.textFile(sys.argv[1])
structured_rdd = input_rdd.map(lambda string: json.loads(string))

# data cleaning
cleaned_rdd = structured_rdd.map(lambda tweet: clean(tweet))

# output
output_rdd = cleaned_rdd.map(lambda tweet: json.dumps(tweet))
output_rdd.saveAsTextFile(sys.argv[1].split("/")[0] + "/output")
