from logging.handlers import HTTPHandler
import logging, traceback, json

# # TODO: add credentials to log to the server
# class CLIHandler(HTTPHandler):
#     """
#     A class which sends records to a Web server, using either GET or
#     POST semantics.
#     """
#     def __init__(self, host, url, secure=False, credentials=None,
#                  context=None):
#         """
#         Initialize the instance with the host and the request URL
#         """
#         logging.Handler.__init__(self)
#         method = "GET"
#         if not secure and context is not None:
#             raise ValueError("context parameter only makes sense "
#                              "with secure=True")
#         self.host = host
#         self.url = url
#         self.method = method
#         self.secure = secure
#         self.credentials = credentials
#         self.context = context
        
#         # logger to log if cannot send data to server
#         self.logger = logging.getLogger('cli_failed')
        
#         file_handler = logging.FileHandler('failed.log.json', 'a')
#         file_handler.setLevel(logging.WARNING)
        
#         self.logger.addHandler(file_handler)

#     def handleError(self, record):
#         # log to a file if clilogger failed to log to the server
#         self.logger.warning( json.dumps(record) )
    
#     def mapLogRecord(self, record):
#         """
#         Default implementation of mapping the log record into a dict
#         that is sent as the CGI data. Overwrite in your class.
#         Contributed by Franz Glasner.
#         """
#         d = record.__dict__
#         _record = {
#                 'time': d['created'],
#                 'msg': d['msg'],
#                 'levelname': d['levelname']
#                 }        
#         if d['exc_info']:
#             _record['error'] = ''.join(traceback.format_exception(*d['exc_info']))
#         return _record

#     def emit(self, record):
#         """
#         Format the record
#         Emit a record.
#         Send the record to the Web server as a percent-encoded dictionary
#         """
#         record = self.mapLogRecord(record)
        
#         try:
#             import http.client, urllib.parse
#             host = self.host
            
#             if self.secure:
#                 h = http.client.HTTPSConnection(host, context=self.context)
#             else:
#                 h = http.client.HTTPConnection(host)
#             url = self.url

#             if (url.find('?') >= 0):
#                 sep = '&'
#             else:
#                 sep = '?'
                
#             data = urllib.parse.urlencode(record) # actual log to send to the server
#             url = url + "%c%s" % (sep, data)
#             h.putrequest(self.method, url)
#             # support multiple hosts on one IP address...
#             # need to strip optional :port from host, if present
#             i = host.find(":")
#             if i >= 0:
#                 host = host[:i]
#             # See issue #30904: putrequest call above already adds this header
#             # on Python 3.x.
#             # h.putheader("Host", host)
#             if self.credentials:
#                 import base64
#                 s = ('%s:%s' % self.credentials).encode('utf-8')
#                 s = 'Basic ' + base64.b64encode(s).strip().decode('ascii')
#                 h.putheader('Authorization', s)
#             h.endheaders()
#             h.getresponse()    # can't do anything with the result
#         except Exception:
#             self.handleError(record) # connection error, log record to a file

def initiate_cli_logger(name):
    
    # only create handlers, filters, formatters, if they does not exists
    if not logging.Logger.manager.loggerDict.get(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(fmt='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

        # http_handler = CLIHandler(host='localhost:5000', url='/')
        # http_handler.setLevel(log_level)
        # logger.addHandler(http_handler)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)    
        logger.addHandler(stream_handler)
        
        file_handler = logging.FileHandler('logs/%s.log'%name)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        logger = logging.getLogger(name)
            
    return logger