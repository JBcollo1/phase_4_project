# logs.py

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from config import db, bcrypt, jwt  # Import db from config.py
from models import User
from flask_jwt_extended import  create_access_token ,create_refresh_token, jwt_required, get_jwt,get_jwt_identity


# Initialize Blueprint
logs_bp = Blueprint('logs_bp', __name__, url_prefix='/logs')
logs_api = Api(logs_bp)
blacklist = set()
# Define the user lookup callback function for JWT
@jwt.user_lookup_loader
def user_detail(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return User.query.filter_by(id=identity).first()


signup_args = reqparse.RequestParser()
signup_args.add_argument('username', type=str, help="Username is required", required=True)
signup_args.add_argument('password', type=str, help="Password is required", required=True)
signup_args.add_argument('email', type=str, help="Email is required", required=True)
signup_args.add_argument('profile', type = str , required = False)

login_args = reqparse.RequestParser()
login_args.add_argument('email', type=str, help="Email is required", required=True)
login_args.add_argument('password', type=str, help="Password is required", required=True)


class Signup(Resource):
    def post(self):
        data = signup_args.parse_args()
        try:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_user = User(email=data['email'], username=data['username'], password=hashed_password , profile = data['profile'])
            db.session.add(new_user)
            db.session.commit()
            return {"msg": "User created successfully"}
        except Exception as e:
            print(f"Error: {e}")  
            db.session.rollback()
            return {"msg": "Internal server error"}, 500


class Login(Resource):
    def post(self):
        data = login_args.parse_args()
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return {"msg": "User does not exist"}, 401
        if not bcrypt.check_password_hash(user.password, data['password']):
            return {"msg": "Wrong password"}, 401
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            "username": user.username,
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200
class user(Resource):      
        @jwt_required()
        def get(self):
            current_user = get_jwt_identity()
            user = User.query.filter_by(id=current_user).first()
            if not user:
                return jsonify({"msg": "User not found"}), 404

            return{
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profile": user.profile,
                "created_at": user.created_at.isoformat() ,
                "updated_at": user.updated_at.isoformat() 
            },200
            # return jsonify(user_data), 200

class Logout(Resource):
    @jwt_required()
    def delete(self):
        jti = get_jwt()['jti']  
        blacklist.add(jti)
        return {"msg":"Successfully logged out"}

logs_api.add_resource(Signup, '/signup')
logs_api.add_resource(Login, '/login')
logs_api.add_resource(Logout, '/logout')
logs_api.add_resource(user, '/user')


