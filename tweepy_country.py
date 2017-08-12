# Import the necessary package to process data in JSON format
import json

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

places = api.geo_search(query="Canada", granularity="country")
place_id = places[0].id

tweets = api.search(q="place:%s" % place_id)


with open('tweet.txt', 'w') as outfile:
    for tweet in tweets:
		#tweet = tweets[0]
        json_str = json.dumps(tweet._json, indent=4)
        outfile.write(json.dumps(tweet._json, indent=4))
        #print(json_str)
        #json.dumps(json_str, outfile)
        outfile.write("\n")
        #outfile.write([tweet.text.encode('utf-8'), tweet.created_at, tweet.id, tweet.place, tweet.user])
        #print(tweet.text.encode('utf-8'), tweet.created_at, tweet.id, tweet.place, tweet.user)


#with open('tweet.txt', 'a') as outfile:
 #   for tweet in tweets:
  #      print(tweet)
   #     json.dumps(tweet, outfile)
    #    outfile.write('\n')


    #json_str = json.dumps(tweets, indent=4)
    #print(json_str)

#for tweet in tweets:
    #print(tweet.text + " | " + tweet.place.name if tweet.place else "Undefined place")
    
         
    #print(tweet.id, tweet.text, tweet.created_at, tweet.user, tweet.place)