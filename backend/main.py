from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import DevConfig
from model import Recipe, User
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
from recipes import recipe_ns
from auth import auth_ns





def create_app(config):
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    db.init_app(app)
    migrate = Migrate(app, db)
    JWTManager(app)
    api = Api(app, doc='/docs')
    api.add_namespace(recipe_ns)
    api.add_namespace(auth_ns)
    


    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Recipe': Recipe, 'User': User}
    return app



if __name__ == '__main__':
    app.run(debug=True)
