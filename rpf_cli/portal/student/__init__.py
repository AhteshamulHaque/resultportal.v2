def register_student_parser(subparsers):
   student_parser = subparsers.add_parser('student', help='Queries student related info')
   # Returns roll and their corresponding names
   student_parser.add_argument('-s', '--search', help='get matching [name]')
   student_parser.add_argument('-r', '--roll', help='[roll] to query')
   student_parser.add_argument('-u', '--usage', help='usage history of [roll]') 
   student_parser.add_argument('-l', '--logins', help='login history of [roll]')

   # TODO: mutually exclusive arguments
   stu_arg_grp = student_parser.add_mutually_exclusive_group()
   stu_arg_grp.add_argument('-b', '--blacklist', help='blacklist a [roll]')
   stu_arg_grp.add_argument('-w', '--whitelist', help='whitelist a [roll]')

   return student_parser

def execute_student_cmd(args):
   print("Executing student cmd")