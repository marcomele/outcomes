try:
	import json
except ImportError:
	import simplejson as json
import ast
with open("data/sampleOutput") as sampleOutput:
	for line in sampleOutput:
		dic = ast.literal_eval(line)
		print dic["text"]
