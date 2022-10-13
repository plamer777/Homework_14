"""This is a main Flask app file"""
from flask import Flask
from app.main_blueprint.main_blueprint import movie_blueprint
from config.app_config import AppConfig
# ------------------------------------------------------------------------
app = Flask(__name__)

app.config.from_object(AppConfig)
app.register_blueprint(movie_blueprint)
# -------------------------------------------------------------------------


@app.errorhandler(404)
def error_404_page(status_code):
    """The 404-error handler

    :param status_code: An error number and description
    """
    print(status_code)
    return "К сожалению ничего найти не удалось"


@app.errorhandler(500)
def error_500_page(status_code):
    """The 500-error handler

    :param status_code: An error number and description
    """
    print(status_code)
    return "Возникла ошибка со стороны сервера"
# ------------------------------------------------------------------------


if __name__ == '__main__':
    app.run()
