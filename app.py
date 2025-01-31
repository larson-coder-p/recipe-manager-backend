import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set database path inside backend folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "recipes.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Ensure database folder and file exist
def initialize_database():
    if not os.path.exists(DATABASE_PATH):
        print("Creating database file...")
        with app.app_context():
            db.create_all()
        print("Database created successfully!")

# Recipe Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

# Call function to ensure database exists
initialize_database()

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

@app.route('/recipes', methods=['POST'])
def add_recipe():
    try:
        print("Incoming POST request:", request.json)  # Debugging
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

        print(f"Recipe '{new_recipe.title}' added successfully!")
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
    print(f"Using database at: {DATABASE_PATH}")
    app.run(debug=True)
