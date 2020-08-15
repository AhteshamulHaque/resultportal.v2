import re, json
import portal.scraper.roll_option as roll_option
import portal.scraper.range_option as range_option
from clilogger import initiate_cli_logger
from collections import namedtuple

'''
File content:
{ 
   "roll_query": {
      "roll1": [...semesters...],
      "roll2": [...semesters...],
      ...................,
   },

   "range_query": [
      { "start": "...", "end": "...", "semesters": [...] } ,
      { "start": "...", "end": "...", "semesters": [...] } ,
      ........,
   ]
}

start -> 2017UGCS002
end -> 2017UGCS034
'''
   
def execute(args):
   '''
      This function downloads every result for every semester from the rolls array
   '''
   # grab the loggers
   # Because file option calls roll and range options, so there is duplication
   # of loggers. To avoid that roll and range options are passed loggers as
   # arguments
   file_log = initiate_cli_logger('scraper:file')
   roll_log = initiate_cli_logger('scraper:roll')
   range_log = initiate_cli_logger('scraper:range')
   pdf_log = initiate_cli_logger('scraper:pdf')
   
   query = json.load(args.file)
   file_log.debug('File=%s', args.file)
   file_log.warning('All downloaded results are saved to result.json')
   
   if query.get('roll_query'):
      
      file_log.debug('Using scraper:roll for scraping')
      for roll, semesters in query['roll_query'].items():
         args.roll = [roll]
         args.semester = semesters
         roll_option.execute(args, roll_log, pdf_log)
         
   
   if query.get('range_query'):
      
      file_log.debug('Using scraper:range for scraping')
      for _range in query['range_query']:
         args.range = [_range['start'], _range['end']]
         args.semester = _range['semesters']
         range_option.execute(args, range_log, pdf_log)