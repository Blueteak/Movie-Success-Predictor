#Install dependencies for IMDbPY package
conda install lxml

#Install IMDbPY
easy_install IMDbPY

#create postgres database
create db imdb_project

#Download IMDB dataset text files from official IMDB website
wget -c -P . ftp://ftp.fu-berlin.de/pub/misc/movies/database/*.list.gz

#Create folder for csv files
mkdir csv_files

#import IMDB data in database
imdbpy2sql.py -d . -u postgres:imdb_project -c csv_files

#login to the database 
psql imdb_project

#create table to create dataset with movie features required for machine learning
CREATE TABLE IF NOT EXISTS movie_info_proj (
    movie_id integer,
    title text,
    country text,
    budget text,
    weekend_gross text,
    gross text
    );
    
#Insert the records of type 'movie'(kind_type='movie') with contry information in the new dataset
#by joining 'title' and 'movie_info' tables on 'movie_id'
INSERT INTO movie_info_proj(movie_id,title,country) 
(SELECT 
title.id,
title.title,
movie_info.info
FROM
title, movie_info
WHERE 
title.id = movie_info.movie_id
and title.kind_id=1
and movie_info.info_type_id=8
);

#Keep records for 'USA' only
DELETE FROM movie_info_proj WHERE country <> 'USA';

#Update movie info with budget,gross,weekend_gross
 id  |              info
 -----+---------------------------------
  3 | genres
  8 | countries
  16 | release dates
  97 | mpaa
  100 | votes
  101 | rating
  105 | budget
  107 | gross
  108 | opening weekend
  
UPDATE movie_info_proj
	SET budget=movie_info.info
	FROM (
	  SELECT
	  movie_info.movie_id,
	  movie_info.info
	  FROM
	  movie_info, movie_info_proj
	  WHERE
	  movie_info_proj.movie_id = movie_info.movie_id
	  and movie_info.info_type_id=105
	  )AS movie_info
	  WHERE movie_info_proj.movie_id = movie_info.movie_id;
  
UPDATE movie_info_proj
	SET gross=movie_info.info
	FROM (
	  SELECT
	  movie_info.movie_id,
	  movie_info.info
	  FROM
	  movie_info, movie_info_proj
	  WHERE
	  movie_info_proj.movie_id = movie_info.movie_id
	  and movie_info.info_type_id=107
	  )AS movie_info
	  WHERE movie_info_proj.movie_id = movie_info.movie_id;
    
UPDATE movie_info_proj
	 SET weekend_gross=movie_info.info
	 FROM (
	   SELECT
	   movie_info.movie_id,
	   movie_info.info
	   FROM
	   movie_info, movie_info_proj
	   WHERE
	   movie_info_proj.movie_id = movie_info.movie_id
	   and movie_info.info_type_id=106
	   )AS movie_info
	 WHERE movie_info_proj.movie_id = movie_info.movie_id;
    
