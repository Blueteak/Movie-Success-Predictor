import tweepy
import imdb
from textblob import TextBlob
import sys
sys.path.append("../")
from twitter_credentials import *
'''
example for analyzing tweets about the cast of The Avengers

'''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

ia = imdb.IMDb()

s_result = ia.search_movie("Avengers")

aveng = s_result[0]
ia.update(aveng)

def tweet_stats(tweets):
    count,pol,sub = 0,0.0,0.0
    for t in tweets:
        if t.text[0:2] <> 'RT':
            blob = TextBlob(t.text)
            count += 1
            pol += blob.polarity
            sub += blob.subjectivity
            
    return count,pol,sub


for actor in aveng['cast']:
    name = actor['name']

    count,pol,sub = 0,0.0,0.0
    for p in range(3):
        tweets = None
        if p == 0:
            tweets = api.search(q=name,lang='en',count=100)
        else:
            tweets = api.search(q=name,lang='en',count=100,max_id=max_id)
        stats = tweet_stats(tweets)
        count += stats[0]
        pol += stats[1]
        sub += stats[2]
        max_id = tweets[-1].id

    if count == 0: break
    if count < 25: break
    print name
    print 'Polarity:\t',pol/count
    print 'Subjectivity:\t',sub/count
    print 'Count:\t\t',count
