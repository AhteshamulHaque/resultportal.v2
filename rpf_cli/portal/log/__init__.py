def register_log_parser(subparsers):
   log_parser = subparsers.add_parser('logs', help='Fetches result and feedback logs')
   log_parser.add_argument('-s', '--stream', choices=['feedback', 'resultportal'], help='stream either ["feedback","resultportal"] log')
   log_parser.add_argument('-l', '--log-level', choices=['debug', 'info', 'warn', 'error'], help='stream <level> of log')
   log_parser.add_argument('-H', '--head', help='fetches `num` number of logs from beginning')
   log_parser.add_argument('-t', '--tail', help='fetches `num` number of logs from end')

   return log_parser

def execute_log_cmd(args):
   print("Log cmd executing")
