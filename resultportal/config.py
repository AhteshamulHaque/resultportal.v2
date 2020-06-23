import os

# Global configuration
class Config:
   DEBUG = False
   TESTING = False
   
   # mysql extension configuration
   MYSQL_DATABASE_HOST = os.getenv('MYSQL_DATABASE_HOST', 'localhost')
   MYSQL_DATABASE_USER = os.getenv('MYSQL_DATABASE_USER', 'root')
   MYSQL_DATABASE_PASSWORD = os.getenv('MYSQL_DATABASE_PASSWORD', 'Haque8900@')
   
   # google drive configuration
   GDRIVE_SCOPES = ['https://www.googleapis.com/auth/drive']
   
   # jwt extension configuration
   JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-jwt-key')
   
   # app secret key
   SECRET_KEY = os.getenv('SECRET_KEY', 'some-random-secret-key')

# Development configuration
class DevelopmentConfig(Config):
   DEBUG = True

# Testing configuration
class TestingConfig(Config):
   DEBUG = True
   TESTING = True
   
   # mysql testing configuration
   MYSQL_DATABASE_HOST = 'localhost'
   MYSQL_DATABASE_USER = 'root'
   MYSQL_DATABASE_PASSWORD = 'Haque8900@'
   
   # jwt testing configuration
   JWT_SECRET_KEY = 'testing-secret-jwt-key'
   
   # testing secret key
   SECRET_KEY = 'some-random-testing-secret-key'
   
   # app api key -> this is for security purpose so that
   # if anyone learns the route and their associated variables
   # they will not be able to manipulate it without the key
   API_KEY = 'a-super-random-api-key'
  

# Production configuration
class ProductionConfig(Config):
   DEBUG = False

dict_config = dict(
   dev=DevelopmentConfig,
   test=TestingConfig,
   prod=ProductionConfig
)