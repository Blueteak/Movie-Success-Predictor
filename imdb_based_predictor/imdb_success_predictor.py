import scipy
import numpy
from sklearn import linear_model
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold

def load_movie_info():
    f = open('movie_info.csv', 'r')
    lines = f.readlines()
    f.close()

    movie_info = []
    for line in lines:
        line = line.strip()
        movie_info.append(line.split(','))
    format_fields(movie_info)
    return movie_info

def format_fields(movie_info):
    for i in range(0, len(movie_info)):

	#extract mpaa rating from text value
    	mpaa = movie_info[i][2]
        mpaa_rating = mpaa.split(' ')
	if len(mpaa_rating) == 0:
                movie_info[i][2] = 0
	elif mpaa_rating[0] =="Rated" and len(mpaa_rating)>0:
		movie_info[i][2] = mpaa_rating[1]
	elif "R" in mpaa_rating:
        	movie_info[i][2] = "R"
	elif "PG" in mpaa_rating:
                movie_info[i][2] = "PG"
	elif "PG-13" in mpaa_rating:
                movie_info[i][2] = "PG-13"
	else:
		movie_info[i][2] = 0
	
	#rmove $ sign from budget
	budget = movie_info[i][4]
	if len(budget) == 0:
		movie_info[i][4] = 0
	elif budget[0] == '$': 
		movie_info[i][4] = budget[1:]
	else:
		movie_info[i][4] = 0

	#extract opening_weekend amount value
	opening_weekend =  movie_info[i][5]
	opening_weekend_arr = opening_weekend.split(' ')
	if len(opening_weekend_arr) > 0 and len(opening_weekend_arr[0]) > 0 and opening_weekend_arr[0][0] == '$':
                open_wknd = opening_weekend_arr[0]
                movie_info[i][5] = open_wknd[1:]
	else:
		movie_info[i][5] = 0

	#extract gross amount value
        gross =  movie_info[i][6]
        gross_arr = gross.split(' ')
        if len(gross_arr) > 0 and len(gross_arr[0]) > 0 and gross_arr[0][0] == '$':
                gross = gross_arr[0]
                movie_info[i][6] = gross[1:]
        else:
                movie_info[i][6] = 0
        
    print movie_info

    return movie_info

def main():
    movie_info = load_movie_info()


if __name__ == '__main__':
    main()

