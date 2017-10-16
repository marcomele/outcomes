try:
	import json
except ImportError:
	import simplejson as json
from twitter import *
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
			"diseases" : 4,
			"mental" : 45,
			"pharmacy" : 3
		},
		"society" : {
			"issues" : 1,
			"law" : 9,
			"relationships" : 2
		},
		"business" : {
			"construction-and-maintenance" : 1,
			"financial-services" : 4,
			"investing" : 76
		}
	}

	api = tweepy.API(auth)
	for category in categories:
		print "*********** " + category + "****************"
		for subcat in category:
			print "retrieving user ids for " + category + "/" + subcat + "..."
			filename = "mergedData/" + category + "-" + subcat + "_ids.txt"
			with open(filename, "r") as inputFile:
				for tweetID in inputFile:
					status = api.get_status(tweetID)
					userID = json.loads(json.dups(status._json))["user"]["id_str"]
					print userID

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
