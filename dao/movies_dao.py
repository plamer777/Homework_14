"""This unit contains MovieDao class allows to work with a database with
movies from Netflix"""
import sqlite3
from config.config import FIND_BY_TITLE_KEYS, FIND_BY_YEARS_KEYS, \
    FIND_BY_RATING_KEYS, FIND_BY_GENRE_KEYS
# --------------------------------------------------------------------------


class MovieDao:
    """MovieDao class with all necessary logic to work with a database"""

    def __init__(self, db_filename: str):
        """Initialization method serves to store database filename"""
        self._db_filename = db_filename

    def find_by_title(self, movie_title: str) -> dict:
        """This method finds movies by title

        :param movie_title: a movie's title to search in database

        return:
            movie_dict - a dict with found movie data
        """
        query = f"""
                SELECT title, country, release_year, 
                listed_in, description
                FROM netflix
                WHERE title LIKE '%{movie_title}%'
                ORDER BY release_year DESC
                LIMIT 1
                """
        # getting movie's data from database
        found_movie = self._get_from_db(query)

        if not found_movie:
            return found_movie

        # creating a dict based on found data
        movie_dict = self._create_dict(FIND_BY_TITLE_KEYS, found_movie[0])

        return movie_dict

    def _get_from_db(self, query: str) -> list:
        """A closed method returns data for database by provided
        query string

        :param query: a database request string

        return:
            result - a list of tuples with found data
        """
        try:
            with sqlite3.connect(self._db_filename) as connect:

                cursor = connect.cursor()

                cursor.execute(query)

                result = cursor.fetchall()

            return result

        except sqlite3.Error as db_error:

            print(f'Не удалось загрузить данные из базы данных\n{db_error}')
            return []

    @staticmethod
    def _create_dict(keys: str, movie_data: tuple) -> dict:
        """This method serves to create a dict by provided tuple with
        single movie data

        :param keys: a string of keys separated by spaces
        :param movie_data: a tuple with movie data

        return:
            movie_dict - a created dict based on provided keys and movie data
        """
        keys_list = keys.split(' ')
        movie_dict = {key: value for key, value in zip(keys_list, movie_data)}

        return movie_dict

    def _create_list_of_dicts(self, keys: str, movies: list) -> list:
        """This method works like _create_dict but this one creates
        a list of dicts with movies data

        :param keys: a string of keys separated by spaces
        :param movies: a list of tuples with movies data

        return:
            movie_list - a list of dicts
        """
        movie_list = []

        for movie in movies:

            movie_dict = self._create_dict(keys, movie)

            movie_list.append(movie_dict)

        return movie_list

    def find_by_years(self, start_year: int, end_year: int) -> list:
        """This method searches movies released between provided years

        :param start_year: a year to start with
        :param end_year: a year to search until

        return:
            list_of_movies - a list of dicts with found movies data
        """
        query = f"""
                    SELECT title, release_year
                    FROM netflix
                    WHERE release_year BETWEEN {start_year} AND {end_year}
                    LIMIT 100              
                """

        found_movies = self._get_from_db(query)
        list_of_movies = self._create_list_of_dicts(FIND_BY_YEARS_KEYS,
                                                    found_movies)

        return list_of_movies

    def find_by_rating(self, movies_rating: list) -> list:
        """The method to find movies my provided rating

        :param movies_rating: the rating by which the search is performed

        return:
            movies_list - a list of dicts with found data
        """
        # turning list into tuple because of error in query otherwise
        movies_rating = tuple(movies_rating)

        query = f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN {movies_rating}                    
                """

        found_movies = self._get_from_db(query)
        movies_list = self._create_list_of_dicts(FIND_BY_RATING_KEYS,
                                                 found_movies)

        return movies_list

    def find_by_genre(self, genre: str) -> list:
        """This method searches movies by provided genre

        :param genre: a searched genre to search movies

        return:
            movies_list - a list of dicts with found movies data
        """
        query = f"""
                SELECT title, description
                FROM netflix
                WHERE listed_in LIKE '%{genre}%'
                ORDER BY release_year DESC
                LIMIT 10                   
                """

        found_movies = self._get_from_db(query)
        movies_list = self._create_list_of_dicts(FIND_BY_GENRE_KEYS,
                                                 found_movies)

        return movies_list

    def find_actors_partners(self, first_actor: str, second_actor: str):
        """This method serves to find all actors worked together with
        provided ones more than two times

        :param first_actor: a full name of first actor
        :param second_actor: a full name of second actor

        return:
            a list with found actors names
        """
        query = f"""
                SELECT "cast"
                FROM netflix
                WHERE  "cast" LIKE '%{first_actor}%' 
                AND "cast" LIKE '%{second_actor}%'                
                GROUP BY "cast"
                """
        # getting all found actors
        found_partners = self._get_from_db(query)

        partners_list = []

        # creating a single list with all found actors
        for group in found_partners:

            group = list(group)[0].split(', ')

            partners_list.extend(group)

        # creating a dict with actors and a count how often they worked
        # together with searched actors
        partners_count = {partner: partners_list.count(partner)
                          for partner in partners_list if partner not in
                          [first_actor, second_actor] and
                          partners_list.count(partner) > 2}

        return list(partners_count.keys())

    def find_by_type_year_genre(self, movie_type: str, year: int, genre: str):
        """This method returns all movies found by type, year and genre

        :param movie_type: a searched movies' type
        :param year: a searched movies' year
        :param genre: a searched movies' genre

        return:
            movies_list - a list of dicts with found movies data
        """
        query = f"""
                        SELECT title, description
                        FROM netflix
                        WHERE listed_in LIKE '%{genre}%'
                        AND release_year = {year}
                        AND type LIKE '%{movie_type}%'                                           
                        """

        found_movies = self._get_from_db(query)
        movies_list = self._create_list_of_dicts(FIND_BY_GENRE_KEYS,
                                                 found_movies)

        return movies_list
