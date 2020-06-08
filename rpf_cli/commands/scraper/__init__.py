from argparse import FileType
import commands.scraper.scrape_all_option as scrape_all_option, commands.scraper.file_option as file_option, \
      commands.scraper.range_option as range_option, commands.scraper.roll_option as roll_option

def register_scraper_parser(subparsers):
   # arguments and options to handle scraper command
   scraper_parser = subparsers.add_parser('scraper', help='Used to scrape the student data')
   scraper_arg_grp1 = scraper_parser.add_mutually_exclusive_group()
   scraper_arg_grp1.add_argument('-a', '--scrape-all', action='store_true', help='download the latest semester of all the branches')
   scraper_arg_grp1.add_argument('-r', '--roll', metavar='[ROLL ...]', help='list of rolls to download', action='append')
   scraper_arg_grp1.add_argument('-f', '--file', type=FileType('r'), help='read file to get rolls and semesters')
   scraper_arg_grp1.add_argument('-R', '--range', metavar='start-end', help='download a range of rolls')
   
   scraper_arg_grp2 = scraper_parser.add_mutually_exclusive_group()
   scraper_arg_grp2.add_argument('-s', '--semester', metavar='[SEMESTER ...]', help='list of semesters to download', action='append')
   scraper_arg_grp2.add_argument('-o', '--semester-options', action='store_true', help='get the available semesters for the given rolls')
   
   scraper_parser.add_argument('-n', '--no-save', action='store_true', help='do not save the result in a file')

def execute_scrape_cmd(args):
   
   if args.scrape_all:
      scrape_all_option.execute()
      
   elif args.roll:
      roll_option.execute(args.roll, args.semester, args.no_save)
   
   elif args.file:
      file_option.execute(args.file)
   
   elif args.range:
      range_option.execute(args.range, args.semester, args.no_save)