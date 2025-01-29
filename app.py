from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Recipe Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Get all recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([{"id": r.id, "title": r.title, "ingredients": r.ingredients, "instructions": r.instructions} for r in recipes])

# Get a single recipe by ID
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    return jsonify({"id": recipe.id, "title": recipe.title, "ingredients": recipe.ingredients, "instructions": recipe.instructions})

# Add a new recipe
@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.json
    new_recipe = Recipe(title=data['title'], ingredients=data['ingredients'], instructions=data['instructions'])
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"message": "Recipe added successfully!", "id": new_recipe.id}), 201

# Update a recipe
@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    data = request.json
    recipe.title = data.get('title', recipe.title)
    recipe.ingredients = data.get('ingredients', recipe.ingredients)
    recipe.instructions = data.get('instructions', recipe.instructions)
    db.session.commit()

    return jsonify({"message": "Recipe updated successfully!"})

# Delete a recipe
@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
