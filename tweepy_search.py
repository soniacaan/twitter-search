# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import *
import tweepy
from tweepy import OAuthHandler
#Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '165885348-V0R5egsyTfGd0ig0lTXbZuyy0q1gWIHLClZrftZa'
ACCESS_SECRET = 'RZ9iCWiutOgzgr7yLnllTrYOtFo1Y4IdWKfgigkrMwxmM'
CONSUMER_KEY = 'o4kJR7rHtZY4ivBd4GRPAQvu1'
CONSUMER_SECRET = 'oNguU1O3YMvvRa1Wu85y42bW280P9vcttqUNQvWhZ9c1j78YpA'

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

for status in tweepy.Cursor(api.home_timeline).items(10):
    print(status.text)

