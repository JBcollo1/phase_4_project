from datetime import datetime
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from config import db, bcrypt, jwt
from models import NovelCollection
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

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
        collection = NovelCollection.query.get(collection_id)
        if not collection:
            return {'msg': 'Collection not found'}, 404

        collection.rating = data['rating']
        db.session.commit()

        return {'msg': 'Collection updated successfully'}, 200

class GetUserCollection(Resource):
    @jwt_required()
    def get(self, user_id):
        collections = NovelCollection.query.filter_by(user_id=user_id).all()

        collections_list = [{
            'id': collection.id,
            'user_id': collection.user_id,
            'novel_id': collection.novel_id,
            'rating': collection.rating,
            'created_at': collection.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': collection.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for collection in collections]

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


novelcollect_api.add_resource(DeleteNovelFromCollection, '/delete/<int:collection_id>')

novelcollect_api.add_resource(AddNovelToCollection, '/add')
novelcollect_api.add_resource(UpdateNovelInCollection, '/update/<int:collection_id>')
novelcollect_api.add_resource(GetUserCollection, '/user/<int:user_id>')
