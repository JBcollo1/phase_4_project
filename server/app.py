# app.py
#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource
import os
from dotenv import load_dotenv  # Import this

load_dotenv()

# Local imports
from config import app 
from logs import logs_bp  
from novels import novels_bp
from novelcollection import novelcollect_bp

# Add your model imports
from models import User, NovelCollection, Novel

# Register the Blueprint
app.register_blueprint(logs_bp)
app.register_blueprint(novels_bp)
app.register_blueprint(novelcollect_bp)



# Views go here!
@app.route('/')
def index():
    return '<h1>Project Server</h1>'

