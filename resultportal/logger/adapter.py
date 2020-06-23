from time import time
from flask import request
from flask_jwt_extended import get_jwt_identity

error_codes = {
   'BadRequest': 400,
   'Forbidden': 403,
   'GatewayTimeout': 504,
   'MethodNotAllowed': 405,
   'NotAcceptable': 406,
   'NotFound': 404,
   'NotImplemented': 501,
   'RequestTimeout': 408,
   'ServiceUnavailable': 503,
   'Unauthorized': 401
}
# Request adapter with functions returning response data
class RequestResponseAdapter:
   
   def get_username(self):
      # get username from jwt token
      try:
         return get_jwt_identity()['username']
      except:
         return 'anonymous'

   def get_http_headers(self):
      return dict(request.headers)

   def get_protocol(self):
      return request.environ.get('SERVER_PROTOCOL')

   def get_path(self):
      return request.full_path[:-1]
   
   def get_method(self):
      return request.method

   def get_remote_ip(self):
      return request.remote_addr

   def get_response_size(self, response):
      return response.calculate_content_length()

   def get_response_content_type(self, response):
      return response.content_type
   
   def get_response_time_ms(self, g):
      return "{:.2f} ms".format( (time()-g.request_time)*1000 )
   
   def get_request_data(self):
      request_data = {}
      
      if request.args.to_dict():
         request_data['data'] = request.args.to_dict()
         
      if request.form.to_dict():
         request_data['form'] = request.form.to_dict()
         
      if request.get_json():
         request_data['json'] = request.get_json()
         
      file_data = {}
      for key, value in request.files.items():
         file_data[key] = value.filename
         
      if file_data:
         request_data['files'] = file_data
         
      if not request_data:
         return None
      
      return request_data
      
   def get_status_code(self, error):
      # All error are expected to be HTTP errors only
      return error_codes.get(error.__class__.__name__, 500)