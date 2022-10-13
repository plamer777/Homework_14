"""This unit contains constants for Dao and the main blueprint"""
FIND_BY_TITLE_KEYS = "title country release_year genre description"
FIND_BY_YEARS_KEYS = "title release_year"
FIND_BY_RATING_KEYS = "title rating description"
FIND_BY_GENRE_KEYS = "title description"

DB_FILE = "netflix.db"

RATINGS = {
    "children": ['TV-G'],
    "family": ['TV-G', 'TV-PG', 'PG-13'],
    "adult": ['R', 'NC-17']
}
