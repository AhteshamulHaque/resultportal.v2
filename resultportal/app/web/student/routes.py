from flask import current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_current_user
from collections import OrderedDict
import os
from random import randint
from app.student.studentrank import StudentRank

# TODO: check for data integrity
############################################ profile ######################################################
class StudentProfile(Resource):
   
   @jwt_required
   def get(self):
   
      try:
         
         user = get_current_user()
         
         conn = current_app.extensions['mysql'].connect()
         cursor = conn.cursor()
         result_array = []
         
         isStudentFailed = False

         for semester in user['semesters']:
            # this try-except because some has more result than the others like one has 3, 4 semesters other
            # may have 2, 3, 4 semester
            single_result = {}
            
            cursor.execute('''SELECT subject_code, subject_name, end_sem, test_1, test_2, grade, total, assignment, quiz_avg
                  FROM nilekrator${year}.result_{course}_{branch}_{semester} INNER JOIN nilekrator$admin.subjects USING(subject_code)
                  WHERE roll='{roll}' '''.format(
                  year=user['year'],
                  course=user['course'],
                  branch=user['branch'],
                  semester=semester,
                  roll=user['roll']
            ))

            # if there are result to iterate
            if cursor.rowcount != 0:
               single_result['semester'] = semester
               single_result['result'] = []

               for _ in range(cursor.rowcount):
                  code, subject_name, end_sem, test_1, test_2, grade, total, assignment, quiz_avg = cursor.fetchone()
                  single_result['result'].append({
                     'subject_code': code,
                     'subject_name': subject_name,
                     'test_1': test_1,
                     'test_2': test_2,
                     'grade': grade,
                     'total': total,
                     'end_sem': end_sem,
                     'assignment': assignment,
                     'quiz_avg': quiz_avg
                  })

               cursor.execute("SELECT cgpa, sgpa, result_status FROM nilekrator${year}.{course}_{branch}_{semester} WHERE roll='{roll}'".format(
                     year=user['year'],
                     course=user['course'],
                     branch=user['branch'],
                     semester=semester,
                     roll=user['roll']
               ))

               cgpa, sgpa, result_status = cursor.fetchone()

               if cgpa == 0:
                     isStudentFailed = True

               cursor.execute("SELECT publish_date FROM nilekrator${year}.metadata WHERE name='{course}_{branch}_{semester}'".format(
                     course=user['course'],
                     year=user['year'],
                     branch=user['branch'],
                     semester=semester
               ))
               publish_date, = cursor.fetchone() # because cursor.fetchone() is (x, )

               single_result['cgpa'] = cgpa
               single_result['sgpa'] = sgpa
               single_result['result_status'] = result_status
               single_result['publish_date'] = publish_date
               
               result_array.append(single_result)
               # end of for loop
            # end of if loop
         
         cursor.execute("SELECT position FROM nilekrator$admin.users WHERE roll='{}'".format(user['roll']))
         position = cursor.fetchone()[0]
         
      finally:
         conn.close()
         
      return { 'data': { 'result': result_array, 'rank': position, 'fail': isStudentFailed } }

############################################## compare ##############################################3
class StudentCompare(Resource):
   
   @jwt_required
   def get(self):
      
      user = get_current_user()
      parser = reqparse.RequestParser()
      parser.add_argument('semester', choices=map(str, range(1, 10)), default=user['latest_semester'], location='args', help='Semester number for the results to compare')
      args = parser.parse_args()
      semester = args['semester']
      
      conn = current_app.extensions['mysql'].connect()
      cursor = conn.cursor()
      
      try:
         cursor.execute("SELECT student_name, e.roll, image_link FROM nilekrator${year}.{course}_{branch}_{semester} e INNER JOIN nilekrator$admin.users d ON e.roll = d.roll WHERE e.roll != '{roll}'".format(
            roll=user['roll'],
            year=user['year'],
            course=user['course'],
            branch=user['branch'],
            semester=semester
         ))

         students = cursor.fetchall()
      finally:
         conn.close()
         
      return { 'data': { 'students': students } }

   # here rolls are passed from post request for actual generation of comparision table
   @jwt_required
   def post(self):

      user = get_current_user()
      
      parser = reqparse.RequestParser()
      parser.add_argument('semester', choices=map(str, range(1, 10)), default=user['latest_semester'], location='json', help='Semester number for the results to compare')
      parser.add_argument('rolls', type=list, location='json', help='List of rolls to compare')
      args = parser.parse_args()
      
      semester = args['semester']
      rolls = args['rolls']
      
      conn = current_app.extensions['mysql'].connect()
      cursor = conn.cursor()

      subject_map = {}
      # your result
      # user data is selected from four tables users, ug_cs(for cgpa, sgpa), result_ug_cs, subjects(for subject name)
      cursor.execute('''SELECT roll, student_name, subject_name, subject_code, total, cgpa, sgpa FROM nilekrator${year}.{course}_{branch}_{semester}
         INNER JOIN (SELECT * FROM nilekrator$admin.subjects INNER JOIN (SELECT * FROM nilekrator${year}.result_{course}_{branch}_{semester}
         INNER JOIN nilekrator$admin.users USING(roll) WHERE roll='{roll}') s USING(subject_code)) d USING(roll)'''.format(
         year=user['year'],
         course=user['course'],
         branch=user['branch'],
         semester=semester,
         roll=user['roll']
      ))

      me = cursor.fetchall()

      # making subject map for line chart
      for stu in me:
         subject_map[stu[3]] = stu[2]

      cursor.execute('''SELECT roll, name, subject_name, subject_code, total, cgpa, sgpa from nilekrator$_{year}.{course}_{branch}_{semester}
         INNER JOIN (SELECT * FROM nilekrator$ADMIN.SUBJECTS INNER JOIN (SELECT *  FROM nilekrator$_{year}.RESULT_{course}_{branch}_{semester}
         INNER JOIN nilekrator$admin.users USING(roll) WHERE roll in ({roll}) ) s USING(subject_code)) d using(roll)'''.format(
         year=user['year'],
         course=user['course'],
         branch=user['branch'],
         semester=semester,
         roll=",".join(rolls)
      ))

      others = cursor.fetchall()

      cursor.execute("SELECT publish_date FROM nilekrator$_{year}.CONF WHERE name='{course}_{branch}_{semester}'".format(
         course=user['course'],
         year=user['year'],
         branch=user['branch'],
         semester=semester
      ))

      publish_date = cursor.fetchone()[0]

      conn.close()

      return {
         'data': {
            'me': me,
            'others': others,
            'semester': semester,
            'publish_date': publish_date,
            'subject_map': subject_map
         }
      }

