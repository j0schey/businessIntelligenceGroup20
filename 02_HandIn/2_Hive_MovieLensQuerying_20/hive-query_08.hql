CREATE VIEW dramaMovies AS SELECT movieID, title FROM movies m
LATERAL VIEW EXPLODE(m.genres) individualGenre
WHERE individualGenre.col = 'Drama';
SELECT title, count(rating) AS noRatings FROM dramaMovies dm INNER JOIN ratings r ON dm.movieID = r.movieID WHERE rating=5.0 GROUP BY title HAVING(count(rating)>10) ORDER BY noRatings DESC LIMIT 10;
