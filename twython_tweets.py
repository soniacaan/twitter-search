#!/usr/bin/env python

"""
Use Twitter API to grab user information from list of organizations; 
export text file
Uses Twython module to access Twitter API
"""

import sys
import string
import json
from twython import Twython
import re #import regex
from twitter import *
import tweepy
from tweepy import OAuthHandler

#WE WILL USE THE VARIABLES DAY, MONTH, AND YEAR FOR OUR OUTPUT FILE NAME
import datetime
now = datetime.datetime.now()
day=int(now.day)
month=int(now.month)
year=int(now.year)


#FOR OAUTH AUTHENTICATION -- NEEDED TO ACCESS THE TWITTER API
t = Twython(app_key='o4kJR7rHtZY4ivBd4GRPAQvu1', #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret='oNguU1O3YMvvRa1Wu85y42bW280P9vcttqUNQvWhZ9c1j78YpA',
    oauth_token='165885348-V0R5egsyTfGd0ig0lTXbZuyy0q1gWIHLClZrftZa',
    oauth_token_secret='RZ9iCWiutOgzgr7yLnllTrYOtFo1Y4IdWKfgigkrMwxmM')

   
#REPLACE WITH YOUR LIST OF TWITTER USER IDS
#ids = "4816,9715012,13023422, 13393052,  14226882,  14235041, 14292458, 14335586, 14730894,\
   # 15029174, 15474846, 15634728, 15689319, 15782399, 15946841, 16116519, 16148677, 16223542,\
    #16315120, 16566133, 16686673, 16801671, 41900627, 42645839, 42731742, 44157002, 44988185,\
    #48073289, 48827616, 49702654, 50310311, 50361094,"

#ACCESS THE LOOKUP_USER METHOD OF THE TWITTER API -- GRAB INFO ON UP TO 100 IDS WITH EACH API CALL
#THE VARIABLE USERS IS A JSON FILE WITH DATA ON THE 32 TWITTER USERS LISTED ABOVE
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

max_tweets = 100
users = t.search(q="place:%s" % place_id, count=max_tweets)



#users = t.lookup_user(user_id = ids)

#NAME OUR OUTPUT FILE - %i WILL BE REPLACED BY CURRENT MONTH, DAY, AND YEAR
outfn = "twitter_user_data_%i.%i.%i.txt" % (now.month, now.day, now.year)

#NAMES FOR HEADER ROW IN OUTPUT FILE
fields = "tweet_id status screen_name name created_at url followers_count friends_count statuses_count \
    favourites_count listed_count \
    contributors_enabled description protected location lang expanded_url".split()

#INITIALIZE OUTPUT FILE AND WRITE HEADER ROW   
#outfp = open(outfn, "w")
#outfp.write("\t".join(fields) + "\n")  # header

tweet = {}

#THE VARIABLE 'USERS' CONTAINS INFORMATION OF THE 32 TWITTER USER IDS LISTED ABOVE
#THIS BLOCK WILL LOOP OVER EACH OF THESE IDS, CREATE VARIABLES, AND OUTPUT TO FILE
for entry in users['statuses']:
    #CREATE EMPTY DICTIONARY
    r = {}
    for f in fields:
        r[f] = ""
    #ASSIGN VALUE OF 'ID' FIELD IN JSON TO 'ID' FIELD IN OUR DICTIONARY
    r['tweet_id'] = entry['id']
    r['status'] = entry['text']
    #only assign unique tweet_id
    tweet[r['tweet_id']] = str(r['status'])
    #print(tweet)
    #print(r['status'])
    #SAME WITH 'SCREEN_NAME' HERE, AND FOR REST OF THE VARIABLES
    r['screen_name'] = entry['user']['screen_name']
    #r['name'] = entry['name']
    r['created_at'] = entry['created_at']
    #r['url'] = entry['url']
    #r['followers_count'] = entry['followers_count']
    #r['friends_count'] = entry['friends_count']
    #r['statuses_count'] = entry['statuses_count']
    #r['favourites_count'] = entry['favourites_count']
    #r['listed_count'] = entry['listed_count']
    #r['contributors_enabled'] = entry['contributors_enabled']
    #r['description'] = entry['description']
    #r['protected'] = entry['protected']
    if entry['place'] is not None:
        r['location'] = entry['place']['name']
    else:
        r['location'] = ''

    #r['lang'] = entry['lang']

    #NOT EVERY ID WILL HAVE A 'URL' KEY, SO CHECK FOR ITS EXISTENCE WITH IF CLAUSE
    #if 'url' in entry['entities']:
     #   r['expanded_url'] = entry['entities']['url']['urls'][0]['expanded_url']
    #else:
     #   r['expanded_url'] = ''
    #CREATE EMPTY List
    lst = []

    #ADD DATA FOR EACH VARIABLE
    for f in fields:
        lst.append(str(r[f]).replace("\/", "/"))
    #WRITE ROW WITH DATA IN LIST
    #outfp.write("\t".join(lst) + "\n")
#outfp.close()

def processTweet(tweet):
    #lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL', tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER', tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet


#initialize stopWords
stopWords = []

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end

#start getfeatureVector
def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end


#process stopwords
st = open('stopwords.txt', 'r')
stopWords = getStopWordList('stopwords.txt')


process = []

for value in tweet.values():
    #print(value)
    processTweets = processTweet(value)
    featureVector = getFeatureVector(processTweets)
    process.append(str(featureVector))

print(process)
print("total tweets " + count(tweet.))
