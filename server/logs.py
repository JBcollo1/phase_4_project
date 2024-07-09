# logs.py

from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from config import db, bcrypt, jwt  # Import db from config.py
from models import User
from flask_jwt_extended import  create_access_token

# Initialize Blueprint
logs_bp = Blueprint('logs_bp', __name__, url_prefix='/logs')
logs_api = Api(logs_bp)

# Define the user lookup callback function for JWT
@jwt.user_lookup_loader
def user_detail(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return User.query.filter_by(id=identity).first()

# Define request parsers for signup and login
signup_args = reqparse.RequestParser()
signup_args.add_argument('username', type=str, help="Username is required", required=True)
signup_args.add_argument('password', type=str, help="Password is required", required=True)
signup_args.add_argument('email', type=str, help="Email is required", required=True)

login_args = reqparse.RequestParser()
login_args.add_argument('email', type=str, help="Email is required", required=True)
login_args.add_argument('password', type=str, help="Password is required", required=True)

# Define the Signup resource
class Signup(Resource):
    def post(self):
        data = signup_args.parse_args()
        try:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_user = User(email=data['email'], username=data['username'], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return {"msg": "User created successfully"}
        except Exception as e:
            print(f"Error: {e}")  # Print the exception for debugging
            db.session.rollback()
            return {"msg": "Internal server error"}, 500

# Define the Login resource
class Login(Resource):
    def post(self):
        data = login_args.parse_args()
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return {"msg": "User does not exist"}, 401
        if not bcrypt.check_password_hash(user.password, data['password']):
            return {"msg": "Wrong password"}, 401
        token = create_access_token(identity=user.id)
        return {"username":user.username,
            "token": token}

# Add the resources to the API
logs_api.add_resource(Signup, '/signup')
logs_api.add_resource(Login, '/login')
