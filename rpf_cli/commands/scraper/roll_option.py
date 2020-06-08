from commands.scraper.helpers import (
   StudentResultDownloader, valid_regno, get_semesters
)
import json
from pprint import pprint
from errors import RollError, StudentNotFoundError

def execute(regnos, semesters, nosave):
   '''
      This function downloads every result for every semester from the rolls array
   '''
   for regno in regnos:
      
      try:
         # the code passes without raising exception if it is a valid roll no
         valid_regno(regno)
         
         # check is the roll given is valid or not
         with open('result.json', 'a') as result_fp:
         
            # if the flag to just fetch semesters is not set
            if semesters:
               for semester in semesters:
                  
                  try:
                     # fetch the student data and save to redirect to stdout
                     student = StudentResultDownloader.download_result(regno, semester)
                     
                     if not nosave:
                        # write the data to a file
                        result_fp.write( json.dumps(student)+'\n' )
                     else:
                        # TODO: log the student
                        pprint(student)
                        
                  except StudentNotFoundError as err:
                     print(err)
         
            # there is no semesters specified default to the last one
            else:
               
               try:
                  student = StudentResultDownloader.download_result(regno, None)
                  
                  if not nosave:
                     # write the data to a file
                     result_fp.write( json.dumps(student)+'\n' )
                  else:
                     # TODO: log the student
                     pprint(student)
                     
               except StudentNotFoundError as err:
                  print(err)
            
      # the roll is not valid 
      except RollError as err:
         #TODO: all logging here
         print(err)