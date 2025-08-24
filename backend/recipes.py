from flask_restx import Api, Resource, fields, Namespace
from flask import Flask, request
from model import Recipe
from exts import db 
from flask_jwt_extended import jwt_required


recipe_ns = Namespace('recipes',description="A namespace for recipes")



recipe_model = recipe_ns.model("Recipe", {
    "id": fields.Integer(),
    "title": fields.String(),
    "description": fields.String(),
})

@recipe_ns.route('/recipes')
class RecipeListResource(Resource):
    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def get(self):
        """Get all recipes"""
        return Recipe.query.all()

    @recipe_ns.expect(recipe_model)
    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()   # ✅ only logged-in users can add recipes
    def post(self):
        """Create a new recipe"""
        data = request.json
        new_recipe = Recipe(
            title=data['title'],
            description=data['description']
        )
        new_recipe.save()
        return new_recipe, 201