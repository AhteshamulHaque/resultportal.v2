def register_verify_parser(subparsers):   
   # TODO: write verify_parser logic
   verify_parser = subparsers.add_parser('verify', help='Verified integrity of data scraped')

   return verify_parser

def execute_verify_cmd(args):
   print("Verify cmd executing")