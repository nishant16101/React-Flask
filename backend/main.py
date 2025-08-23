from flask import Flask
from flask_restx import Api,Resource
from config import DevConfig
from models import Recipe
from exts import db

app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app,doc='/docs ')

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {"message":"Hello, World!"}

if __name__ == '__main__':
    app.run(debug=True)