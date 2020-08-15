from bs4 import BeautifulSoup
from errors import StudentNotFoundError, RollError
from argparse import ArgumentTypeError
import requests
import random
import re
import os
# TODO: Add functionality to scrape __VIEWSTATE first for remote scraping 
# url = 'http://14.139.205.172/web_new/Default.aspx'

def _parse_result_table(result_table):
   '''
      input: bs4 parsed html table
      return: a dictionary of result table extracted from scraping
   '''
   trs = result_table.find_all("table")[0].find_all("tr", recursive=False)[1:]

   result = {}
   headers = ['', 'subject', 'test_1', 'test_2','assignment', 'quiz_avg', 'end_sem', 'total', 'grade']
   code = ''

   for tr in trs:
      tds = tr.find_all("td", recursive=False)
      
      for i,td in enumerate(tds):
         if i == 0:
            code = td.text.strip()
            result[code] = dict()
         else:
            result[code][headers[i]] = td.text.strip()

   return result

def _first_request(url, regno, semester=None):
   '''
      return: [ valid_semesters, form_data ]
   '''
   
   post_data = {
      "ToolkitScriptManager1_HiddenField" :"",
      "__EVENTTARGET": "",
      "__EVENTARGUMENT": "",
      # always first manually/automatically set _VIEWSTATE
      "__VIEWSTATE": "/wEPDwULLTE5MTk3NDAxNjkPZBYCAgEPZBYCAicPZBYEAhIPFCsAAmRkZAIUD2QWAgIDDxQrAAJkZGQYAwUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgQFCmJ0bmltZ1Nob3cFEGJ0bmltZ1Nob3dSZXN1bHQFC2J0bkltZ1ByaW50BQxidG5pbWdDYW5jZWwFCWx2QmFja2xvZw9nZAUQbHZTdWJqZWN0RGV0YWlscw9nZEM0w+4vgN3bILbO4Zuep/+vlVWU",
      "__VIEWSTATEGENERATOR" :"011071C8",
      "txtRegno": "{}".format(regno),
      "btnimgShow.x": str(random.randint(1, 99)),
      "btnimgShow.y": str(random.randint(1, 99)),
      "ddlSemester": "0",
      "hfldno": "",
      "hdfidno": ""
   }
   
   resp = requests.post(url, post_data)      
   data = resp.text

   if "alert('Student Not Available or Result Yet not Published.')" in data:
      # Student with this regno does not exists
      raise StudentNotFoundError('%s does not exists'%regno)
   
   # parse the html data and extract valid semesters
   soup = BeautifulSoup(data, 'lxml')
   
   valid_sems = soup.find_all("option", attrs={"value": re.compile(r'[123456789]')})
   valid_sems = [ _['value'] for _ in valid_sems ]

   # if no semester is supplied default to the last semester
   if semester == None:
      semester = valid_sems[-1]
   
   # change to str in case semester is passed as an integer
   semester = str(semester)
   
   # supplied semester is not a valid semester
   # happens when some semester is not present for some rolls but
   # present for other rolls
   if semester not in valid_sems:
      raise StudentNotFoundError("Result for semester %s does not exists %s"%(semester,valid_sems) )
   
   form_vars = [ "ToolkitScriptManager1_HiddenField", "__EVENTTARGET", "__EVENTARGUMENT",
   "__VIEWSTATE", "__VIEWSTATEGENERATOR", "hfIdno", "hdfidno" ]

   form_data = {}

   for var in form_vars:
      try:
         form_data[var] = soup.find("input", attrs={"id": var})['value']
      except:
         form_data[var] = ""

   form_data["txtRegno"] = regno
   form_data["btnimgShowResult.x"] = str(random.randint(1,100))
   form_data["btnimgShowResult.y"] = str(random.randint(1,100))
   form_data["ddlSemester"] = semester # setting the semester for `second call response`

   return valid_sems, form_data


