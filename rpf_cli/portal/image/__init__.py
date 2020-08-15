from portal.image.service import download_image, upload_image
from clilogger import initiate_cli_logger
import os
import time
import json

def register_image_parser(subparsers):
   image_parser = subparsers.add_parser('image', help='Used to download and upload images')
   image_parser.add_argument('url', help='http url to upload/download the image')
   
   # this argument gets the link of the image for the specified roll from the server ( not the thumbnail link )
   image_parser.add_argument('--roll', metavar='ROLL', help='gets the image of the specified roll')
   
   image_subparsers = image_parser.add_subparsers(dest='imgcmd', help='image sub-commands')
   
   # image download subparser
   image_download_subparser = image_subparsers.add_parser('download', help='scrape images from a url')
   
   # mutually exclusive argument for download subparser
   image_download_subparser_group1 = image_download_subparser.add_mutually_exclusive_group(required=True)
   image_download_subparser_group1.add_argument('-g', '--get', metavar='[id]', help='gets the image named by specified id')
   image_download_subparser_group1.add_argument('-r', '--range', metavar='[start-end]', help='download and save image in range [start-end]')
   
   # image upload subparser
   image_upload_subparser = image_subparsers.add_parser('upload', help='upload images to server')
   
   # mutually exclusive argument for upload subparser
   image_upload_subparser_group2 = image_upload_subparser.add_mutually_exclusive_group(required=True)   
   image_upload_subparser_group2.add_argument('-p', '--put', metavar='[FILE...]', action='append', help='upload image')
   image_upload_subparser_group2.add_argument('-d', '--dir', help='directory\'s images to upload')
   
   return image_parser


def execute_image_cmd(args, log_parser):
      
   log = initiate_cli_logger('image')
   
   # download command is called
   if args.imgcmd == 'download':
            
      # get option used ( a single image download )
      if args.get:
         start = int(args.get)
         end = start
         image_list = range(start, end+1)
         
      # range option used ( range of images download )
      elif args.range:
         start, end = map(int, args.range.split('-'))
         image_list = range(start, end+1)
            
      # download image here
      for image_id in image_list:
         download_image(image_id, args.url, log)

            
   # upload command is called
   elif args.imgcmd == 'upload':
      
      # get option used ( a single image upload )
      if args.put:
         image_list = args.put
         
      # directory option used ( upload images from a directory )
      elif args.dir:
         image_list = [ os.path.join(args.dir, file) for file in os.listdir(args.dir) ]
      
      for image_path in image_list:
         upload_image(image_path, args.url, log)
   
   # TODO: fetch roll from the website
   elif args.roll:
      print("Getting roll "+args.roll)