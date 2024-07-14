from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from config import db, bcrypt, jwt  
from models import  Novel 
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity


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
            'created_at': novel.created_at.isoformat() 
        } for novel in novels]
        
        return {'novels': novels_list}, 200  
class AddNovel(Resource):
    @jwt_required()
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

        
        db.session.add(new_novel)
        db.session.commit()

        return {'msg': 'Novel added successfully', 'novel_id': new_novel.id}, 201


class GetNovel(Resource):
    def get(self, novel_id):
        novel = Novel.query.get(novel_id)
        if not novel:
            return {'msg': 'Novel not found'}, 404

        return {
            'id': novel.id,
            'title': novel.title,
            'genre': novel.genre,
            'author': novel.author,
            'profile': novel.profile,
            'publication_year': novel.publication_year,
            'synopsis': novel.synopsis,
            'created_at':novel.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }, 200
    
class Gettitle(Resource):
    def get(self, title):
        try:
        
            title = str(title)
        except ValueError:
            return {'msg': 'Invalid title format'}, 400

        novel = Novel.query.filter_by(title=title).first()
        if not novel:
            return {'msg': 'Novel not found'}, 404

        return {
            'id': novel.id,
            'title': novel.title,
            'genre': novel.genre,
            'author': novel.author,
            'profile': novel.profile,
            'publication_year': novel.publication_year,
            'synopsis': novel.synopsis,
            'created_at': novel.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }, 200
        


novels_api.add_resource(AddNovel, '/addnovel')  
novels_api.add_resource(GetNovel, '/<int:novel_id>')    
novels_api.add_resource(Gettitle, '/name/<string:title>')    



novels_api.add_resource(ListNovels, '/list')
