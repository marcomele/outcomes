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

# parse nohup files and create metadata and dictionary
for [category, subcategory] in [["business", "construction"], ["society", "issues"]]:
	metadata = {
		"count" : 0,
		"unauthorized" : 0,
		"status-not-found" : 0,
		"internal-error" : 0,
		"over-capacity" : 0,
		"page-not-exists" : 0,
		"user-suspended" : 0,
		"connection-timed-out" : 0,
		"total" : 0
	}
	directory = "data/" + category + "-" + subcategory + "/"
	nohupfile =  directory + "/nohup.out"
	with open(nohupfile, "rU") as nohup:
		for record in nohup:
			if record and not "rate limit reached, waiting..." in record:
				if "u'code': 179" in record:
					metadata["unauthorized"] += 1
				elif "u'code': 144" in record:
					metadata["status-not-found"] += 1
				elif "u'code': 131" in record:
					metadata["internal-error"] +=1
				elif "u'code': 130" in record:
					metadata["over-capacity"] += 1
				elif "u'code': 34" in record:
					metadata["page-not-exists"] += 1
				elif "u'code': 63" in record:
					metadata["user-suspended"] += 1
				elif "api.twitter.com timed out" in record:
					metadata["connection-timed-out"] += 1
				elif int(record):
					metadata["count"] += 1
				metadata["total"] -= 1
		assert not sum(int(metadata[key]) for key in metadata)
		metadata["total"] *= -1
	total = metadata["total"]
	for key in metadata:
		count = metadata[key]
		metadata[key] = {"count" : count, "percent" : str(round(100 * float(count) / total, 2)) + "%"}
	outfile = directory + "/metadata"
	with open(outfile, "w") as out:
		out.write(str(metadata))
	print "metadata saved in " + outfile
