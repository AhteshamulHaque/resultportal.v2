#!/bin/python3
# import program subcommands and their associated
# arguments and logic to execute when they are called
# Note - Order of the arguments matter
from portal.config import register_config_parser, execute_config_cmd
from portal.student import register_student_parser, execute_student_cmd
from portal.log import register_log_parser, execute_log_cmd
from portal.image import register_image_parser, execute_image_cmd
from portal.pdf import register_pdf_parser, execute_pdf_cmd
from portal.rank import register_rank_parser, execute_rank_cmd
from portal.scraper import register_scraper_parser, execute_scrape_cmd
from portal.verify import register_verify_parser, execute_verify_cmd
import argparse
from collections import namedtuple

def main():
   # define rpf metadata such as description, usage, etc
   
   parser = argparse.ArgumentParser(
            prog='rpf',
            description='CLI program for managing result portal and feedback'
         )

   # add all the subparsers to the main program
   subparsers = parser.add_subparsers(dest='cmd', help='sub-commands')
   config_parser = register_config_parser(subparsers)
   student_parser = register_student_parser(subparsers)
   log_parser = register_log_parser(subparsers)
   image_parser = register_image_parser(subparsers)
   pdf_parser = register_pdf_parser(subparsers)
   rank_parser = register_rank_parser(subparsers)
   scraper_parser = register_scraper_parser(subparsers)
   verify_parser = register_verify_parser(subparsers)
   
   args = parser.parse_args()
   
   # create a named tuple to hold the execution function and its corresponding parser
   # parser is passed to the execution function so that a proper error can be raised
   Parser = namedtuple('parser', 'function parser')
   
   exe_cmd = {
      'config': Parser(execute_config_cmd, config_parser),
      'student': Parser(execute_student_cmd, student_parser),
      'log': Parser(execute_log_cmd, log_parser),
      'image': Parser(execute_image_cmd, image_parser),
      'pdf': Parser(execute_pdf_cmd, pdf_parser),
      'rank': Parser(execute_rank_cmd, rank_parser),
      'scraper': Parser(execute_scrape_cmd, scraper_parser),
      'verify': Parser(execute_verify_cmd, verify_parser)
   }

   # Executing the appropriate command
   function = exe_cmd[args.cmd].function
   _parser = exe_cmd[args.cmd].parser
   
   function(args, _parser)
   
if __name__ == '__main__':
   main()