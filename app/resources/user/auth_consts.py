from flask import current_app
# Client Keys
CLIENT_ID = current_app.config['CLIENT_ID']
CLIENT_SECRET = current_app.config['CLIENT_SECRET']
FERNET_KEY = b'NyklX3e5H0HV_2YPLGNBQGtAC17XmUh8QCyuDg70z5A='

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"


# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000

REDIRECT_URI = "{}:{}/callback".format(CLIENT_SIDE_URL, PORT)

# SCOPE
SCOPE = ("playlist-read-private"
         " playlist-read-collaborative"
         " user-library-modify"
         " playlist-modify-private"
         " playlist-modify-public"
         " user-read-email"
         " user-top-read"
         " user-read-recently-played"
         " user-read-private"
         " user-library-read"
         )

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "show_dialog": 'false',
    "client_id": CLIENT_ID
}

SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = f"{SPOTIFY_API_BASE_URL}/{API_VERSION}"
