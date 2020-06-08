from flask import current_app
from flask_restful import reqparse, Resource
import logging, os
from logging.handlers import RotatingFileHandler

# This routes provides the functionality for aggregating cli logging
class FeedbackLogger(Resource):
   
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('log', location='json', required=True, help='feedback log')
      
      args = parser.parse_args()
      
      logger = logging.getLogger('feedback')
      logger.setLevel(logging.INFO)
      
      # prepare file handlers for the logger
      # all logs handler
      # 5 MB log file
      all_log_handler = RotatingFileHandler('logs/feedback.log.json', maxBytes=5242880, backupCount=100)
      all_log_handler.setLevel(logging.INFO)
      all_log_handler.setFormatter(logging.Formatter(fmt='%(message)s'))
      
      # all the file handler
      logger.addHandler(all_log_handler)
      
      logger.info(args['log'])
      
      return { 'app': 'feedback', 'message': 'Logging successfull' }, 200