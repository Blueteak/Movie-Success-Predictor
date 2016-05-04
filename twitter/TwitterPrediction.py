'''
Main program for predicting box office success via Twitter
Need box office / budget info to proceed
'''
from TwitterQuery import *
from sklearn.linear_model import SGDClassifier
from sklearn import metrics

movies = []
with open('data_labels.csv') as file:
    for line in file:
        movies.append(line.split(','))

api,ia = get_twitter_imdb_access()
with open('twitter_data.csv','a') as file:
    count = 5642
    for j in range(count,len(movies)):
        m = movies[j]
        d = twitter_search(m[1],api,ia)
        d = [x for y in d for x in y]
        m[2] = m[2][0]
        data = m + d
        count += 1
        file.write(','.join(str(i) for i in data)+'\n')
        print count,'Written ',m[1],' data to file'
        #insert m,actor_polarity,actor_subjectivity,actor_followers,director_polarity,director_subjectivity,director_followers into table
        #maybe insert label, also

#get all data

#shuffle and split into train data and test data
#train_data, test_data, train_labels, test_labels = [],[],[],[]

#clf = SGDClassifier()
#clf.fit(train_data,train_labels)

#metrics.roc_auc_score(clf.predict(train_labels),test_labels)
