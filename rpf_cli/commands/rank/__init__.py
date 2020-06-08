def register_rank_parser(subparsers):
   # TODO: incomplete rank parser
   rank_parser = subparsers.add_parser('rank', help='Update the rank of students')
   rank_parser.add_argument('-a', '--all', help='Update everyone\'s rank')
   rank_parser.add_argument('-p', '--parse-from-roll', help='Update rank for [roll]')

def execute_rank_cmd(args):
   print("Rank cmd executing")
