LOAD DATA INPATH 's3://hivestore/mldataset/genome-tags.csv' INTO TABLE genome_tags;
LOAD DATA INPATH 's3://hivestore/mldataset/genome-scores.csv' INTO TABLE genome_scores;
LOAD DATA INPATH 's3://hivestore/mldataset/ratings2.csv' INTO TABLE ratings
LOAD DATA INPATH 's3://hivestore/mldataset/tags.csv' INTO TABLE tags;
LOAD DATA INPATH 's3://hivestore/mldataset/movies.csv' INTO TABLE moviesV1;
CREATE VIEW movies AS SELECT CAST (movieID as INT), title, split(genres, '\\|') as genres FROM moviesV1;


