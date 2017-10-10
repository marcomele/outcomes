try:
	import json
except ImportError:
	import simplejson as json
from twitter import *
try:
	from urllib.parse import parse_qs
except ImportError:
	from urlparse import parse_qs

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
	oauth = OAuth(credentials["ACCESS_TOKEN"],
		credentials["ACCESS_SECRET"],
		credentials["CONSUMER_KEY"],
		credentials["CONSUMER_SECRET"])
	return oauth

if __name__ == '__main__':
	credentials = getcredentials()
	oauth = authenticate(credentials)
	urls = {
		"authenticate_token" : "https://api.twitter.com/oauth2/token",
		"request_token" : "https://api.twitter.com/oauth/request_token",
		"authorize" : "https://api.twitter.com/oauth/authorize",
		"access_token" : "https://api.twitter.com/oauth/access_token"
	}
