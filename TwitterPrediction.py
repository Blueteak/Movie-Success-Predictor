'''
Main program for predicting box office success via Twitter
Need box office / budget info to proceed
'''
from TwitterQuery import *
from sklearn.linear_model import SGDClassifier
from sklearn import metrics

#list of movies (still need)
movies = None

api,ia = get_twitter_imdb_access()
for m in movies:
    d = twitter_search(m,api,ia)
    d = [d[0][0],d[0][1],d[1][0],d[1][1]]
    #insert m,actor_polarity,actor_subjectivity,director_polarity,director_subjectivity into table
    #maybe insert label, also

#get all data

#shuffle and split into train data and test data
train_data, test_data, train_labels, test_labels = [],[],[],[]

clf = SGDClassifier()
clf.fit(train_data,train_labels)

metrics.roc_auc_score(clf.predict(train_labels),test_labels)
