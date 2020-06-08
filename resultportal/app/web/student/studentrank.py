from collections import namedtuple
import pymysql as mysql
import os

student = namedtuple('student', 'roll name gpa image_id')
credit  = namedtuple('credits', 'code credits')

class StudentRank:

	def __init__(self, method, year, course, branch, semester, cursor):
		self.method = method
		self.semester = semester
		self.year = year
		self.course = course
		self.branch = branch
		self.student_rank = list()
		self.subject_scores = dict()
		self.cursor = cursor


	def get_failed_once(self):
		self.cursor.execute("SELECT roll, student_name, {method}, image_link FROM nilekrator${year}.{course}_{branch}_{semester} INNER JOIN nilekrator$admin.users USING(roll)  WHERE {method} = 0 ORDER BY {method} DESC".format(
			year=self.year,
            course=self.course,
            branch=self.branch,
            semester=self.semester,
            method=self.method,
		))
		return self.cursor.fetchall()


	def get_raw_rank(self):
		self.cursor.execute("SELECT roll,student_name, {method}, image_link FROM nilekrator${year}.{course}_{branch}_{semester} INNER JOIN nilekrator$admin.users USING(roll)  WHERE {method} <> 0 ORDER BY {method} DESC".format(
            year=self.year,
            course=self.course,
            branch=self.branch,
            semester=self.semester,
            method=self.method,
        ))

	    # here the student is ranked but the same cgpa, sgpa are not ranked
		self.student_rank = [ student(*i) for i in self.cursor ]

		self.cursor.execute("SELECT roll, subject_code, total FROM nilekrator${year}.result_{course}_{branch}_{semester}".format(
		    year=self.year,
		    course=self.course,
		    branch=self.branch,
		    semester=self.semester
		))

		# get marks to build the rank for same cgpa, sgpa students
		# I made a dictionary because it will be easy to reference the marks
		# in case they are not arranged according to code...can't take the risk...can
		# generate wrong results
		for i in self.cursor:
			if self.subject_scores.get(i[0]):
				self.subject_scores[i[0]][i[1]] = i[2]
			else:
				self.subject_scores[i[0]] = {}
				self.subject_scores[i[0]][i[1]] = i[2]

		try:
		    self.cursor.execute('''SELECT subject_code, credits FROM nilekrator$admin.subjects.{course}_{branch} WHERE subject_code
		        IN (SELECT DISTINCT subject_code FROM nilekrator${year}.result_{course}_{branch}_{semester}) ORDER BY credits DESC'''.format(
		        course=self.course,
		        branch=self.branch,
		        year=self.year,
		        semester=self.semester
		    ))

		    self.credits = [ credit(*i) for i in self.cursor ]
		except:
		    self.credits = ()


		for i in range( len(self.student_rank) ):
			marks = []

			# if credits happen to be missing select all the marks from the roll dictionary
			if self.credits:
				for credit in self.credits:
					marks.append( self.subject_scores[ self.student_rank[i].roll ][credit.code] )
			else:
				for mark in self.subject_scores[ self.student_rank[i].roll ]:
					marks.append( self.subject_scores[ self.student_rank[i].roll ][mark] )

			self.student_rank[i] = [ self.student_rank[i].roll, self.student_rank[i].name,
										(self.student_rank[i].gpa, *marks), self.student_rank[i].image_id
									]

		self.student_rank = sorted(self.student_rank, key=lambda a: a[2], reverse=True)


	def get_original_rank(self):

		RANK = 0
		previous_tuple = ()

		limit = len(self.student_rank)

		for i in range( limit ):

			if self.student_rank[i][2] != previous_tuple:
				RANK += 1

			self.student_rank[i].append(RANK)
			previous_tuple = self.student_rank[i][2]

		return self.student_rank

if __name__ == '__main__':

	DBs = ["2015", "2016", "2017", "2018"]
	conn = mysql.connect(os.getenv('MYSQL_DATABASE_HOST', 'localhost'), os.getenv('MYSQL_DATABASE_USER', 'root'), os.getenv('MYSQL_DATABASE_PASSWORD', 'password'))
	cursor = conn.cursor()

	for year in DBs:
		print("Ranking for", year)

		cursor.execute("SELECT CONCAT( name, '_', SUBSTRING_INDEX(semesters,',', -1)) FROM nilekrator${}.metadata WHERE scheme IS NULL AND session IS NULL".format(year))

		BRANCH = cursor.fetchall()

		for branch in BRANCH:
			course, branch, semester = branch[0].split('_')

			S = StudentRank('cgpa', year, course, branch, semester, cursor)

			result = S.get_failed_once()

			for stu in result:
				print(stu[0], "failed")
				cursor.execute("UPDATE nilekrator$ADMIN.USERS SET rank=0 WHERE roll='{}'".format(
					stu[0]
				))

			S.get_raw_rank()

			for stu in S.get_original_rank():
				print(stu[0], "ranked", stu[-1])
				cursor.execute("UPDATE nilekrator$admin.users SET rank={} WHERE roll='{}'".format(
					stu[-1], stu[0]
				))

		print()

	conn.commit()
	conn.close()