def _second_request_for_result(url, post_data):
   '''
      return: a dictionary of student data
   '''
   
   resp = requests.post(url, post_data)
   data = resp.text

   soup = BeautifulSoup(data, 'lxml')

   student = {}

   student['regno'] = soup.find('span',attrs={'id':'lblRollNo'}).text
   student['session'] = soup.find("span", attrs={"id": "lblsession"}).text
   student['degree'] = soup.find("span", attrs={"id": "lblDegreeName"}).text
   student['scheme'] = soup.find("span", attrs={"id": "lblSchemetype"}).text

   student['student_name'] = soup.find("span", attrs={"id": "lblStudentName"}).text
   student['branch'] = soup.find("span", attrs={"id": "lblBranchName"}).text
   student['semester'] = post_data['ddlSemester']

   student['result_status'] = soup.find("span", attrs={"id": "lblResult"}).text
   student['sgpa'] = soup.find("span", attrs={"id": "lblSPI"}).text
   student['cgpa'] = soup.find("span", attrs={"id": "lblCPI"}).text

   student['publish_date'] = soup.find("span", attrs={"id": "lblPublishDate"}).text
   student['student_id'] = soup.find("input", attrs={"id": "hfIdno"})['value']

   student['result'] = _parse_result_table(soup.find("div",attrs={"id": "PnlShowResult"}).find_all("tr")[5])

   return student


def get_pdf(regno, student_id, semester, log, url):
   '''
      Downloads and save the pdf in pdfs directory
   '''
   # regno is used in filename so to update the database
   # easily, can use student_id in place of regno but
   # database updation steps will increase
   filename = '%s_%s'%(regno, semester)
   filepath = os.path.join('pdfs', filename)
   
   if not os.path.exists('pdfs'):
      log.debug('Creating folder pdfs')
      os.makedirs('pdfs')

   if os.path.exists(filepath):
      log.warning('pdf for regno=%s, semester=%s already exists', regno, semester)
      return

   url= url.format(student_id, semester)
   log.debug('Requesting to %s', url)
   
   try:
      resp = requests.get(url)
      with open(filepath, 'wb') as fp:
         fp.write(resp.content)
      log.info('Downloaded pdf for regno=%s, semester=%s', regno, semester)
   except Exception:
      log.error('Failed to download pdf for regno=%s, semester=%s', regno, semester)
   
   return resp.content


def get_result(regno, url, semester=None):
   '''
      This calls [ _first_call_response, _second_call_response ] to fetch a particular result
      It also downloads the result pdf also. This is to save time by not making the same two calls
      again.
   '''

   _, form_data = _first_request(url, regno, semester)
   
   # means no student found with the specified regno
   if _ == None:
      raise StudentNotFoundError('%s does not exists'%regno)
   
   student = _second_request_for_result(url, form_data)
   return student
    
   
def get_semesters(regno, url):
   valid_sems, _ = _first_request(url, regno)
   return valid_sems
   
def valid_range(_range):
   '''
      This method check if the range is composed of valid registration number
      by internally calling valid_regno
   '''
   start, end = _range.split('-')
   
   valid_regno(start)
   valid_regno(end)
   
   return [start, end]    
   
      
def valid_regno(regno):
   '''
      This method check if the regno is a valid registration number
      by checking it against a regex
      -> Raises Error if not a valid regno
   '''
   regno_regex = re.compile(r'^2\d{3}(UG|PG)\w{2,4}\d{1,3}|TYC\d\d\w{2,4}\d{1,3}$', re.IGNORECASE)
   
   if re.match(regno_regex, regno):
      return regno
   else:
      raise ArgumentTypeError('%s is not a valid registration number'%regno)

   
def split_regno(regno):
   '''
      After the valid_regno function is True this function is called
      to split the regno in three parts (year, course, branch)
   '''
   if 'TYC' in regno:
      year = '20'+regno[3:5]
      course = 'TYC'
      branch = re.sub(r'\d+$', '',regno[5:]).upper()
   else:
      year = regno[:4]
      course = regno[4:6]
      branch = re.sub(r'\d+$', '', regno[6:]).upper()

   return year, course, branch


def regno_from_opts(year, course, branch, roll):
   
   year = str(year)
   regno = ''
   
   if course == 'TYC':
      regno = ''.join([course, year[2:], branch, "%02d"%roll])
   elif course == 'PG':
      regno = ''.join([year, course, branch, "%02d"%roll])
   else:
      regno = ''.join([year, course, branch, "%03d"%roll])

   return regno