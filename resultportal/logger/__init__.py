import logging, time, json, traceback
from flask import g, request, jsonify
from logger.adapter import RequestResponseAdapter
from werkzeug.exceptions import HTTPException
from datetime import datetime
from logger.handler import CompressingRotatingFileHandler
import pymysql as MySQL

class WebLogger:
   
   def __init__(self, app, disable_werkzeug=True, backup_count=10, max_bytes=1024*1024*5):
      self.app = app
      self.adapter = RequestResponseAdapter()
      self.disable_werkzeug = disable_werkzeug
      self.backup_count = backup_count
      self.max_bytes = max_bytes
      
   # Function to initiate the logger
   # This function sets up logger and register request and error handlers
   # to the flask app
   # :: Called from the flask app after initialisation
   def initiate_web_logger(self):
      self._register_flask_logger()
      self._register_before_request()
      self._register_exception_handler()
      self._register_after_request()


   def _register_flask_logger(self):
      # disable werkzeug handler on demand
      if self.disable_werkzeug:
         logging.getLogger('werkzeug').disabled = True
      
      self.logger = logging.getLogger('web')
      self.logger.setLevel(logging.DEBUG)
      
      # prepare stream handlers for the logger
      # TODO: in production stream logging is not required, all logs goes to a file
      # the stream handler is for testing purpose
      stream_handler = logging.StreamHandler()
      stream_handler.setLevel(logging.WARNING)
      stream_handler.setFormatter(logging.Formatter(fmt='%(message)s'))
      
      # prepare file handlers for the logger
         # all logs handler
         # 5 MB log file
      file_handler = CompressingRotatingFileHandler(f'logs/{self.logger.name}.log.json', maxBytes=self.max_bytes, backupCount=self.backup_count)
      file_handler.setLevel(logging.WARNING)
      file_handler.setFormatter(logging.Formatter(fmt='%(message)s'))
      
      # add all the handlers to the logger
      self.logger.addHandler(file_handler)
      self.logger.addHandler(stream_handler)


   # catch the request on incoming
   def _register_before_request(self):
      # before start of request get the time of request, this time is
      # used by request adapter for getting the precise response time
      @self.app.before_request
      def track_start_of_request():
         g.request_time = time.time()
   
   
   # register error handlers for all type of exceptions
   def _register_exception_handler(self):
      
      @self.app.errorhandler(Exception)
      def handle_all_exception(err=None):
         
         # handle http exceptions
         if isinstance(err, HTTPException):
            g.status_code = self.adapter.get_status_code(err)
            return jsonify(err={
               'msg': str(err)
            }), g.status_code
         
         # handle uncaught exceptions
         g.status_code = 500         
         error = {
            'traceback': traceback.format_exc()
         }
         
         # handle mysql errors, if any
         # Note: set the g.mysql_stmt before executing any statement
         if isinstance(err, MySQL.Error):
            # get function is used becuase error may be on connecting or acquiring cursor
            error['mysql_stmt'] = g.get('mysql_stmt')
         
         g.error = error

         return jsonify(error={
            'msg': 'The server encountered an error'
         }), g.status_code
      
       
   # modify response if necessary and log data
   def _register_after_request(self):
      
      @self.app.after_request
      def log_request(response): 
         
         adp = self.adapter
         
         # global log format
         log_format = { 
            "headers": adp.get_http_headers(),
            "request_time": "{:.2f}".format(datetime.now().timestamp()),
            "method": adp.get_method(),
            "username": adp.get_username(),
            "path": adp.get_path(),
            "protocol": adp.get_protocol(),
            "remote_ip": adp.get_remote_ip(),
            "response_time_ms": adp.get_response_time_ms(g),
            "response_status_code": g.get('status_code', response.status_code),
            "response_size_bytes": adp.get_response_size(response),
            "response_content_type": adp.get_response_content_type(response),
         }
         
         # if request.method is other than GET, log the data
         if request.method != "GET":
            log_format["request_data"] = adp.get_request_data()
            
         # log with exception and errors
         # g.error flag signifies error other than HTTP errors
         if g.get('error'):
            log_format["error"] = g.error
            self.logger.error(json.dumps(log_format, ensure_ascii=False))
                                
         # common log
         else:            
            self.logger.warning(json.dumps(log_format, ensure_ascii=False))
         
         return response