"""This unit contains a test class for testing dao class' methods"""
import pytest
from dao.movies_dao import MovieDao
from config.config import DB_FILE, RATINGS
from config.testing_config import TEST_TITLE_KEYS, TEST_YEARS_KEYS, \
    TEST_RATING_KEYS, TEST_GENRE_KEYS
# ------------------------------------------------------------------------


@pytest.fixture()
def movies_dao_test():
    """The fixture for testing

    return:
        movie_dao - an instance of MovieDao class
    """
    movie_dao = MovieDao(DB_FILE)

    return movie_dao
# -------------------------------------------------------------------------


class TestMoviesDao:
    """TestMoviesDao is a class for testing MovieDao class methods"""

    def test_find_by_title(self, movies_dao_test):
        """This method serves to test find_by_title method of MovieDao

        :param movies_dao_test: a fixture with MovieDao instance
        """
        found_movies = movies_dao_test.find_by_title('100')

        assert len(found_movies) != 0, 'Данные не получены'
        assert type(found_movies) == dict, 'Неверный тип данных'
        assert set(found_movies.keys()) == TEST_TITLE_KEYS, 'Неверные ключи'

    def test_find_by_years(self, movies_dao_test):
        """This method tests find_by_years method of MovieDao

        :param movies_dao_test: a fixture with MovieDao instance
        """
        found_movies = movies_dao_test.find_by_years(2010, 2015)

        assert len(found_movies) != 0, 'Список пуст'
        assert type(found_movies) == list, 'Неверный тип данных'
        assert set(found_movies[0]) == TEST_YEARS_KEYS, 'Неверные ключи'

    def test_find_by_rating(self, movies_dao_test):
        """This method serves to test find_by_rating method of MovieDao

        :param movies_dao_test: a fixture with MovieDao instance
        """
        found_movies = movies_dao_test.find_by_rating(RATINGS['adult'])

        assert len(found_movies) != 0, 'Список пуст'
        assert type(found_movies) == list, 'Неверный тип данных'
        assert set(found_movies[0]) == TEST_RATING_KEYS, 'Неверные ключи'

    def test_find_by_genre(self, movies_dao_test):
        """This method tests find_by_genre method of MovieDao

        :param movies_dao_test: a fixture with MovieDao instance
        """
        found_movies = movies_dao_test.find_by_genre('comedies')

        assert len(found_movies) != 0, 'Список пуст'
        assert type(found_movies) == list, 'Неверный тип данных'
        assert set(found_movies[0]) == TEST_GENRE_KEYS, 'Неверные ключи'

    def test_find_actors_partners(self, movies_dao_test):
        """This method serves to test find_actors_partners method of MovieDao

        :param movies_dao_test: a fixture with MovieDao instance
        """
        found_actors = movies_dao_test.find_actors_partners('Rose McIver',
                                                            'Ben Lamb')

        assert len(found_actors) == 2, 'Проверьте кол-во найденных актеров'
        assert type(found_actors) == list, 'Неверный тип данных'
        assert type(found_actors[0]) == str, 'Неверный тип данных в списке'

    def test_find_by_type_year_genre(self, movies_dao_test):
        """This method serves to test find_by_type_year_genre method of
        MovieDao

        :param movies_dao_test: a fixture with MovieDao instance
        """
        found_movies = movies_dao_test.find_by_type_year_genre('Movie',
                                                               2010,
                                                               'comedies')

        assert len(found_movies) != 0, 'Список пуст'
        assert type(found_movies) == list, 'Неверный тип данных'
        assert set(found_movies[0]) == TEST_GENRE_KEYS, 'Неверные ключи'

    def test_db_error(self):
        """This method tests the behavior of MovieDao class if a file is not
        found"""
        # creating an instance with a wrong database's filename
        movie_dao = MovieDao('error.db')

        found_movies = movie_dao.find_by_title('100')

        assert len(found_movies) == 0
        assert type(found_movies) == list
