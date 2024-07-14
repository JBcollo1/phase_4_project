import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://nest_nkpa_user:7ImvCUBGdDEin5cpL80TCvPRDwmJ0MT2@dpg-cq9s53dds78s739i8gqg-a.ohio-postgres.render.com/nest_nkpa')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # Replace with a secure key in production
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    CORS_ALLOW_ORIGINS = '*'  # Adjust this to match your CORS policy
    JSON_COMPACT = False
