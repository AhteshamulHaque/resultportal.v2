import logging, time, json, traceback
from flask import g, request, jsonify
from util.adapters import RequestResponseAdapter
from werkzeug.exceptions import HTTPException
from datetime import datetime
from logging.handlers import RotatingFileHandler

# TODO: check form data and json using logging
class WebLogger:
   
   def __init__(self, app):
      self.app = app
      self.adapter = RequestResponseAdapter()
      
   # Function to initiate the logger
   # This function sets up logger and register request and error handlers
   def initiate_web_logger(self):
      self.register_flask_logger()
      self.register_before_request()
      self.register_exception_handler()
      self.register_after_request()


   def register_flask_logger(self):
      # disable werkzeug handler
      logging.getLogger('werkzeug').disabled = True
      
      self.logger = logging.getLogger('web')
      self.logger.setLevel(logging.INFO)
      
      # prepare stream handlers for the logger
      streamhandler = logging.StreamHandler()
      streamhandler.setLevel(logging.INFO)
      streamhandler.setFormatter(logging.Formatter(fmt='%(message)s'))
      
      # prepare file handlers for the logger
         # all logs handler
         # 5 MB log file
      all_log_handler = RotatingFileHandler('logs/app.log.json', maxBytes=5242880, backupCount=100)
      all_log_handler.setLevel(logging.INFO)
      all_log_handler.setFormatter(logging.Formatter(fmt='%(message)s'))
      
      # add all the handlers to the logger
      self.logger.addHandler(all_log_handler)
      self.logger.addHandler(streamhandler)


   # catch the request on incoming
   def register_before_request(self):
      # before start of request get the time of request
      # this time is used by request adapter for getting the precise
      # response time
      @self.app.before_request
      def track_start_of_request():
         g.request_time = time.time()
   
   
   # register error handlers for all type of exceptions
   def register_exception_handler(self):
      
      @self.app.errorhandler(Exception)
      def handle_all_exception(err=None):
         
         if isinstance(err, HTTPException):
            g.status_code = self.adapter.get_status_code(err)
            return jsonify(err={
               'msg': str(err)
            }), g.status_code
         
         # if error is not a HTTP error, g.error signifies error flag
         g.error = True
         g.error_log = traceback.format_exc()
         g.status_code = 500

         return jsonify(error={
            "msg": "The server encountered an error"
         }), g.status_code
      
       
   # modify response if necessary and log data
   def register_after_request(self):
      
      @self.app.after_request
      def log_request(response): 
         
         # global log format
         log_format = { 
            "request_time": datetime.strftime(datetime.now(), '%d/%m/%Y %M:%H:%S'),
            "method": self.adapter.get_method(),
            "username": self.adapter.get_username(),
            "path": self.adapter.get_path(),
            "referer": self.adapter.get_http_header('Referer', '-'),
            "x_forwarded_for": self.adapter.get_http_header('X-Forwarded-For', '-'),
            "protocol": self.adapter.get_protocol(),
            "remote_ip": self.adapter.get_remote_ip(),
            "response_time_ms": self.adapter.get_response_time_ms(g),
            "request_content_type": self.adapter.get_http_header('Content-Type', '-'),
            "response_status_code": g.get('status_code', response.status_code),
            "response_size_bytes": self.adapter.get_response_size(response),
            "response_content_type": self.adapter.get_response_content_type(response),
         }
         
         # if request.method is other than GET, log the data
         if request.method != "GET":
            log_format["data"] = self.adapter.get_request_data()
            
         # log with exception and errors
         # g.error flag signifies error other than HTTP errors
         if g.get('error', False):
            log_format["error"] = g.error_log
            self.logger.info(json.dumps(log_format, ensure_ascii=False))
                                
         # common log
         else:            
            self.logger.info(json.dumps(log_format, ensure_ascii=False))
         
         return response