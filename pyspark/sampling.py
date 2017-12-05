import os
import sys
import json
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("edu.uic.cs.cs594.fakenews.sampling.py")
sc = SparkContext(conf = conf)

# load tweets
input_rdd = sc.textFile(sys.argv[1])
structured_rdd = input_rdd.map(lambda string: json.loads(string))
structured_rdd.cache()
num_total_users = structured_rdd.map(lambda tweet: tweet["author"].strip().lower()).distinct().count()

# load biased users
bias_rdd = sc.textFile(sys.argv[2])
biased_users_rdd = bias_rdd.map(lambda row: str(row.split("\t")[0].strip().lower()))
biased_users = biased_users_rdd.collect()
num_biased_users = len(biased_users)

# ratio_biased_users = (float) num_biased_users / num_total_users
ratio_biased_users = 0.1

# split bias_rdd into biased and unbiased
min_tweets = 5
max_tweets = 35
biased_users_rdd = structured_rdd.groupBy(lambda tweet: tweet["author"].strip().lower()).filter(lambda pair: pair[0] in biased_users and min_tweets <= len(pair[1]) <= max_tweets)
unbiased_users_rdd = structured_rdd.groupBy(lambda tweet: tweet["author"].strip().lower()).filter(lambda pair: pair[0] not in biased_users and min_tweets <= len(pair[1]) <= max_tweets)

# sample from the two portions
sampling_ratio = .01
sampled_biased_users_rdd = biased_users_rdd.sample(False, sampling_ratio * ratio_biased_users)
sampled_unbiased_users_rdd = unbiased_users_rdd.sample(False, sampling_ratio * (1 - ratio_biased_users))
sampled_biased_users_rdd.cache()
sampled_unbiased_users_rdd.cache()
total_sampled_users = sampled_biased_users_rdd.count() + sampled_unbiased_users_rdd.count()

# output
sampled_unbiased_tweets_rdd = sampled_unbiased_users_rdd.flatMap(lambda pair: pair[1]).map(lambda tweet: json.dumps(tweet)).cache()
sampled_biased_tweets_rdd = sampled_biased_users_rdd.flatMap(lambda pair: pair[1]).map(lambda tweet: json.dumps(tweet)).cache()
total_sampled_tweets = sampled_unbiased_tweets_rdd.count() + sampled_biased_tweets_rdd.count()
sampled_unbiased_tweets_rdd.union(sampled_biased_tweets_rdd).saveAsTextFile(sys.argv[1].split("/")[0] + "/output_samples")
print "total sampled users: " + str(total_sampled_users)
print "total sampled tweets: " + str(total_sampled_tweets)
