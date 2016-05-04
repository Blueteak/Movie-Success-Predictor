movies = []
success = 0
failure = 0
with open('imdb_based_predictor/movie_info.csv','r') as file:
    for line in file:
        l = line.split(',')
        id = l[0]
        title = l[1]
        country = l[3]
        budget  = l[4]
        gross = l[6]
        if budget <> '' and gross <> '' and country == 'USA':
            try:
                if budget[0] == '$':
                    budget = int(budget[1:])
                else:
                    continue
                if gross[0] == '$':
                    gross = int(gross.split(' ')[0][1:])
                else:
                    continue
            except ValueError:
                continue
            s = 1
            if gross <= budget:
                s = 0
                failure += 1
            else:
                success += 1
            movies.append([id,title,s])

print success,failure

with open('data_labels.csv','w') as file:
    for m in movies:
        file.write(str(m[0]) + ',' + m[1] + ',' + str(m[2]) + '\n')
