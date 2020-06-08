import re
from errors import RollError

def parse_roll(roll):
   
   roll = roll.lower()
   roll_regex = re.compile(r'^2\d{3}(UG|PG)\w{2,4}\d{1,3}|TYC\d\d\w{2,4}\d{1,3}$', re.IGNORECASE)
   
   # if the roll number is not a valid roll
   # raise RollError
   if not re.match(roll_regex, roll):
      raise RollError('{} is not a valid roll'.format(roll))
   
   # parse roll for UG|PG|TYC
   if 'tyc' in roll:
      year = '20'+roll[3:5]
      course = 'tyc'
      branch = re.sub(r'\d+', '',roll[5:])
   else:
      year = roll[:4]
      course = roll[4:6]
      branch = re.sub(r'\d+$', '', roll[6:])

   return year, course, branch