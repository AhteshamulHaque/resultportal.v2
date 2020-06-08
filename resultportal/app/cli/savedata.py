import json
from util import parse_roll
import warnings

def executeStatementSafely(stmt, cursor):
   
   try:
      cursor.execute(stmt)
   except Exception as error:
      
      error_stmt = {
         'statement': stmt, 
         'error': error
      }
      with open('mysqlerror.json', 'a') as fp:
         fp.write( json.dumps(error_stmt) + '\n')      


def return_zero_if_empty(string):
    if not string:
        return 0
    else:
        try:    # person may be absent so it is found that the table cell is filled with ABS, references 2017ugpi042
            return float(string)
        except ValueError:
            return 0


def SaveData(fp, cursor):
   
   warnings.filterwarnings('ignore')
      
   # first create skeleton of every database and its table
   # This is done so that it is not created in every iteration of a student data
   # TODO: create possible database and their tables
   
   for line in fp:
      student = json.loads(line)
      year, course, branch = parse_roll(student['roll'])
      
      # insert the student data into nilekrato$admin.users table
      stmt = "INSERT INTO nilekrator$admin.users(regno, student_name, student_id) VALUES('{regno}', '{student_name}', '{student_id}')".format(
         regno=student['regno'],
         student_name=student['student_name'],
         student_id=student['student_id']
      )
      executeStatementSafely(stmt, cursor)
      
      # create the student year database(eg: nilekrator$2016) if not present
      stmt = "CREATE DATABASE IF NOT EXISTS nilekrator${year}".format(year=year)
      executeStatementSafely(stmt, cursor)
      
      # create the metadata table
      stmt = '''CREATE TABLE nilekrator${year}.metadata(
            branch_name varchar(20) PRIMARY KEY,
            session varchar(15),
            publish_date varchar(15),
            semester int,
            scheme varchar(10),
            degree varchar(15)
         )'''.format(year=year)
      executeStatementSafely(stmt, cursor)
      
      # try to insert metadata information
      stmt = '''INSERT IGNORE INTO nilekrator${year}.metadata VALUES('{branch_name}', '{session}', '{publish_date}', '{semester}', '{scheme}', '{degree}')'''.format(
         year=year,
         branch_name=course+'_'+branch+'_'+student['semester'],
         session=student['session'],
         publish_date=student['publish_date'],
         semester=student['semester'],
         scheme=student['scheme'],
         degree=student['degree']
      )
      executeStatementSafely(stmt, cursor)

      # create the sgpa, cgpa table
      stmt = '''CREATE TABLE nilekrator${year}.{course}_{branch}_{semester} (
            regno varchar(20) PRIMARY KEY,
            cgpa float(5,2) DEFAULT NULL,
            sgpa float(5,2) DEFAULT NULL,
            result_status enum('PASS','FAIL') DEFAULT NULL,
            pdf_link varchar(200),
            FOREIGN KEY regno REFERENCES nilekrator$admin.users(regno) ON DELETE CASCADE
         )'''
      executeStatementSafely(stmt, cursor)
      
      # insert cgpa and sgpa data
      stmt = '''INSERT INTO nilekrator${year}.{course}_{branch}_{semester} (regno, cgpa, sgpa, result_status) VALUES({regno}, {cgpa}, {sgpa}, {result_status})'''.format(
         year=year,
         course=course,
         branch=branch,
         semester=student['semester'],
         regno=student['regno'],
         cgpa=student['cgpa'],
         sgpa=student['sgpa'],
         result_status=student['result_status']            
      )
      executeStatementSafely(stmt, cursor)
      
      # create result table result_ug_cs_3
      stmt = '''CREATE TABLE result_{course}_{branch}_{semester} (
            regno varchar(20) DEFAULT NULL,
            subject_code varchar(10) DEFAULT NULL,
            end_sem float(5,2) DEFAULT NULL,
            test_1 float(5,2) DEFAULT NULL,
            test_2 float(5,2) DEFAULT NULL,
            grade varchar(7) DEFAULT NULL,
            total float(5,2) DEFAULT NULL,
            assignment float(5,2) DEFAULT NULL,
            quiz_avg float(5,2) DEFAULT NULL,
            FOREIGN KEY regno REFERENCES nilekrator$admin.users(regno) ON DELETE CASCADE
            )'''
      executeStatementSafely(stmt, cursor)


      #insert student in result_ug_cs_3
      for subject_code in student['result']:
         stmt = "INSERT INTO nilekrator${year}.{course}_{branch}_{semester} VALUES('{regno}', '{code}', {end_sem}, {test_1:.2f}, {test_2:.2f}, '{grade}', {total}, {assignment}, {quiz_avg} )".format(
            year=year,
            course=course,
            branch=branch,
            semester=student['semester'],
            regno=student['regno'],
            code=subject_code,
            end_sem=return_zero_if_empty( student['result'][subject_code]['end_sem'] ),
            test_1=return_zero_if_empty( student['result'][subject_code]['test_1'] ),
            test_2=return_zero_if_empty( student['result'][subject_code]['test_2'] ),
            grade=student['result'][subject_code]['grade'],
            total=return_zero_if_empty( student['result'][subject_code]['total'] ),
            assignment=return_zero_if_empty( student['result'][subject_code]['assignment'] ),
            quiz_avg=return_zero_if_empty( student['result'][subject_code]['quiz_avg'] ),
         )
         executeStatementSafely(stmt, cursor)

         cursor.execute("INSERT IGNORE INTO nilekrator$ADMIN.subjects VALUES('{code}','{name}')".format(
            code=subject_code,
            name=student['result'][subject_code]['subject']
         ))
         executeStatementSafely(stmt, cursor)