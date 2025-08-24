from flask import Flask,request,jsonify
from flask_restx import Api,Resource,fields
from config import DevConfig
from model import Recipe
from exts import db
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

migrate = Migrate(app,db )

api = Api(app,doc='/docs ')
with app.app_context():
    db.create_all()


#model serilaizer
recipe_model = api.model("Recipe",{
    "id":fields.Integer(),
    "title":fields.String(),
    "description":fields.String(),
})

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {"message":"Hello, World!"}

@api.route('/recipes')
class RecipeResource(Resource):
    @api.marshal_with(recipe_model)
    def get(self):
        recipes = Recipe.query.all()
        return recipes
    
    @api.marshal_with(recipe_model)
    def post(self):
        data = request.json
        new_recipe = Recipe(title=data['title'], description=data['description'])
        new_recipe.save()
        return new_recipe, 201

        

@api.route('/recipes/<int:id>')
class RecipeResource(Resource):
    @api.marshal_with(recipe_model)
    def get(self, id):
        recipe = Recipe.query.get_or_404(id)
        return recipe
    
    @api.marshal_with(recipe_model)   
    def put(self, id):
        recipe_to_update = Recipe.query.get_or_404(id)
        data = request.json
        recipe_to_update.update(title=data['title'], description=data['description'])
        return recipe_to_update, 200

    def delete(self, id):
        pass

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Recipe': Recipe}

if __name__ == '__main__':
    app.run(debug=True)