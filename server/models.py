# models.py

from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from app import db  # Import db from config.py

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define the relationship to NovelCollection
    novel_collections = db.relationship('NovelCollection', back_populates='user', lazy=True)


class NovelCollection(db.Model, SerializerMixin):
    __tablename__ = 'novel_collections'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define the relationships to User and Novel
    user = db.relationship('User', back_populates='novel_collections')
    novel = db.relationship('Novel', back_populates='novel_collections')


class Novel(db.Model, SerializerMixin):
    __tablename__ = 'novels'

    id = db.Column(db.Integer, primary_key=True)
    profile = db.Column(db.String(200), nullable = False)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer)
    synopsis = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define the relationship to NovelCollection
    novel_collections = db.relationship('NovelCollection', back_populates='novel', lazy=True)
