from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from config import db, bcrypt, jwt  
from models import User, Novel, NovelCollection 
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity


novels_bp = Blueprint('novels_bp', __name__, url_prefix='/novels')
novels_api = Api(novels_bp)


novels_args = reqparse.RequestParser()
novels_args.add_argument('title', type=str, required=True, help="Title is required")
novels_args.add_argument('genre', type=str, required=True, help="Genre is required")
novels_args.add_argument('author', type=str, required=True, help="Author is required")
novels_args.add_argument('profile', type=str, required=False, help="Profile is optional")
novels_args.add_argument('publication_year', type=int, required=True, help="Publication year is required")
novels_args.add_argument('synopsis', type=str, required=True, help="Synopsis is required")

class ListNovels(Resource):
    def get(self):
        
        novels = Novel.query.all()
        
        
        novels_list = [{
            'id': novel.id,
            'profile':novel.profile,
            'title': novel.title,
            'genre': novel.genre,
            'author': novel.author,
            'publication_year': novel.publication_year,
            'synopsis': novel.synopsis,
            'created_at': novel.created_at
        } for novel in novels]
        
        return {'novels': novels_list}, 200  
class AddNovel(Resource):
    def post(self):
        data = novels_args.parse_args()
        if not all(key in data for key in ['title', 'genre', 'author', 'profile','publication_year', 'synopsis']):
            return {'msg': 'Missing required fields'}, 400

        
        new_novel = Novel(
            title=data['title'],
            genre=data['genre'],
            profile = data['profile'],
            author=data['author'],
            publication_year=data['publication_year'],
            synopsis=data['synopsis']
        )

        # Add the new novel to the database
        db.session.add(new_novel)
        db.session.commit()

        return {'msg': 'Novel added successfully', 'novel_id': new_novel.id}, 201


novels_api.add_resource(ListNovels, '/list')
