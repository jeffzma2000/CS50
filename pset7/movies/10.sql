SELECT name FROM people, directors ON id = person_id WHERE movie_id = (SELECT id FROM movies, ratings ON id = movie_id WHERE rating >= 9.0);