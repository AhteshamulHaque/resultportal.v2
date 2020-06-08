#!/bin/python3
import argparse

# import program subcommands and their associated arguments and logic
# to execute when they are called
# these are function names to register with the program
from commands import (
      # subcommands options and arguments
      register_config_parser, register_student_parser, register_log_parser,
      register_image_parser, register_pdf_parser, register_rank_parser,
      register_scraper_parser, register_verify_parser,
      
      # subcommands logic to execute
      execute_config_cmd, execute_student_cmd, execute_log_cmd,
      execute_image_cmd, execute_pdf_cmd, execute_rank_cmd,
      execute_scrape_cmd, execute_verify_cmd
   )

def main():
   # Defines rpf metadata such as description, usage, etc
   parser = argparse.ArgumentParser(
            prog='rpf',
            description='CLI program for managing result portal'
         )
   parser.add_argument('-v', '--verbose', help='Detailed output of the operations')

   # add all the subparsers to the main program
   subparsers = parser.add_subparsers(dest='cmd', help='sub-commands', required=True)
   register_config_parser(subparsers)
   register_student_parser(subparsers)
   register_log_parser(subparsers)
   register_image_parser(subparsers)
   register_pdf_parser(subparsers)
   register_rank_parser(subparsers)
   register_scraper_parser(subparsers)
   register_verify_parser(subparsers)

   args = parser.parse_args()
   exe_cmd = {
      'config': execute_config_cmd,
      'student': execute_student_cmd,
      'log': execute_log_cmd,
      'image': execute_image_cmd,
      'pdf': execute_pdf_cmd,
      'rank': execute_rank_cmd,
      'scraper': execute_scrape_cmd,
      'verify': execute_verify_cmd
   }

   exe_cmd.get(args.cmd)(args)
   print('\n', '\n', args)

if __name__ == '__main__':
   main()