from flask import Flask, render_template, request, redirect, url_for
from datamanager.sql_data_manager import SQLiteDataManager
from api import api  # Importing the API blueprint

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')


class FrontendApp:
    """This class handles the front end"""

    def __init__(self):
        """This code initializes everything"""
        self.data_manager = SQLiteDataManager('data/movies.sqlite')
        self.setup_routes()
        self.setup_error_handlers()

    def setup_routes(self):
        """This code sets up routes"""
        app.add_url_rule('/', 'home', self.home, methods=['GET'])
        app.add_url_rule('/users', 'list_users', self.list_users,
                         methods=['GET'])
        app.add_url_rule('/users/<int:user_id>', 'user_movies',
                         self.user_movies, methods=['GET'])
        app.add_url_rule('/add_user', 'add_user', self.add_user,
                         methods=['GET', 'POST'])
        app.add_url_rule('/users/<int:user_id>/add_movie', 'add_movie',
                         self.add_movie, methods=['GET', 'POST'])
        app.add_url_rule('/users/<int:user_id>/update_movie/<int:movie_id>',
                         'update_movie', self.update_movie,
                         methods=['GET', 'POST'])
        app.add_url_rule('/users/<int:user_id>/delete_movie/<int:movie_id>',
                         'delete_movie', self.delete_movie, methods=['GET'])

    def setup_error_handlers(self):
        @app.errorhandler(404)
        def page_not_found(e):
            return render_template('404.html'), 404

    def home(self):
        """This code just handles the front end"""
        return render_template('home.html')

    def list_users(self):
        """This code calls the get all users code,
        and sends it out as a list"""
        try:
            users = self.data_manager.get_all_users()
        except IOError as e:
            print("An IOError occurred: ", str(e))
        return render_template('users.html', users=users)

    def user_movies(self, user_id):
        """This code displays the movies"""
        movies = self.data_manager.get_user_movies(user_id)
        return render_template('movies.html', movies=movies, user_id=user_id)

    def add_user(self):
        """This code handles the front end of adding a user"""
        if request.method == 'POST':
            username = request.form.get('username')
            self.data_manager.add_user(username)
            return redirect(url_for('list_users'))
        return render_template('add_user.html')

    def add_movie(self, user_id):
        """This code handles the front end of adding a user"""
        if request.method == 'POST':
            movie_title = request.form.get('movie_title')
            self.data_manager.add_movie(user_id, movie_title)
            return redirect(url_for('user_movies', user_id=user_id))
        return render_template('add_movie.html', user_id=user_id)

    def update_movie(self, user_id, movie_id):
        """This code handles the front end of updating a movie"""
        movie = self.data_manager.get_movie(user_id, movie_id)
        if movie is not None:
            if request.method == 'POST':
                movie_title = request.form.get('movie_title')
                director = request.form.get('director')
                year = int(request.form.get('year'))
                rating = float(request.form.get('rating'))
                self.data_manager.update_movie(user_id, movie_id, movie_title,
                                               director, year, rating)
                return redirect(url_for('user_movies', user_id=user_id))
            return render_template('update_movie.html', user_id=user_id,
                                   movie_id=movie_id, movie=movie)
        return "Movie not found!"

    def delete_movie(self, user_id, movie_id):
        """This code handles the front end of deleting a movie"""
        self.data_manager.delete_movie(user_id, movie_id)
        return redirect(url_for('user_movies', user_id=user_id))

    def run(self):
        """This starts the server"""
        app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == '__main__':
    my_app = FrontendApp()
    my_app.run()
