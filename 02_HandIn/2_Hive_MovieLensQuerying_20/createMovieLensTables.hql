CREATE TABLE moviesV1 (movieID INT, title STRING, genres ARRAY<STRING>)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\""
)
STORED AS TEXTFILE;


CREATE TABLE tags (userID INT, movieID INT, tag STRING, datevalue BIGINT)
COMMENT 'Tag details'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;

CREATE TABLE ratings(userID INT, movieID INT, rating DOUBLE, datevalue BIGINT)
COMMENT 'Rating details'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;

CREATE TABLE genome_scores (movieID INT, tagID INT, relevance DOUBLE)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;
	
	
CREATE TABLE genome_tags(tagID INT, tag STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;
