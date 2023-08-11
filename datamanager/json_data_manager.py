import json
import requests
from .datamanager_interface import DataManagerInterface


class JsonDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def fetch_data(self):
        """This fetches data"""
        with open(self.filename) as fileobj:
            movie_database = json.load(fileobj)
            return movie_database

    def save_data(self, movie_database):
        """This saves the data"""
        with open(self.filename, 'w') as fileobj:
            json.dump(movie_database, fileobj)

    def fetch_movie(self, movie):
        """This tries to fetch the movie,
        if it fails it should return None or a server error"""
        name = movie
        res = requests.get(
            f'https://www.omdbapi.com/?t={name}&apikey=1e3e73a4')
        # store the response of URL

        if res.status_code != 200:
            return "Server error"
        else:
            movie = res.json()
            if movie['Response'] == "False":
                return None
            else:
                return movie

    def add_user(self, name):
        """This code will add a user to the database"""
        username = name

        new_user = {
            'id': len(self.fetch_data()) + 1,
            'name': username,
            'movies': []
        }

        movie_database = self.fetch_data()
        movie_database.append(new_user)
        self.save_data(movie_database)

        return "User added successfully!"

    def get_all_users(self):
        """This will return a list of all users"""
        # This gets the data
        data = self.fetch_data()

        # This will hold the list of users
        user_list = []

        for user in data:
            user_list.append(user)
        return user_list

    def get_user_movies(self, user_id):
        """This uses the user_id to return their perspective list """

        # this fetches the data
        data = self.fetch_data()

        # this deals with the counter
        counter = 0

        # this code searches for the user,
        # and returns either the dictionary or the error message
        for dct in data:
            counter += 1
            if dct['id'] == user_id:
                return dct['movies']

            # This code returns an error message
            # if the user is not in database
            elif counter == len(data):
                return f"User {user_id} is not in the database"

    def add_movie(self, user_id, movie_title):
        """Add a movie to the given database"""
        movie_data = self.fetch_movie(movie_title)
        database = self.fetch_data()
        user_movies = None

        # Find the user in the database
        for user in database:
            if user['id'] == user_id:
                user_movies = user['movies']
                break

        # If the user is found, add the movie to their movies list
        if user_movies is not None:

            # this code prevents N/A in the rating, from crashing everything
            try:
                movie_rating = float(movie_data['imdbRating'])

            except ValueError:
                movie_rating = movie_data['imdbRating']

            # this code prevents N/A in the year, from crashing everything
            try:
                movie_year = int(movie_data['Year'])

            except ValueError:
                movie_year = movie_data['Year']

            movie = {
                'id': len(user_movies) + 1,
                'name': movie_data['Title'],
                'director': movie_data['Director'],
                'year': movie_year,
                'rating': movie_rating,
                'poster': movie_data['Poster']
            }
            user_movies.append(movie)

            # Save the updated database
            self.save_data(database)

            return "Movie added successfully!"
        else:
            return "User not found in the database!"

    def get_movie(self, user_id, movie_id):
        """This retrieves a specific movie from a user's list"""
        movies = self.get_user_movies(user_id)

        for movie in movies:
            if movie['id'] == movie_id:
                return movie

        return None

    def update_movie(self, user_id, movie_id, movie_title, director, year,
                     rating):
        """This updates the details of a movie in the database"""
        movie_database = self.fetch_data()

        for user in movie_database:
            if user['id'] == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        movie['name'] = movie_title
                        movie['director'] = director
                        movie['year'] = year
                        movie['rating'] = rating
                        break

        self.save_data(movie_database)

    def delete_movie(self, user_id, movie_id):
        """Delete the selected movie
        from the user's list of favorite movies"""
        movie_database = self.fetch_data()

        for user in movie_database:
            if user['id'] == user_id:
                movies = user['movies']
                for movie in movies:
                    if movie['id'] == movie_id:
                        movies.remove(movie)
                        break

        self.save_data(movie_database)
