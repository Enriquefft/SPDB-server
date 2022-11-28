# Flask utils
from flask import Flask


def create_app(config_class='Dev'):

    verifyConfClass(config_class)

    # Jinja inline comments
    Flask.jinja_options = {'line_comment_prefix': '##'}
    app = Flask(__name__)

    app.config.from_object(f'app.Config.{config_class}Config')

    from app.models import db
    db.init_app(app)

    # CREATE TABLES
    #from app.models import user, tables
    # with app.app_context():
    #    db.create_all()

    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)

    from flask_cors import CORS
    CORS(app)

    # Blueprints
    from app.resources.blueprints import user_bp, home_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(home_bp)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        from app.models.user import User
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    return app


# Move to utils.py?
def verifyConfClass(config_class):
    options = ['Dev', 'Prod']
    if config_class not in options:

        from click import BadParameter
        from sys import exit

        BadParameter(
            f"\n'{config_class}' config setup not available.\nAvailable options are:\n{[x for x in options]}").show()
        exit()
