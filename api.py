from flask import Blueprint, jsonify, request, make_response
from datamanager.sql_data_manager import SQLiteDataManager

# Create a data manager instance
api = Blueprint('api', __name__)
data_manager = SQLiteDataManager('data/movies.sqlite')


@api.route('/users', methods=['GET'])
def get_users():
    try:
        users = data_manager.get_all_users()
        return jsonify(users), 200
    except IOError as e:
        return jsonify({'error': str(e)}), 500


@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return jsonify(movies), 200


@api.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    try:
        movie_title = request.json.get('movie_title')
        print(movie_title)
        data_manager.add_movie(user_id, movie_title)
        return jsonify({'message': 'Movie added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
