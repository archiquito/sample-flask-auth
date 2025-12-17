"""CONFIGURATION FILE"""

class Config:
    """BASE CONFIGURATION CLASS"""
    HOST = '127.0.0.1'
    PORT = 8000
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask_auth:example@localhost:3306/flask_auth'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'

class EnviorementConfig(Config):
    """DEVELOPMENT CONFIGURATION CLASS"""
    DEBUG = True
    ENV = 'development'


config = {
    'enviorement': EnviorementConfig.ENV,
    'db_uri': Config.SQLALCHEMY_DATABASE_URI    
}