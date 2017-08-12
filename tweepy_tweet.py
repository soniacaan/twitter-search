# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import *
import tweepy
from tweepy import OAuthHandler
import re
from pprint import pprint
import os
import datetime

now = datetime.datetime.now()
day=int(now.day)
month=int(now.month)
year=int(now.year)

#Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '165885348-V0R5egsyTfGd0ig0lTXbZuyy0q1gWIHLClZrftZa'
ACCESS_SECRET = 'RZ9iCWiutOgzgr7yLnllTrYOtFo1Y4IdWKfgigkrMwxmM'
CONSUMER_KEY = 'o4kJR7rHtZY4ivBd4GRPAQvu1'
CONSUMER_SECRET = 'oNguU1O3YMvvRa1Wu85y42bW280P9vcttqUNQvWhZ9c1j78YpA'

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

places = api.geo_search(query="Canada", granularity="country")
place_id = places[0].id

#tweets = api.search(q="place:%s" % place_id)
tweets = tweepy.Cursor(api.search, q="place:"+place_id).items()
#print(tweets)
print(place_id)

# We use the file saved from last step as example
tweets_filename = 'twitter_1000tweets.txt'
tweets_file = open(tweets_filename, "r")



while True:
    try:
        tweet = next(tweets)
        count += 1
        #use count-break during dev to avoid twitter restrictions
        if (count>10):
            break
        print(tweet)
    except tweepy.TweepError:
        #catches TweepError when rate limiting occurs, sleeps, then restarts.
        #nominally 15 minnutes, make a bit longer to avoid attention.
        print("sleeping....")
        time.sleep(60*16)
        tweet = next(tweets)
    except StopIteration:
        break
    try:
        print("Writing to JSON tweet number:"+str(count))
        json.dump(tweet._json,file,sort_keys = True,indent = 4)
        
    except UnicodeEncodeError:
        errorCount += 1
        print("UnicodeEncodeError,errorCount ="+str(errorCount))

#print("completed, errorCount ="+" total tweets="+str(count))
    


#for tweet in tweepy.Cursor(api.search, q=place_id).items():
    #with open('tweet.json', 'a') as f:
        #f.write(json.dumps(tweet._json))
        #f.write("\n")

#with open('tweet._json', 'w') as outfile:
#for tweet in tweets:
        #target = (tweet.text + " | " + tweet.place.name if tweet.place else "Undefined place")
        #json.dumps(tweet, outfile)
        #process_or_store(tweet)
        #outfile.write('\n')
        #print(place_id)
        





