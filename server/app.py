#!/usr/bin/env python3

# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .config import Config
from sqlalchemy import MetaData

# Define metadata for the database schema
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize extensions
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from config.py

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize CORS
    CORS(app, origins=Config.CORS_ALLOW_ORIGINS)

    # Set up JWT blacklist loader
    blacklist = set()

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in blacklist

    # Instantiate REST API
    api = Api(app)

    # Import models to register them with SQLAlchemy
    with app.app_context():
        from .models import User, NovelCollection, Novel  # Import models here

    # Import API routes
    from .logs import logs_bp
    from .novels import novels_bp
    from .novelcollection import novelcollect_bp

    app.register_blueprint(logs_bp)
    app.register_blueprint(novels_bp)
    app.register_blueprint(novelcollect_bp)

    # Views go here!
    @app.route('/')
    def index():
        return '<h1>Project Server</h1>'

    return app

# Initialize the app
app = create_app()
if __name__ == "__main__":
    app.run(port=5000, debug=True)