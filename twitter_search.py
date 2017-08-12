# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import *
#Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '165885348-V0R5egsyTfGd0ig0lTXbZuyy0q1gWIHLClZrftZa'
ACCESS_SECRET = 'RZ9iCWiutOgzgr7yLnllTrYOtFo1Y4IdWKfgigkrMwxmM'
CONSUMER_KEY = 'o4kJR7rHtZY4ivBd4GRPAQvu1'
CONSUMER_SECRET = 'oNguU1O3YMvvRa1Wu85y42bW280P9vcttqUNQvWhZ9c1j78YpA'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_search = Twitter(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_search.geo.search(query="Canada", granularity="country")
place_id = iterator['result']['places'][0]['id']


# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
result = twitter_search.search.tweets(q="place:%s" % place_id)

for tweet in result['statuses']:
    print(tweet['text'] + " | " + tweet['place']['name'] if tweet['place'] else "Undefined place")

