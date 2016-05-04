from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import metrics
from sklearn import cross_validation
from random import shuffle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import interp

data = []
with open('twitter_data.csv','r') as file:
    index = 0
    for line in file:
        index += 1
        data.append(line.split(','))
        # id, title, label, actor_polarity, actor_subjectivity, actor_followers, director_polarity, director_subjectivity, director_followers
        
        #fix line with error
        if data[-1][0] == '3628786':
            del data[-1][1]

        # convert strings to numbers
        for i in (0,2,5,8):
            data[-1][i] = int(data[-1][i])

        for i in (3,4,6,7):
            data[-1][i] = float(data[-1][i])


#full feature vector
#features = np.array([i[3:] for i in data])

#just follower counts
#features = np.array([[i[5],i[8]] for i in data])

#just sentiment
features = np.array([[i[3],i[4],i[6],i[7]] for i in data])

labels = np.array([i[2] for i in data])

def print_metrics(clf):

    #scores = cross_validation.cross_val_score(clf,features,labels,cv=5,scoring='accuracy')
    #print 'Accuracy:',scores.mean()
    
    cv = cross_validation.StratifiedKFold(labels,n_folds=5)

    mean_tpr = 0.0
    mean_fpr = np.linspace(0,1,100)
    all_tpr = []

    for i, (train,test) in enumerate(cv):
        probas_ = clf.fit(features[train],labels[train]).predict_proba(features[test])

        fpr,tpr,thresholds = metrics.roc_curve(labels[test],probas_[:,1])
        mean_tpr += interp(mean_fpr,fpr,tpr)
        mean_tpr[0] = 0.0
        roc_auc = metrics.auc(fpr,tpr)

        plt.plot(fpr,tpr,lw=1,label='ROC fold %d (area = %0.2f)' % (i,roc_auc))

    plt.plot([0,1],[0,1],'--',color=(0.6,0.6,0.6),label='Luck')
    
    mean_tpr /= len(cv)
    mean_tpr[-1] = 1.0
    mean_auc = metrics.auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, 'k--',
             label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.savefig('auc_sent.png')
    
    


clf = AdaBoostClassifier()
print_metrics(clf)
