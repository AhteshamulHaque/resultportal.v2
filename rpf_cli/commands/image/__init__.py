from commands.image.helpers import ImageDownloaderUploader
import os, time, json

def register_image_parser(subparsers):
   image_parser = subparsers.add_parser('image', help='Used to download and upload images')
   
   # this argument gets the link of the image for the specified roll from the server ( not the thumbnail link )
   image_parser.add_argument('--roll', metavar='ROLL', help='gets the image of the specified roll')
   
   image_subparsers = image_parser.add_subparsers(dest='imgcmd', help='image sub-commands')
   
   # image download subparser
   image_download_subparser = image_subparsers.add_parser('download', help='scrape images from a url')
   image_download_subparser.add_argument('url', help='url from where images are to be downloaded')
   
   # mutually exclusive argument for download subparser
   image_download_subparser_group1 = image_download_subparser.add_mutually_exclusive_group(required=True)
   image_download_subparser_group1.add_argument('-g', '--get', metavar='[id]', help='gets the image named by specified id')
   image_download_subparser_group1.add_argument('-r', '--range', metavar='[start-end]', help='download and save image in range[start-end]')
   image_download_subparser_group1.add_argument('-d', '--download-from-log-file', action='store_true', help='download images that are found in log file')
   
   # image upload subparser
   image_upload_subparser = image_subparsers.add_parser('upload', help='upload images to servers')
   image_upload_subparser.add_argument('url', help='http url to save the image')
   
   # mutually exclusive argument for upload subparser
   image_upload_subparser_group2 = image_upload_subparser.add_mutually_exclusive_group(required=True)   
   image_upload_subparser_group2.add_argument('-p', '--put', metavar='[FILE...]', action='append', help='upload image')
   image_upload_subparser_group2.add_argument('-d', '--dir', help='directory\'s images to upload', default='images')
   image_download_subparser_group1.add_argument('-u', '--upload-from-log-file', action='store_true', help='upload images that are found in log file')


def execute_image_cmd(args):
      
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
      
      # file option used ( download using log file )
      else:
         image_list = []
         
         with open('logs/images.failed.log', 'r') as fp:
            
            for line in fp:
               json_data = json.loads(line)
               if json_data['type'] == 'download':
                  image_list.append( json_data['img_info'] )
            
      # download image here
      idu = ImageDownloaderUploader()
      idu.download_upload_with_progress(image_list, args.url, args.imgcmd)   

            
   # upload command is called
   elif args.imgcmd == 'upload':
      
      # get option used ( a single image download )
      if args.put:
         image_list = args.put
         
      # range option used ( range of images download )
      elif args.dir:
         image_list = [ os.path.join(args.dir, file) for file in os.listdir(args.dir) ]
      
      # file option used ( download using log file )
      else:
         image_list = []
         
         with open('logs/images.failed.log', 'r') as fp:
            
            for line in fp:
               json_data = json.loads(line)
               if json_data['type'] == 'upload':
                  image_list.append( json_data['img_info'] )
            
      # upload image here
      idu = ImageDownloaderUploader()
      idu.download_upload_with_progress(image_list, args.url, args.imgcmd)
   
   # TODO: fetch roll from the website
   elif args.roll:
      print("Getting roll "+args.roll)