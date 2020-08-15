from portal.scraper.service import (
   get_result, get_pdf, get_semesters, split_regno, regno_from_opts
)
from pprint import pprint
import re
import json
from clilogger import initiate_cli_logger
from errors import RollError, StudentNotFoundError

def execute(args, range_log, pdf_log):
   '''
      This function downloads every result for every semester from the rolls array
      _range: [start_regno, end_regno]
      
   '''
   _range = args.range
   semesters = args.semester
   url = args.url
   pdf_url = args.pdf_url
   stdout = args.stdout
   
   range_log.debug('Options: _range=%s, semesters=%s', _range, semesters)
   
   # get start and end roll
   strt_regno, end_regno = _range
   
   # split the roll
   year, course, branch = split_regno(strt_regno)
   range_log.debug('year=%s, course=%s, branch=%s', year, course, branch)
   
   # find integer number of start roll and end roll
   strt_num = int( re.search(r'\d+$', strt_regno).group() )
   end_num = int( re.search(r'\d+$', end_regno).group() )
   range_log.debug('Start roll number=%s, End roll number=%s', strt_num, end_num)
   
   # check if start roll is greater that end roll
   if strt_num > end_num:
      raise ValueError("%s cannot be greater than %s", strt_regno, end_regno)
   
   result_fp = open('result.json', 'a')
      
   for roll_num in range( strt_num, end_num+1 ):
      
      # if semesters are supplied
      if semesters:
         for semester in semesters: 
            try:
               regno = regno_from_opts(year, course, branch, roll_num)
               range_log.debug('Requesting for regno=%s, semester=%s', regno, semester)
               
               # fetch the student data and save
               student = get_result(regno, url, semester)
               # download the pdf also
               get_pdf(regno, student['student_id'], semester, pdf_log, pdf_url)
               
               range_log.info('Downloaded result for regno=%s, semester=%s', regno, semester)
               
               if not stdout:
                  # write the data to a file
                  result_fp.write( json.dumps(student)+'\n' )
               else:
                  # TODO: log to stdout
                  pprint(student)
                  
            except StudentNotFoundError:
               range_log.warning('Student with regno=%s,semester=%s not found', regno, semester)
   
      # there is no semesters specified default to the last one
      else:
         try:
            regno = regno_from_opts(year, course, branch, roll_num)
            range_log.debug('Requesting for regno=%s, semester=latest', regno)
            
            # fetch the student data and save
            student = get_result(regno, url)
            # download the pdf also
            get_pdf(regno, student['student_id'], student['semester'], pdf_log, pdf_url)
            
            range_log.info('Downloaded result for regno=%s, semester=latest', regno)
            
            if not stdout:
               # write the data to a file
               result_fp.write( json.dumps(student)+'\n' )
            else:
               # TODO: log the student
               pprint(student)
               
         except StudentNotFoundError:
            range_log.warning('Student with regno=%s, semester=latest not found'%regno)
            
   result_fp.close()