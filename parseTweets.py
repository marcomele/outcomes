try:
	import json
except ImportError:
	import simplejson as json
import ast
import re
from pprint import pprint
from threading import Thread
import time
import random
from Queue import Queue

def printKey(dictionary, key, depth = 0):
	print "\t" * depth + key
	if isinstance(dictionary[key], dict):
		for subkey in dictionary[key]:
			printKey(dictionary[key], subkey, depth + 1)

category = "society"
subcategory = "issues"
rawFileName = "data/" + category + "-" + subcategory + "/output"
queue = Queue()
produced = 0
consumed = 0

class ProducerThread(Thread):
	def getOneTweet(Thread, line):
		while True:
			try:
				[first, reminder] = line.split("}{", 1)
				yield first + "}"
				line = "{" + reminder
			except ValueError:
				yield line
				break
	def run(self):
		global rawFileName
		global queue
		global produced
		with open(rawFileName, "r") as rawFile:
			for line in rawFile:
				for literal in ProducerThread.getOneTweet(self, line):
					queue.put(literal)
					produced += 1

class ConsumerThread(Thread):
	def run(self):
		global queue
		global consumed
		while True:
			literal = queue.get()
			consumed += 1
			print literal[:10]
			queue.task_done()

ProducerThread().start()
ConsumerThread().start()