########################################## stats ##################################################
class StudentStatistics(Resource):
   
   @jwt_required
   def get(self):
      
      user = get_current_user()
      
      conn = current_app.extensions['mysql'].connect()
      cursor = conn.cursor()
      
      data = []
      
      try:
         for semester in user['semesters']:
            cursor.execute("SELECT cgpa, sgpa FROM nilekrator${year}.{course}_{branch}_{semester} WHERE roll='{roll}'".format(
               year=user['year'],
               course=user['course'],
               branch=user['branch'],
               semester=semester,
               roll=user['roll']
            ))

            cgpa, sgpa = cursor.fetchone()
            
            data.append({
               'semester': semester,
               'cgpa': cgpa,
               'sgpa': sgpa
            })
            
      finally:
         conn.close()
         
      return { 'data': data }


############################################# rank page ##############################################
class StudentRankList(Resource):
   @jwt_required
   def get(self):

      user = get_current_user()
      
      parser = reqparse.RequestParser()
      parser.add_argument('method', choices=['sgpa', 'cgpa'], default='cgpa')
      parser.add_argument('semester', choices=map(str, range(1, 10)), default=user['latest_semester'])
      parser.add_argument('failed', choices=[0, 1], default=1)
      
      args = parser.parse_args()

      method = args['method']
      semester = args['semester']
      
      try:
         conn = current_app.extensions['mysql'].connect()
         cursor = conn.cursor()
         Stu = StudentRank(method, user['year'], user['course'], user['branch'], semester, cursor)
         Stu.get_raw_rank()

      finally:
         conn.close()
         
      return {
         'data': {
            'failed_student': Stu.get_failed_once(),
            'pass_students': Stu.get_original_rank(),
            'semester': semester,
            'method': method
         }
      }


   ############################################# updaterank ##################################
   @jwt_required
   def post(self):

      user = get_current_user()
      
      conn = current_app.extensions['mysql'].connect()
      cursor = conn.cursor()

      semester = user['new_semester']

      S = StudentRank('cgpa', user['year'], user['course'], user['branch'], semester)

      result = S.get_failed_once()

      for stu in result:
         cursor.execute("UPDATE nilekrator$admin.users SET position=0 WHERE roll='{}'".format(stu[0]))

      S.get_raw_rank()

      for stu in S.get_original_rank(200):
         cursor.execute( "UPDATE nilekrator$admin.users SET position={} WHERE roll='{}'".format( stu[-1], stu[0]) )

      conn.close()
      return { 'message': 'Update Successfull'}

# The below routes will start with a /college
########################################### College Home ##############################################
class ListCollegeYears(Resource):
   
   @jwt_required
   def get(self):
      try:
         conn = current_app.extensions['mysql'].connect()
         cursor = conn.cursor()

         cursor.execute("SHOW DATABASES")

         result = cursor.fetchall()
         batch = []
         db_name = 'nilekrator$2'
         
         for res, in result:
            if res.startswith(db_name):
               batch.append(res[ len(db_name) :])

      finally:
         conn.close()
         
      return {'batch': batch }


class ListCollegeByYear(Resource):
   
   @jwt_required
   def get(self, year):
      
      try:
         conn = current_app.extensions['mysql'].connect()
         cursor = conn.cursor()

         cursor.execute("SELECT branch_name, degree FROM nilekrator${year}.metadata WHERE session IS NULL AND scheme IS NULL ORDER BY degree".format(
               year=year
         ))

         DEGREE = set()

         result = cursor.fetchall()

         for branch, degree in result:
            DEGREE.add(degree)
            
      finally:
         conn.close()
         
      return { 'degree': DEGREE , 'branch': branch }


class ListCollegeByYearCourseBranch(Resource):
   
   @jwt_required
   def get(self, year, course, branch):
      #actually all results are ranked and then limit records are rendered...fix this
      try:
         conn = current_app.extensions['mysql'].connect()
         cursor = conn.cursor()

         cursor.execute("SELECT SUBSTRING_INDEX(semesters,',',-1) FROM nilekrator${year}.metadata WHERE name='{course}_{branch}'".format(
            year=year,
            course=course,
            branch=branch
         ))

         semester, = cursor.fetchone()
         
      finally:
         conn.close()

         S = StudentRank('cgpa', year, course, branch, semester)
         S.get_raw_rank()

      return {
         'year': year,
         'course': course,
         'branch': branch,
         'ranklist': S.get_original_rank()
      }