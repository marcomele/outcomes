try:
	import json
except ImportError:
	import simplejson as json
from twitter import *
import time
try:
	from urllib.parse import parse_qs
except ImportError:
	from urlparse import parse_qs
import tweepy

def getcredentials():
	credentials = {
		"ACCESS_TOKEN" : None,
		"ACCESS_SECRET" : None,
		"CONSUMER_KEY" : None,
		"CONSUMER_SECRET" : None
	}
	for key in credentials:
		f = open(key + ".key", "r")
		credentials[key] = f.readline()[0:-1]
	return credentials

def authenticate(credentials):
	return OAuth1(credentials["ACCESS_TOKEN"],
		credentials["ACCESS_SECRET"],
		credentials["CONSUMER_KEY"],
		credentials["CONSUMER_SECRET"])

if __name__ == '__main__':
	# create authentication object
	credentials = getcredentials()
	auth = tweepy.OAuthHandler(credentials["CONSUMER_KEY"], credentials["CONSUMER_SECRET"])
	auth.set_access_token(credentials["ACCESS_TOKEN"], credentials["ACCESS_SECRET"])

	# categories
	categories = {
		"health" : {
			"diseases" : 0,
			"mental" : 0,
			"pharmacy" : 0
		},
		"society" : {
			"issues" : 0,
			"law" : 0,
			"relationships" : 0
		},
		"business" : {
			"construction-and-maintenance" : 0,
			"financial-services" : 0,
			"investing" : 0
		}
	}

	api = tweepy.API(auth)

	#for category in categories:
	category = "society"
	#print "*********** " + category + "****************"
	#for subcat in categories[category]:
	subcat = "issues"
	#print "retrieving user ids for " + category + "/" + subcat + "..."
	filename = "mergedData/" + category + "-" + subcat + "_ids.txt"
	with open(filename, "r") as inputFile:
		for tweetID in inputFile:
			while True:
				try:
					#print tweetID + "does exist"
					status = api.get_status(tweetID)
					with open("output", "a") as outputFile:
						outputFile.write(str(json.loads(json.dumps(status._json))))
						print tweetID
						break
				except tweepy.RateLimitError as r:
					print "rate limit reached, waiting..."
					time.sleep(60)
				except tweepy.TweepError as e:
					print e
					categories[category][subcat] += 1
					break
	print categories[category][subcat]
					#userID = json.loads(json.dups(status._json))["user"]["id_str"]
					#print userID

	#status = api.get_status(911994120658239488)
	#jstat = json.loads(json.dumps(status._json))
	#myId = jstat["user"]["id_str"]

	#user2 = api.get_user("Fra_Marcantoni")
	#juser2 = json.loads(json.dumps(user2._json))
	#fraId = juser2["id_str"]

	#timeline = api.user_timeline(fraId)
	#st = timeline[0]
	#jst = json.loads(json.dumps(st._json))
	#print jst["text"]
