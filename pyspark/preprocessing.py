import os
import sys
import json
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("edu.uic.cs.cs594.fakenews")
sc = SparkContext(conf = conf)

input_rdd = sc.textFile(sys.argv[1])
json_rdd = input_rdd.map(lambda string: json.loads(string)
authors_rdd = json_rdd.map(lambda j: j["author"]).distinct()
authors_rdd.saveAsTextFile(sys.argv[0] + "_out")
