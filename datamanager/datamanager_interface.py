from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def fetch_movie(self, movie):
        pass

    @abstractmethod
    def add_user(self, name):
        pass

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_movie(self, user_id, movie_title):
        pass

    @abstractmethod
    def get_movie(self, user_id, movie_id):
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, movie_title, director, year,
                     rating):
        pass
