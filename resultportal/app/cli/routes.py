from flask import current_app, request
from flask_restful import reqparse, Resource
import logging
from logging.handlers import RotatingFileHandler
from app.cli.savedata import SaveData
from app.cli.saveimage import SaveImage
from app.cli.savepdf import SavePDF
from werkzeug.datastructures import FileStorage

# This routes provides the functionality for cli logging
class CLILogger(Resource):
   
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('log', location='json', required=True, help='feedback log')
      
      args = parser.parse_args()
      
      logger = logging.getLogger('feedback')
      logger.setLevel(logging.INFO)
      
      # prepare file handlers for the logger
      # all logs handler
      # 5 MB log file
      all_log_handler = RotatingFileHandler('logs/cli.log.json', maxBytes=5242880, backupCount=100)
      all_log_handler.setLevel(logging.INFO)
      all_log_handler.setFormatter(logging.Formatter(fmt='%(message)s'))
      
      logger.info(args['log'])
      
      return { 'app': 'cli', 'message': 'Logging successfull' }, 200
   

# Resource to update database
# need a json file
class CLIUploadData(Resource):
   
   def post(self):
      
      parser = reqparse.RequestParser()
      parser.add_argument('data_file', type=FileStorage, location='files', help='Result data to upload', required=True)
      args = parser.parse_args()
      
      conn = current_app.extensions['mysql']
      cursor = conn.cursor()
      
      # actual saving of data in the database
      SaveData(args['data_file'], cursor)
      
      conn.commit()
      conn.close()


# Resource to upload images to gdrive and links to mysql
class CLIUploadImage(Resource):
   
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('images', type=FileStorage, action='append', location='files', help='Images to upload', required=True)
      args = parser.parse_args()
      
      gdrive = current_app.extensions['gdrive']
      
      conn = current_app.extensions['mysql']
      cursor = conn.cursor()
      
      # actual saving of images in gdrive and mysql updating
      SaveImage(args['images'], gdrive, cursor)
      
      conn.commit()
      conn.close()


# Resource to upload pdf to gdrive and link to mysql
class CLIUploadPDF(Resource):
   
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('pdfs', type=FileStorage, action='append', location='files', help='Pdfs to upload', required=True)
      args = parser.parse_args()
      
      gdrive = current_app.extensions['gdrive']
      
      conn = current_app.extensions['mysql']
      cursor = conn.cursor()
      
      # actual saving of images in gdrive and mysql updating
      SaveImage(args['pdfs'], gdrive, cursor)
      
      conn.commit()
      conn.close()