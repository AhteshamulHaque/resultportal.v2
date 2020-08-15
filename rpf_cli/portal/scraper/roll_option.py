from portal.scraper.service import get_result, get_pdf
from pprint import pprint
from errors import StudentNotFoundError
from clilogger import initiate_cli_logger
import json

def execute(args, roll_log, pdf_log):
   '''
      This function downloads every result for every semester from the rolls array
   '''
   regnos = args.roll
   semesters = args.semester
   stdout = args.stdout
   url = args.url
   pdf_url = args.pdf_url
   
   roll_log.debug('Options: regnos=%s, semesters=%s', regnos, semesters)
   result_fp = open('result.json', 'a')
      
   for regno in regnos:
         
      # if semesters are supplied
      if semesters:
         for semester in semesters: 
            try:
               roll_log.debug('Requesting for regno=%s, semester=%s', regno, semester)
               
               # fetch the student data and save
               student = get_result(regno, url, semester)
               # download the pdf also
               get_pdf(regno, student['student_id'], semester, pdf_log, pdf_url)
               
               roll_log.info('Downloaded result for regno=%s, semester=%s', regno, semester)
               
               if not stdout:
                  # write the data to a file
                  result_fp.write( json.dumps(student)+'\n' )
               else:
                  # TODO: log to stdout
                  pprint(student)
                  
            except StudentNotFoundError:
               roll_log.warning('Student with regno=%s, semester=%s not found', regno, semester)
   
      # there is no semesters specified default to the last one
      else:
         try:
            roll_log.debug('Requesting for regno=%s, semester=latest', regno)
            
            # fetch the student data and save
            student = get_result(regno, url)
            # download the pdf also
            get_pdf(regno, student['student_id'], student['semester'], pdf_log, pdf_url)
            
            roll_log.info('Downloaded result for regno=%s, semester=latest', regno)
            
            if not stdout:
               # write the data to a file
               result_fp.write( json.dumps(student)+'\n' )
            else:
               # TODO: log the student
               pprint(student)
               
         except StudentNotFoundError:
            roll_log.warning('Student with regno=%s, semester=latest not found'%regno)
            
   result_fp.close()