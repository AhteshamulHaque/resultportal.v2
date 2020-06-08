from flask import Blueprint, jsonify, request, current_app
from flask_restful import reqparse, Resource
from errors import RollError
from util import parse_roll
from flask_jwt_extended import create_access_token
from pymysql.cursors import DictCursor

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
class StudentLoginAuthentication(Resource):
   
   # argument required for the post route
   parser = reqparse.RequestParser()
   parser.add_argument('roll', location='json', required=True)
   
   def post(self):
      args = self.parser.parse_args()
      roll = args['roll'].upper()

      # this try except exists because if someone gave a roll which could not
      # be split to year, roll, course, branch for example: 'not-a-valid-roll'
      try:
         year, course, branch = parse_roll(roll)
      except RollError as error:
         return { 'message': str(error) }, 404

      conn = current_app.extensions['mysql'].connect()
      cursor = conn.cursor(cursor=DictCursor)
      
      try:
         cursor.execute("SELECT semesters FROM nilekrator${year}.metadata WHERE name='{course}_{branch}'".format(
               year=year,
               course=course,
               branch=branch
         ))

         semesters = cursor.fetchone()['semesters'].split(',')
         # The below line guarantees that the semesters are in decreasing order
         semesters = sorted(semesters, reverse=True)

         # this is always the last semester given....used to show result prediction
         cursor.execute("SELECT student_name, image_link  FROM nilekrator${year}.{course}_{branch}_{semester} INNER JOIN nilekrator$admin.users USING(roll) WHERE roll='{roll}'".format(
         year=year, course=course,
         branch=branch, semester=semesters[-1],
         roll=roll
         ))
         name, image_id = cursor.fetchone().values()
         
      finally:
         conn.commit()
         conn.close()
      
      student_jwt_data = {
         'roll': roll,
         'name': name,
         'semesters': semesters,
         'latest_semester': semesters[-1],
         'year': year,
         'course': course,
         'branch': branch,
         'image_link': image_id,
      }
      
      return jsonify(access_token=create_access_token(student_jwt_data))
   


class AdminLoginAuthentication(Resource):
   
   # argument required for the post route
   parser = reqparse.RequestParser()
   parser.add_argument('password', location='json', required=True)
   
   def post(self):
      args = self.parser.parse_args()
      password = args['password']

      if password == 'this-is-a-password':
         return jsonify(access_token=create_access_token({'username': 'admin'}))
      else:
         return jsonify(msg="Invalid password"), 401