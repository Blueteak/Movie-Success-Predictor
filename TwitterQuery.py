import tweepy
import imdb
from textblob import TextBlob
import sys
sys.path.append("../")
from twitter_credentials import *
import time
from sklearn.svm import SVC
'''
Gets twitter analysis of first member of cast and director

'''
MAX_TWEETS=100

def get_twitter_imdb_access():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth)
    
    ia = imdb.IMDb()
    return api,ia

def tweet_stats(tweets,count):
    pol,sub = 0.0,0.0
    for t in tweets:
        if t.text[0:2] <> 'RT':
            blob = TextBlob(t.text)
            count += 1
            pol += blob.polarity
            sub += blob.subjectivity
        if count == MAX_TWEETS: break

    return count,pol,sub

def get_tweets(api,name,max_id=None):
    ratelimit = True
    tweets = None
    while ratelimit:
        try:
            if max_id == None:
                tweets = api.search(q=name,lang='en',count=100)
            else:
                tweets = api.search(q=name,lang='en',count=100,max_id=max_id)
            ratelimit = False
        except tweepy.error.RateLimitError:
            print 'RateLimitError, trying again in 60 seconds'
            time.sleep(60)
    return tweets

def twitter_search(movie,api,ia):
    
    s_result = ia.search_movie(movie)

    mov = s_result[0]
    ia.update(mov)

    result = []
    for i in range(2):
        name = ''
        if i == 0:
            name = mov['cast'][0]['name']
        else:
            name = mov['director'][0]['name']

        count,pol,sub = 0,0.0,0.0
        max_id = None
        for p in range(10):
            tweets = get_tweets(api,name,max_id)
            stats = tweet_stats(tweets,count)
            count = stats[0]
            pol += stats[1]
            sub += stats[2]
            max_id = tweets[-1].id
            if count == MAX_TWEETS: break

        #if they don't get to MAX_TWEETS, just assume they did

        result.append((pol,sub))
        print name
        print 'Polarity:\t',pol
        print 'Subjectivity:\t',sub
        print 'Count:\t\t',count

    return result


if __name__ == '__main__':
    api,ia = get_twitter_imdb_access()
    movies = ['The Avengers','Batman v Superman: Dawn of Justice','The Jungle Book','Captain America: The First Avenger','Star Wars: The Force Awakens']
    clf = SVC()
    data = []
    labels = []
    for m in movies:
        d = twitter_search(m,api,ia)
        data.append([d[0][0],d[0][1],d[1][0],d[1][1]])
        if m == 'Batman v Superman: Dawn of Justice':
            labels.append(0)
        else:
            labels.append(1)
    
    clf.fit(data,labels)
    d = twitter_search('Captain America: Civil War',api,ia)
    data = []
    data.append([d[0][0],d[0][1],d[1][0],d[1][1]])
    print clf.predict(data)
