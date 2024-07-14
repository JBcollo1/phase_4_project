from datetime import datetime
from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from config import db, bcrypt, jwt
from models import NovelCollection,User,Novel
from flask_jwt_extended import  create_refresh jwt_required, get_jwt_identity

novelcollect_bp = Blueprint('novelcollect_bp', __name__, url_prefix='/novelcollection')
novelcollect_api = Api(novelcollect_bp)

novelcollect_args = reqparse.RequestParser()
novelcollect_args.add_argument('novel_id', type=int, required=True, help="Novel ID is required")
novelcollect_args.add_argument('rating', type=int, required=True, help="Rating is required")

class AddNovelToCollection(Resource):
    @jwt_required()
    def post(self):
        data = novelcollect_args.parse_args()
        print("Received data:", data)  

        user_id = get_jwt_identity()  

        existing_collection = NovelCollection.query.filter_by(user_id=user_id, novel_id=data['novel_id']).first()
        if existing_collection:
            return {'msg': 'Novel already in collection'}, 400

        new_collection = NovelCollection(
            user_id=user_id,
            novel_id=data['novel_id'],
            rating=data['rating']
        )
        db.session.add(new_collection)
        db.session.commit()

        return {'msg': 'Novel added to collection successfully', 'collection_id': new_collection.id}, 201


class UpdateNovelInCollection(Resource):
    @jwt_required()
    def put(self, collection_id):
        data = novelcollect_args.parse_args()
        print(f"Request Data: {data}")  # Add this line to check the incoming data
        collection = NovelCollection.query.get(collection_id)
        user_id = get_jwt_identity()  
        novel_id =NovelCollection.query.filter_by(user_id=user_id, novel_id=data['novel_id']).first()
        if not collection:
            return {'msg': 'Collection not found'}, 404

        collection.rating = data['rating']
        db.session.commit()

        return {'msg': 'Collection updated successfully'}, 200

class GetUserCollection(Resource):
    @jwt_required()
    def get(self, user_id):
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return {'msg': 'Unauthorized'}, 403

        collections = NovelCollection.query.filter_by(user_id=user_id).all()

        collections_list = []
        for collection in collections:
            novel = Novel.query.get(collection.novel_id)
            if novel:
                collections_list.append({
                    'id': collection.id,
                    'user_id': collection.user_id,
                    'novel_id': collection.novel_id,
                    'rating': collection.rating,
                    'created_at': collection.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': collection.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'novel': {
                        'title': novel.title,
                        'genre': novel.genre,
                        'author': novel.author,
                        'profile': novel.profile,  # Ensure profile field is included
                        'publication_year': novel.publication_year,
                        'synopsis': novel.synopsis,
                    }
                })

        return {'collections': collections_list}, 200


class DeleteNovelFromCollection(Resource):
    @jwt_required()
    def delete(self, collection_id):
        user_id = get_jwt_identity()  

        
        collection = NovelCollection.query.filter_by(id=collection_id, user_id=user_id).first()
        if not collection:
            return {'msg': 'Collection item not found'}, 404

        db.session.delete(collection)
        db.session.commit()

        return {'msg': 'Novel removed from collection successfully'}, 200

class GetUserId(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()  # Extract userId from the JWT token
        return {'userId': user_id}, 200
    
class GetUserDetails(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'msg': 'User not found'}, 404

        user_details = {
            'id': user.id,
            'username': user.username,
            'profile': user.profile,
            'email': user.email,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        return jsonify(user_details)
novelcollect_api.add_resource(DeleteNovelFromCollection, '/delete/<int:collection_id>')
novelcollect_api.add_resource(GetUserId, '/getUserId')
novelcollect_api.add_resource(AddNovelToCollection, '/add')
novelcollect_api.add_resource(UpdateNovelInCollection, '/update/<int:collection_id>')
novelcollect_api.add_resource(GetUserCollection, '/user/<int:user_id>')
novelcollect_api.add_resource(GetUserDetails, '/getuserdetails')


