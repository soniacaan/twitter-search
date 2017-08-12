from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sentiment_mod as s


#consumer key, consumer secret, access token, access secret.
ACCESS_TOKEN = '165885348-V0R5egsyTfGd0ig0lTXbZuyy0q1gWIHLClZrftZa'
ACCESS_SECRET = 'RZ9iCWiutOgzgr7yLnllTrYOtFo1Y4IdWKfgigkrMwxmM'
CONSUMER_KEY = 'o4kJR7rHtZY4ivBd4GRPAQvu1'
CONSUMER_SECRET = 'oNguU1O3YMvvRa1Wu85y42bW280P9vcttqUNQvWhZ9c1j78YpA'

from twitterapistuff import *


class listener(StreamListener):

    def on_data(self, data):
    	
        all_data = json.loads(data)
        
        tweet = all_data["text"]
        sentiment_value, confidence = s.sentiment(tweet)
        print(tweet, sentiment_value, confidence)

        if confidence*100 >= 80:
            output = open("twitter-out.txt","a")
            output.write(sentiment_value)
            output.write('\n')
            output.close()

        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["happy"])
