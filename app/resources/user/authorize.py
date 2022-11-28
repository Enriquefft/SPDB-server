from flask_restful import Resource, abort, reqparse

from flask_jwt_extended import jwt_required

from cryptography.fernet import Fernet

FERNET_KEY = b'NyklX3e5H0HV_2YPLGNBQGtAC17XmUh8QCyuDg70z5A='
fernet = Fernet(FERNET_KEY)

STATE = ""


def GenerateState(user_id):
    from string import ascii_letters, digits
    from random import choice
    chars = ascii_letters + digits
    state = ''.join(choice(chars) for _ in range(8)) + " " + user_id
    return fernet.encrypt(state.encode()).decode()


class authorize(Resource):

    @jwt_required()
    def get(self):

        from flask_jwt_extended import current_user

        if (current_user.has_authorized()):
            abort(403, message="User has already authorized")

        global STATE
        STATE = GenerateState(str(current_user.id))

        from .auth_consts import auth_query_parameters, SPOTIFY_AUTH_URL
        auth_query_parameters["state"] = STATE

        from urllib.parse import urlencode
        url_args = urlencode(auth_query_parameters)

        auth_url = f"{SPOTIFY_AUTH_URL}/?{url_args}"

        return {"redirect": auth_url}, 200


class callback(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('state', required=True,
                        nullable=False, location='args')
    parser.add_argument('code', required=True, nullable=False, location='args')

    def get(self):

        data = self.parser.parse_args()

        if data.get('state') != STATE:
            abort(400, message="Invalid state")
        if data.get('error') is not None:
            abort(400, message=data.get('error'))

        code = data.get('code')

        from .auth_consts import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SPOTIFY_TOKEN_URL
        from base64 import b64encode
        from requests import post

        body = {
            'grant_type': 'authorization_code',
            'code': str(code),
            'redirect_uri': REDIRECT_URI,
        }

        headers = {
            'Authorization': f"Basic {b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}",
            'content-type': 'application/x-www-form-urlencoded'
        }

        post_request = post(SPOTIFY_TOKEN_URL, data=body, headers=headers)

        if (post_request.status_code != 200):
            abort(400, message="Invalid code")

        auth_data = post_request.json()

        from .auth_consts import SPOTIFY_API_URL
        from requests import get

        token = auth_data.get('access_token')

        from json import dumps
        print(dumps(auth_data, indent=4))

        # Get current user info
        headers = {
            'Authorization': f"Bearer {token}"
        }
        profile_request = get(f"{SPOTIFY_API_URL}/me", headers=headers)

        if (profile_request.status_code != 200):
            abort(400, message="Invalid token")

        profile_data = profile_request.json()

        state = fernet.decrypt(STATE.encode()).decode()
        user_id = state.split(" ")[1]

        from app.models.user import User
        user = User.query.get(user_id)

        user.sp_id = profile_data.get('id')
        user.sp_uri = profile_data.get('uri')
        user.sp_username = profile_data.get('display_name')
        user.email = profile_data.get('email')
        user.refresh_token = auth_data.get('refresh_token')

        print(user.update())

        from flask import redirect
        return redirect("http://localhost:5173/login")
