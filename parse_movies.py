'''
This turns the movies.list file from ftp://ftp.funet.fi/pub/mirrors/ftp.imdb.com/pub/ into movie titles and years
It filters out tv shows and removes some junk from the title
The years (2011-2015) are just arbitrary for now
'''

with open('../movies.list','r') as file:
    count = 0
    for lines in file:
        if lines[0] == '"':
            continue 
        line = lines.split('\t')
        try:
            year = int(line[-1].split('\n')[0])
        except:
            continue
        if year < 2011 or year > 2015:
            continue 
        title = ''
        temp = line[0].split(' ')
        for w in temp:
            if w == '': continue
            if (w[0] <> '(' and w[-1] <> ')'): 
                if len(w) < 4:
                    title += w + ' ' 
                elif (w[0:2] <> '{{' and w[-3:] <> '}}'):
                    title += w + ' ' 
                    
        title = title[:-1]

        print title,year

        count += 1
       
    print count
