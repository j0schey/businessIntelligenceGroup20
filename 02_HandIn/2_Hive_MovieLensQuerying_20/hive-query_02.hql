SELECT COUNT(m.movieID) FROM movies m
LATERAL VIEW EXPLODE(m.genres) individualGenre
WHERE individualGenre.col = 'Horror';