import requests
import random, re
from bs4 import BeautifulSoup
from collections import OrderedDict
from errors import StudentNotFoundError, RollError
# TODO: Add functionality to scrape __VIEWSTATE first for remote scraping 

# url = 'http://14.139.205.172/web_new/Default.aspx'
url = 'http://localhost:3000/'

class StudentResultDownloader:
      
   @staticmethod
   def first_call_response(regno, semester=None):
      '''
         parameters: 
            regno -> str
            semester -> str 
         return: [ valid_semesters, form_data ]
      '''
      global url

      post_data = {
         "ToolkitScriptManager1_HiddenField" :"",
         "__EVENTTARGET": "",
         "__EVENTARGUMENT": "",
         # always first manually set viewstate
         "__VIEWSTATE": "/wEPDwULLTE5MTk3NDAxNjkPZBYCAgMPZBYEAgMPFCsAAmQQFgAWABYAZAIqD2QWBAISDxQrAAJkZGQCFA9kFgICAw8UKwACZGRkGAMFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYEBQpidG5pbWdTaG93BRBidG5pbWdTaG93UmVzdWx0BQtidG5JbWdQcmludAUMYnRuaW1nQ2FuY2VsBQlsdkJhY2tsb2cPZ2QFEGx2U3ViamVjdERldGFpbHMPZ2RRUBQxFvIgVfx50k5f51Z0VJON3rlAmXJvDT2YJxv0oA==",
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

      if "alert('Student Not Available or Result Yet not Published.')" in resp:
         return None, None  # ResultFetcher with this regno does not exists

      # parse the html data and extract valid semesters
      soup = BeautifulSoup(data, 'lxml')
      
      valid_sems = soup.find_all("option", attrs={"value": re.compile(r'[123456789]')})
      valid_sems = [ _['value'] for _ in valid_sems ]

      # if no semester is supplied default to the last semester
      if semester == None:
         semester = valid_sems[-1]
         
      # supplied semester is not a valid semester
      if semester not in valid_sems:
         raise KeyError("%s not in %s"%(semester,valid_sems) )
      
      form_vars = [ "ToolkitScriptManager1_HiddenField", "__EVENTTARGET", "__EVENTARGUMENT",
      "__VIEWSTATE", "__VIEWSTATEGENERATOR", "hfIdno", "hdfidno" ]

      form_data = OrderedDict()

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


   @staticmethod
   def second_call_response(post_data):
      '''
         return: a dictionary of student data
      '''
      global url
      
      resp = requests.post(url, post_data)
      data = resp.text

      soup = BeautifulSoup(data, 'lxml')

      student = OrderedDict()

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

      student['result'] = StudentResultDownloader.parse_result_table(soup.find("div",attrs={"id": "PnlShowResult"}).find_all("tr")[5])
      # student['given_regno'] = self.regno

      return student

   @staticmethod
   def parse_result_table(result_table):
      '''
         return: a dictionary of result table extracted from scraping
      '''
      trs = result_table.find_all("table")[0].find_all("tr", recursive=False)[1:]

      result = OrderedDict()
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
   
   
   @staticmethod
   def download_result(regno, semester=None):
      '''
         The regno is valid and uppercased. semester can be invalid but str.
         This calls [ first_call_response, second_call_response ] to fetch a particular result
      '''
      
      _, form_data = StudentResultDownloader.first_call_response(regno, semester)
      
      # means no student found with the specified regno
      if _ == None:
         raise StudentNotFoundError('%s does not exists'%regno)
      
      student = StudentResultDownloader.second_call_response(form_data)
      return student
    
   
def get_semesters(regno):
   valid_sems, _ = StudentResultDownloader.first_call_response(regno)
   return valid_sems
   
      
def valid_regno(regno):
   '''
      This method check if the regno is a valid registration number
      by checking it against a regex
      -> Raises Error if not a valid regno
   '''
   regno_regex = re.compile(r'^2\d{3}(UG|PG)\w{2,4}\d{1,3}|TYC\d\d\w{2,4}\d{1,3}$', re.IGNORECASE)
   
   if re.match(regno_regex, regno):
      return True
   else:
      raise RollError('%s is not a valid registration number'%regno)

   
def parse_regno(regno):
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


def regno_from_opts(year, course, branch, regno):
   
   year = str(year)
   
   reg_no = ''
   if course == 'TYC':
      reg_no = ''.join([course, year[2:], branch, "%02d"%regno])
   elif course == 'PG':
      reg_no = ''.join([year, course, branch, "%02d"%regno])
   else:
      reg_no = ''.join([year, course, branch, "%03d"%regno])

   return reg_no