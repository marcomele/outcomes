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

	api = tweepy.API(auth)
	status = api.get_status(911994120658239488)
	jstat = json.loads(json.dumps(status._json))
	myId = jstat["user"]["id_str"]

	user2 = api.get_user("Fra_Marcantoni")
	juser2 = json.loads(json.dumps(user2._json))
	fraId = juser2["id_str"]

	timeline = api.user_timeline(fraId)
	st = timeline[0]
	jst = json.loads(json.dumps(st._json))
	print jst["text"]
