from portal.scraper.service import get_result, get_pdf, regno_from_opts
import json

from errors import StudentNotFoundError
from clilogger import initiate_cli_logger

UG_branches = ["CS", "EC", "EE", "MM", "ME", "CE", "PI"]
PG_Branches = [
               "CACA", "CHCH", "MHMH", "PHPH", "MMFT",
               "MMMT", "CSCS", "CAIS", "METE", "MEES",
               "MECI", "MFMS", "CHSS", "CESE", "CEGE",
               "CEWR", "EEPE", "EEPS", "ECEM", "ECCO",
            ]
TYC_branches = [ "MME" ]


def execute(args):   
   # grab the logger
   log = initiate_cli_logger('scraper:all')
   pdf_log = initiate_cli_logger('scraper:pdf')
   
   start_year, end_year = int(args.start_year), int(args.end_year)
   log.debug('Options: start year= %s, end year=%s', start_year, end_year)
   
   result_fp = open('result.json', 'a')
   log.warning('All results are saved to result.json')
      
   for year in range(start_year, end_year+1):
      for course, branches in [ ("UG", UG_branches), ("PG", PG_Branches) ,("TYC", TYC_branches)]:
         for branch in branches:
            
            no_of_misses = 0
            
            # FIXME: it is assumed that there is no more than 130 students in each branch
            for regno in range(1, 130):
               
               try:
                  regno = regno_from_opts(year, course, branch, regno)
                  log.debug('Requesting for regno=%s, semester=latest', regno)
                  
                  # download result and save
                  student = get_result(regno, args.url)
                  # download pdf and save
                  get_pdf(regno, student['student_id'], student['semester'], pdf_log, args.pdf_url)
                  
                  no_of_misses = 0
                  result_fp.write(json.dumps(student)+'\n')
                  log.info('Downloaded result for regno=%s, semester=latest', regno)
                  
               except StudentNotFoundError:
                  log.warning('Student with regno=%s, semester=latest not found'%regno)
                  no_of_misses += 1    
                  
               if no_of_misses == 5:
                  log.warning('Consecutively missed 5 students for branch %s%s%s', year, course, branch)
                  break
   
   result_fp.close()