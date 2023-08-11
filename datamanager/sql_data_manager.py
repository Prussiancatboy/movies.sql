import sqlite3
import requests
from .datamanager_interface import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def fetch_data(self):
        """Fetches data from the database"""
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies")
        data = cursor.fetchall()
        conn.close()
        return data

    def save_data(self, movie_database):
        """Saves the data to the database"""
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies")
        cursor.executemany("INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?, ?)",
                           movie_database)
        conn.commit()
        conn.close()

    def fetch_movie(self, movie):
        """Fetches movie details from the OMDB API"""
        name = movie
        res = requests.get(
            f'https://www.omdbapi.com/?t={name}&apikey=1e3e73a4')
        if res.status_code != 200:
            return "Server error"
        else:
            movie = res.json()
            if movie['Response'] == "False":
                return None
            else:
                return movie

    def add_user(self, name):
        """Add a user to the database"""
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()

    def get_all_users(self):
        """Get a list of all users with movie details"""
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        all_users = []
        for user in users:
            user_dict = {'id': user[0], 'name': user[1], 'movies': []}
            cursor.execute("SELECT * FROM movies WHERE user_id = ?",
                           (user[0],))
            movies = cursor.fetchall()
            for movie in movies:
                movie_dict = {
                    'id': movie[0],
                    'name': movie[2],
                    'director': movie[3],
                    'year': movie[4],
                    'rating': movie[5],
                    'poster': movie[6]
                }
                user_dict['movies'].append(movie_dict)
            all_users.append(user_dict)

        conn.close()
        return all_users

    def get_user_movies(self, user_id):
        """Get a user's movie list"""
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE user_id = ?", (user_id,))
        movies = cursor.fetchall()
        conn.close()

        user_movies = []
        for movie in movies:
            movie_dict = {
                'id': movie[0],
                'name': movie[2],
                'director': movie[3],
                'year': movie[4],
                'rating': movie[5],
                'poster': movie[6]
            }
            user_movies.append(movie_dict)

        return user_movies

    def add_movie(self, user_id, movie_title):
        """Add a movie to the database"""
        # Fetch movie details
        movie_data = self.fetch_movie(movie_title)

        if movie_data is not None:
            conn = sqlite3.connect(self.db_filename)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO movies "
                "(user_id, name, director, year, rating, poster) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, movie_data['Title'], movie_data['Director'],
                 movie_data['Year'], movie_data['imdbRating'],
                 movie_data['Poster']))
            conn.commit()
            conn.close()
            return "Movie added successfully!"
        else:
            return "Movie not found or server error"

    def get_movie(self, user_id, movie_id):
        """Get a specific movie from a user's list"""
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE user_id = ? AND id = ?",
                       (user_id, movie_id))
        movie = cursor.fetchone()
        conn.close()

        if movie:
            movie_dict = {
                'id': movie[0],
                'name': movie[2],
                'director': movie[3],
                'year': movie[4],
                'rating': movie[5],
                'poster': movie[6]
            }
            return movie_dict
        else:
            return None

    def update_movie(self, user_id, movie_id, movie_title, director, year,
                     rating):
        """Update movie details in the database"""
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE movies SET name = ?, director = ?, "
            "year = ?, rating = ? WHERE user_id = ? AND id = ?",
            (movie_title, director, year, rating, user_id, movie_id))
        conn.commit()

        # Fetch updated movie details
        cursor.execute("SELECT * FROM movies WHERE user_id = ? AND id = ?",
                       (user_id, movie_id))
        updated_movie = cursor.fetchone()

        conn.close()

        if updated_movie:
            updated_movie_dict = {
                'id': updated_movie[0],
                'name': updated_movie[2],
                'director': updated_movie[3],
                'year': updated_movie[4],
                'rating': updated_movie[5],
                'poster': updated_movie[6]
            }
            return updated_movie_dict
        else:
            return None

    def delete_movie(self, user_id, movie_id):
        """Delete a movie from a user's list"""
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE user_id = ? AND id = ?",
                       (user_id, movie_id))
        conn.commit()
        conn.close()
