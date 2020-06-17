from config import dict_config
from flask import Flask, g
from flaskext.mysql import MySQL
from flask_restful import Api
from flask_jwt_extended import JWTManager
from util.logger import WebLogger
from flask_cors import CORS
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseUpload

def create_app():
   app = Flask(__name__)
   app.config.from_object(dict_config['dev'])

   # make the app an api
   api = Api(app)
   
   # allow cross-origin-requests
   CORS(app)
   
   # register driver extension
   creds = None
   # Always pass a valid token for the gdrive api
   if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
         creds = pickle.load(token)

   try:
      gdrive = build('drive', 'v3', credentials=creds)
      app.extensions['gdrive'] = gdrive
   except Exception as error:
      print(error)
      
   
   # register mysql extension
   mysql = MySQL()
   mysql.init_app(app)
   app.extensions['mysql'] = mysql
   
   # register jwt extension
   JWTManager(app)
   
   # register custom logger
   logger = WebLogger(app)
   logger.initiate_web_logger()
   
   # sentry logger for fallback
   # sentry_sdk.init(
   #     dsn="https://d5c57da451664aa59065c03b4777909d@sentry.io/1471638",
   #     integrations=[FlaskIntegration()]
   # )
      
   # import auth api and register   
   from app.web.auth.routes import StudentLoginAuthentication, AdminLoginAuthentication
   api.add_resource(StudentLoginAuthentication, '/student')
   api.add_resource(AdminLoginAuthentication, '/admin')

   # import feedback api and register
   from app.feedback.routes import FeedbackLogger
   api.add_resource(FeedbackLogger, '/feedback/logs')
   
   # import cli api and register
   from app.cli.routes import CLILogger, CLIUploadData, CLIUploadImage, CLIUploadPDF
   api.add_resource(CLILogger, '/cli/logs')
   api.add_resource(CLIUploadData, '/cli/upload/data')
   api.add_resource(CLIUploadImage, '/cli/upload/image')
   api.add_resource(CLIUploadPDF, '/cli/upload/pdf')
   
   return app

if __name__ == '__main__':
   app = create_app()
   app.run()