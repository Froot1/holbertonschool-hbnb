import os
from datetime import timedelta
from dotenv import load_dotenv


class Config:
    load_dotenv()
    DEBUG = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY','xFx_my_team_the_best_developers_xFx')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_ALGORITHM = 'HS512'
    JWT_DECODE_ALGORITHMS = ['HS512']


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
}
