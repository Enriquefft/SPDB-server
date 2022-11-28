from app.models.user import User

from flask_restful import Resource, abort, reqparse

from flask_jwt_extended import create_access_token

from string import ascii_lowercase, ascii_uppercase, digits


def isValidSize(password):
    MIN_SIZE = 8
    if len(password) < MIN_SIZE:
        return False
    return True


def hasSingleChar(password, charSet):
    for char in password:
        if char in charSet:
            return True
    return False


def isValidPassword(password):
    if not password:
        return False

    if not isValidSize(password):
        return False

    if not hasSingleChar(password, ascii_lowercase):
        return False

    if not hasSingleChar(password, ascii_uppercase):
        return False

    if not hasSingleChar(password, digits):
        return False

    return True


class register(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, nullable=False)
    parser.add_argument('password', required=True, nullable=False)

    def post(self):

        data = self.parser.parse_args(strict=True)
        user = User.query.filter_by(username=data.get('username')).scalar()

        if user is not None:
            abort(404, error='username already exists')

        # password validation
        if (data.get('password') == data.get('username')):
            abort(404, error='password cannot be username')

        if not isValidPassword(data.get('password')):
            abort(404, error='password is not valid')

        from werkzeug.security import generate_password_hash

        pass_hash = generate_password_hash(data.get('password', None))
        passFriends = User.query.filter_by(pass_hash=pass_hash).scalar()

        if passFriends is not None:
            abort(404, error='password already in use')

        new_user = User(data.get('username'), pass_hash)

        new_user = new_user.insert()

        if new_user is None:
            abort(404, error='user not created')

        user = User.query.filter_by(username=data.get('username')).scalar()

        response = {
            'username': user.username,
            'access_token': create_access_token(user)
        }

        if not user.has_authorized():
            response['notAuthorized'] = True

        return response, 200
