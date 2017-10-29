from __future__ import division
try:
	import json
except ImportError:
	import simplejson as json
from pprint import pprint
from dateutil.parser import parse
from dateutil.tz import *
from datetime import *
import os
import sys

def err(str):
	sys.stderr.write(str)

try:
	tokenfilename = sys.argv[1]
	folder = sys.argv[2]
except IndexError:
	err("missing argument\n")
	exit()

with open(tokenfilename, "r") as tokenfile:
	tokens = [token[:-1] for token in tokenfile.readlines()]
print tokens

for filename in os.listdir(folder):
	with open(folder + "/" + filename, "r") as userfile:
		print filename
