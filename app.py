import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# PostgreSQL Database Configuration
DATABASE_URL = "postgresql://recipes_db_l4zc_user:GA15b6X1FCBD3tXxyGoOzeem2AaL384V@dpg-cudjolqj1k6c73cos74g-a.oregon-postgres.render.com/recipes_db_l4zc"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Recipe Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

# Initialize Database
with app.app_context():
    db.create_all()

# API Routes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([{
        "id": r.id,
        "title": r.title,
        "ingredients": r.ingredients,
        "instructions": r.instructions
    } for r in recipes])

@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe_by_id(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    return jsonify({
        "id": recipe.id,
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions
    })

@app.route('/recipes', methods=['POST'])
def add_recipe():
    try:
        data = request.json
        if not data or "title" not in data or "ingredients" not in data or "instructions" not in data:
            return jsonify({"error": "Invalid input"}), 400

        new_recipe = Recipe(
            title=data["title"],
            ingredients=data["ingredients"],
            instructions=data["instructions"]
        )
        db.session.add(new_recipe)
        db.session.commit()

        return jsonify({
            "id": new_recipe.id,
            "title": new_recipe.title,
            "ingredients": new_recipe.ingredients,
            "instructions": new_recipe.instructions,
        }), 201
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    print(f"Using database at: {DATABASE_URL}")
    app.run(debug=True)
