try:
    from Constants import CLIENT_ID, CLIENT_SECRET, DEV_URI, PROD_URI, SECRET_KEY, JWT_SECRET_KEY
except ImportError:
    from sys import exit
    exit("Please, ensure you have a Constants.py file with the CLIENT_ID, CLIENT_SECRET And INIT_URI variables.")


class BaseConfig:

    # Base config
    CLIENT_ID = CLIENT_ID
    CLIENT_SECRET = CLIENT_SECRET
    SECRET_KEY = SECRET_KEY
    BUNDLE_ERRORS = True  # error handling as bundle
    JWT_SECRET_KEY = JWT_SECRET_KEY

    #CORS_HEADERS = "Content-Type"


class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = PROD_URI


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DEV_URI
    #EXPLAIN_TEMPLATE_LOADING = True
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_ECHO = True
