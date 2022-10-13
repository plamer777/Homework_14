"""This unit contains TestMainBlueprint for testing main blueprint of Flask
app"""
import pytest
from flask.testing import FlaskClient
from run import app
from config.testing_config import TEST_TITLE_KEYS, TEST_YEARS_KEYS, \
    TEST_RATING_KEYS, TEST_GENRE_KEYS
# ------------------------------------------------------------------------


@pytest.fixture()
def test_app() -> FlaskClient:
    """This fixture returns a test client of Flask app

    return:
        test_app_client - a Flask's test client
    """
    test_app_client = app.test_client()

    return test_app_client
# ------------------------------------------------------------------------


class TestMainBlueprint:
    """This class contains all necessary methods for testing main blueprint"""

    def test_movie_by_title_view(self, test_app: FlaskClient) -> None:
        """This method tests movie_by_title view of main blueprint

        :param test_app: a Flask's test client
        """
        # creating a request object with json data
        request = test_app.get('/movie/100/', follow_redirects=True)
        json_data = request.json

        assert request.status_code == 200, 'Ответ сервера не ОК'
        assert type(json_data) == dict, 'Неверный тип данных'
        assert len(json_data) != 0, 'Словарь данных пуст'
        assert set(json_data) == TEST_TITLE_KEYS, 'Неверные ключи'

        # checking app's behavior when a route is wrong
        request = test_app.get('/movie/abcde/', follow_redirects=True)

        assert request.text == 'К сожалению ничего найти не удалось', \
                               'Вьюшка не выбрасывает ошибку 404'

    def test_found_by_years_view(self, test_app: FlaskClient) -> None:
        """This method tests found_by_years view of main blueprint

        :param test_app: a Flask's test client
        """
        request = test_app.get('/movie/2010/to/2015/', follow_redirects=True)

        # using a universal method to test all necessary parameters
        self._check_data(request, TEST_YEARS_KEYS)

        request = test_app.get('/movie/20/to/1000/', follow_redirects = True)

        assert request.text == 'К сожалению ничего найти не удалось', \
            'Вьюшка не выбрасывает ошибку 404'

    @staticmethod
    def _check_data(request, keys: set) -> None:
        """This method contains a test logic using in different test methods

        :param request: a request object
        :param keys: a set of keys using to compare with dict keys received
        from json
        """
        json_data = request.json

        assert request.status_code == 200, 'Ответ сервера не ОК'
        assert type(json_data) == list, 'Неверный тип данных'
        assert len(json_data) != 0, 'Словарь данных пуст'

        # checking keys and types of all dicts in list
        for movie in json_data:

            assert type(movie) == dict, "Неверный тип вложенных данных"
            assert set(movie) == keys, 'Неверные ключи'

    def test_found_by_rating_view(self, test_app: FlaskClient) -> None:
        """This method tests found_by_rating view of main blueprint

        :param test_app: a Flask's test client
        """
        request = test_app.get('/rating/adult/', follow_redirects=True)

        self._check_data(request, TEST_RATING_KEYS)

        request = test_app.get('/rating/wrong_rating/', follow_redirects=True)

        assert request.text == 'К сожалению ничего найти не удалось', \
            'Вьюшка не выбрасывает ошибку 404'

    def test_found_by_genre_view(self, test_app: FlaskClient) -> None:
        """This method tests found_by_genre view of main blueprint

        :param test_app: a Flask's test client
        """
        request = test_app.get('/genre/comedies/', follow_redirects=True)

        self._check_data(request, TEST_GENRE_KEYS)

        request = test_app.get('/genre/wrong_genre', follow_redirects=True)

        assert request.text == 'К сожалению ничего найти не удалось', \
            'Вьюшка не выбрасывает ошибку 404'
