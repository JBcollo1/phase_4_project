from flask import Blueprint 
from flask_restful import Api,Resource, reqparse 
from models import User
from config import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import  create_access_token, JWTManager


logs_bp = Blueprint('logs_bp', __name__, url_prefix='/logs')
jwt = JWTManager()
bcrypt = Bcrypt()
logs_api = Api(logs_bp)


@jwt.User_lookup_loader
def user_detail(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return User.query.filter_by(id = identity).first()


signup_args = reqparse.RequestParser()
signup_args.add_argument('username',type=str, help="Username is required", required=True)
signup_args.add_argument('password',type=str, help="Password is required", required=True)
signup_args.add_argument('email',type=str, help="Email is required", required=True)

login_args = reqparse.RequestParse()
login_args.add_argument ('email')
login_args.add_argument ('password')



class Signup (Resource):
    def post (self):
        data = signup_args.parse_args()
        hashed_password = bcrypt.generate_password_hash(data.get('password'))
        new_user = User(email = data.get('email'),username = data.get('username'), password = hashed_password)
        db.session.add (new_user)
        db.session.commit()
        return {"msg":"user created successfully"}






class Register(Resource):
     

     def post(self):

        data = register_args.parse_args()
        hashed_password = bcrypt.generate_password_hash(data.get('password'))
        new_user = User(email = data.get('email'), username = data.get('username'),password= hashed_password )
        db.session.add(new_user)
        db.session.commit()

        return {"msg":'user created successfully'}
     

class Login(Resource):

    def post(self):
        data = login_args.parse_args()
        # check if the user exists in our db 
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return {"msg":"User Does not exists in our DB"}
        if not bcrypt.check_password_hash(user.password, data.get('password')):
            return {"msg": "Password is incorrect!"}
        # check if the password is correct 
        
        # login
        token = create_access_token(identity=user.id)
        return {"token":token}


          
          




# routes
auth_api.add_resource(Register,'/register')
auth_api.add_resource(Login,'/login')