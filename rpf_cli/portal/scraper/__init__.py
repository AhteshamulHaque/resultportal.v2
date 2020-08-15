from argparse import FileType
from portal.scraper.service import valid_regno, valid_range, get_semesters
import portal.scraper.all_option as all_option, portal.scraper.file_option as file_option, \
      portal.scraper.range_option as range_option, portal.scraper.roll_option as roll_option
from clilogger import initiate_cli_logger

def register_scraper_parser(subparsers):
   # arguments and options to handle scraper command
   scraper_parser = subparsers.add_parser('scraper', help='Used to scrape the student data')
   scraper_parser.add_argument('-u', '--url', default='http://122.252.250.250/StudentPortal/Default.aspx', help='Url to scrape result from')
   scraper_parser.add_argument('-p', '--pdf-url', default='http://122.252.250.250/StudentPortal/commanreport.aspx?pagetitle=gradecarde&path=crptNewGradecard.rpt&param=@P_IDNO={},@P_SEMESTERNO={},@P_COLLEGE_CODE=11', help='Url to scrape pdf from')
   scraper_parser.add_argument('-s', '--semester', metavar='[SEMESTER ...]', help='list of semesters to download', action='append')
   scraper_parser.add_argument('-S', '--start-year', help='Start year for scraping')
   scraper_parser.add_argument('-E', '--end-year', help='End year for scraping')
   scraper_parser.add_argument('--stdout', action='store_true', help='print result on standard output')
   scraper_parser.add_argument('-o', '--semester-options', help='get the available semesters for the roll')
   
   scraper_arg_grp = scraper_parser.add_mutually_exclusive_group()
   scraper_arg_grp.add_argument('-a', '--all', action='store_true', help='download the latest semester result of all branch')
   scraper_arg_grp.add_argument('-r', '--roll', metavar='[ROLL ...]', type=valid_regno, help='download result of a roll', action='append')
   scraper_arg_grp.add_argument('-f', '--file', type=FileType('r'), help='read file to get rolls and semesters')
   scraper_arg_grp.add_argument('-R', '--range', metavar='start-end', type=valid_range, help='download result for a range of rolls')
   return scraper_parser
   
def execute_scrape_cmd(args, scraper_parser):
   
   if args.all:
      if not args.start_year or not args.end_year:
         scraper_parser.error('the following arguments are required: -S/--start-year and -E/--end-year')
         
      all_option.execute(args)
      
   elif args.roll:
      roll_log = initiate_cli_logger('scraper:roll')
      pdf_log = initiate_cli_logger('scraper:pdf')
      roll_log.warning('All downloaded results are saved to result.json')
      roll_option.execute(args, roll_log, pdf_log)
   
   elif args.file:
      file_option.execute(args)
   
   elif args.range:
      range_log = initiate_cli_logger('scraper:range')
      pdf_log = initiate_cli_logger('scraper:pdf')
      range_log.warning('All downloaded results are saved to result.json')
      range_option.execute(args, range_log, pdf_log)
   
   elif args.semester_options:
      print('Available semesters:', get_semesters(args.semester_options, args.url))