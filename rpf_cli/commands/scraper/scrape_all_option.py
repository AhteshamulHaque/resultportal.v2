from commands.scraper.helpers import StudentResultDownloader, regno_from_opts
import json
from errors import StudentNotFoundError

START_YEAR = 2016
END_YEAR = 2019

UG_courses = ["CS", "EC", "EE", "MM", "ME", "CE", "PI"]
PG_courses = [
               "CACA", "CHCH", "MHMH", "PHPH", "MMFT",
               "MMMT", "CSCS", "CAIS", "METE", "MEES",
               "MECI", "MFMS", "CHSS", "CESE", "CEGE",
               "CEWR", "EEPE", "EEPS", "ECEM", "ECCO",
            ]
TYC_courses = [ "MME" ]

def execute():
   
   with open('result.json', 'a') as result_fp, open('missed.json', 'a') as missed_fp:
      
      for year in range(START_YEAR, END_YEAR+1):         
         for course, branches in [ ("UG", UG_courses), ("PG", PG_courses) ,("TYC", TYC_courses)]:
            for branch in branches:
               
               no_of_misses = 0
               
               for regno in range(1, 130):
                  
                  regno = regno_from_opts(year, course, branch, regno)
                  
                  try:
                     # write json student data to the file
                     student = StudentResultDownloader.download_result(regno)
                     no_of_misses = 0
                     result_fp.write(json.dumps(student)+'\n')
                     
                  except StudentNotFoundError as err:
                     # write missed regno to a file
                     print(err)
                     no_of_misses += 1
                     missed_fp.write(regno+'\n')                     
                     
                  if no_of_misses == 5:
                     break
                     