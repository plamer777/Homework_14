"""This is a main blueprint processes all requests"""
from flask import Blueprint, jsonify, abort
from dao.movies_dao import MovieDao
from config.config import DB_FILE, RATINGS
# --------------------------------------------------------------------------
# creating blueprint and DAO instances
movie_blueprint = Blueprint('movie_blueprint', __name__)
movie_dao = MovieDao(DB_FILE)
# --------------------------------------------------------------------------


@movie_blueprint.route('/movie/<title>/')
def movie_by_title(title):
    """This view returns all movies found by provided title"""
    found_movies = movie_dao.find_by_title(title)

    if not found_movies:
        abort(404)

    return jsonify(found_movies)


@movie_blueprint.route('/movie/<int:start_year>/to/<int:end_year>/')
def found_by_years(start_year: int, end_year: int):
    """The view returns movies found by a provided range of years"""
    found_movies = movie_dao.find_by_years(start_year, end_year)

    if not found_movies:
        abort(404)

    return jsonify(found_movies)


@movie_blueprint.route('/rating/<movie_rating>/')
def found_by_rating(movie_rating: str):
    """This view returns movies found by a rating"""
    rating = RATINGS.get(movie_rating)

    if rating:

        found_movies = movie_dao.find_by_rating(rating)

        if not found_movies:
            abort(404)

        return jsonify(found_movies)

    abort(404)


@movie_blueprint.route('/genre/<genre>/')
def found_by_genre(genre: str):
    """This view returns all movies found by provided genre"""
    found_movies = movie_dao.find_by_genre(genre)

    if not found_movies:
        abort(404)

    return jsonify(found_movies)
