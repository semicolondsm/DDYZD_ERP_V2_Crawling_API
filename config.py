import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_DECODE_ALGORITHMS = 'HS256'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(base_dir, 'develop.sqlite')
    pass

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://'
    pass

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}