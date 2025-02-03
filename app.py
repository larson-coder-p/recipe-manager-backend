import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate  # Import Flask-Migrate
from models import db, User, Recipe, Category, Review

app = Flask(__name__)
CORS(app)

# PostgreSQL Database Configuration
DATABASE_URL = "postgresql://recipes_db_l4zc_user:GA15b6X1FCBD3tXxyGoOzeem2AaL384V@dpg-cudjolqj1k6c73cos74g-a.oregon-postgres.render.com/recipes_db_l4zc"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

if __name__ == '__main__':
    app.run(debug=True)
