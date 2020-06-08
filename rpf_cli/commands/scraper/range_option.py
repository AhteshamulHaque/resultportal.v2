from commands.scraper.helpers import (
   StudentResultDownloader, valid_regno, get_semesters, parse_regno, regno_from_opts
)
from pprint import pprint
import re, json
from errors import RollError, StudentNotFoundError

def execute(_range, semesters, nosave):
   '''
      This function downloads every result for every semester from the rolls array
   '''
   
   # get start and end roll
   strt_regno, end_regno = _range.split('-')
   
   # check if the rolls are valid or not
   try:
      valid_regno(strt_regno)
      valid_regno(end_regno)

      # split the roll
      year, course, branch = parse_regno(strt_regno)
      
      # find integer number of start roll and end roll
      strt_num = re.search(r'\d+$', strt_regno).group()
      end_num = re.search(r'\d+$', end_regno).group()
      
      # check if start roll is greater that end roll
      if int(strt_num) < int(end_num):
         raise ValueError("%s cannot be greater than %s", end_regno, strt_regno)
      
      with open('result.json', 'a') as fp:
         
         for roll_num in range( int(strt_num), int(end_num)+1 ):
            
            for semester in semesters:
               # fetch the student data and save to redirect to stdout
               try:
                  roll = regno_from_opts(year, course, branch, roll_num)
                  student = StudentResultDownloader.download_result(roll, semester)
                  
                  if nosave:
                     # TODO: log the student
                     pprint(student)
                     pass
                     
                  else:
                     fp.write(json.dumps(student)+'\n')

               except StudentNotFoundError as err:
                  print(err)
                  
   except RollError as err:
      print(err)