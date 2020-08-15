def register_config_parser(subparsers):
   # command to handle config options
   config_parser = subparsers.add_parser('config', help='Sets up configuration for the program before use')
   config_parser.add_argument('-s', '--set', metavar='key=value', help='(key=value) pair to add to the environment')
   config_parser.add_argument('-i', '--init', metavar='', help='initialse necessary variables')
   config_parser.add_argument('-l', '--list', metavar='', help='lists all variable\'s')
   config_parser.add_argument('-c', '--clear', metavar='', help='for testing purpose')

   # TODO: config_parser action goes here
   return config_parser

def execute_config_cmd(args):
   print("Config cmd executing")