try:
	import json
except ImportError:
	import simplejson as json
import ast
import re
from pprint import pprint

def printKey(dictionary, key, depth = 0):
	print "\t" * depth + key
	if isinstance(dictionary[key], dict):
		for subkey in dictionary[key]:
			printKey(dictionary[key], subkey, depth + 1)

# with open("data/sampleOutput") as sampleOutput:
# 	for line in sampleOutput:
# 		dictionary = ast.literal_eval(line)
# 		for key in dictionary:
# 			printKey(dictionary, key)

categories = {
		"business" : {
			"construction" : {
				"count" : 0,
				"unauthorized" : 0,
				"status-not-found" : 0,
				"internal-error" : 0,
				"over-capacity" : 0,
				"page-not-exists" : 0,
				"user-suspended" : 0,
				"connection-timed-out" : 0,
				"total" : 0
		}},
		"society" : {
			"issues" : {
				"count" : 0,
				"unauthorized" : 0,
				"status-not-found" : 0,
				"internal-error" : 0,
				"over-capacity" : 0,
				"page-not-exists" : 0,
				"user-suspended" : 0,
				"connection-timed-out" : 0,
				"total" : 0
		}}
	}

# parse nohup files and create metadata and dictionary
for category in categories:
	for subcategory in categories[category]:
		nohupfile = "data/" + category + "-" + subcategory + "/nohup.out"
		with open(nohupfile, "rU") as nohup:
			for record in nohup:
				if record and not "rate limit reached, waiting..." in record:
					if "u'code': 179" in record:
						categories[category][subcategory]["unauthorized"] += 1
					elif "u'code': 144" in record:
						categories[category][subcategory]["status-not-found"] += 1
					elif "u'code' : 131" in record:
						categories[category][subcategory]["internal-error"] +=1
					elif "u'code': 130" in record:
						categories[category][subcategory]["over-capacity"] += 1
					elif "u'code': 34" in record:
						categories[category][subcategory]["page-not-exists"] += 1
					elif "u'code': 63" in record:
						categories[category][subcategory]["user-suspended"] += 1
					elif "api.twitter.com timed out" in record:
						categories[category][subcategory]["connection-timed-out"] += 1
					elif int(record):
						categories[category][subcategory]["count"] += 1
					categories[category][subcategory]["total"] -= 1
			assert not sum(int(categories[category][subcategory][key]) for key in categories[category][subcategory])
			categories[category][subcategory]["total"] *= -1
pprint(categories)
