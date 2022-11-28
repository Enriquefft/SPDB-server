try:
    from Constants import CLIENT_ID, CLIENT_SECRET, SECRET_KEY, JWT_SECRET_KEY, FERNET_KEY
except ImportError as error:
    from sys import exit
    print(error)
    exit("Please, ensure you have a Constants.py file with the CLIENT_ID, CLIENT_SECRET And INIT_URI variables.")


class BaseConfig:

    # Base config
    CLIENT_ID = CLIENT_ID
    CLIENT_SECRET = CLIENT_SECRET
    SECRET_KEY = SECRET_KEY
    BUNDLE_ERRORS = True  # error handling as bundle
    JWT_SECRET_KEY = JWT_SECRET_KEY
    FERNET_KEY = FERNET_KEY

    #CORS_HEADERS = "Content-Type"


class ProdConfig(BaseConfig):
    from Constants import PROD_URI
    SQLALCHEMY_DATABASE_URI = PROD_URI


class DevConfig(BaseConfig):
    from Constants import DEV_URI
    SQLALCHEMY_DATABASE_URI = DEV_URI
    #EXPLAIN_TEMPLATE_LOADING = True
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_ECHO = True
