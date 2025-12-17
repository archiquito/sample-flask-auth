"""CONFIGURATION FILE"""

class Config:
    """BASE CONFIGURATION CLASS"""
    HOST = '127.0.0.1'
    PORT = 8000
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
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