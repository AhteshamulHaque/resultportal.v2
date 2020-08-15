from portal.pdf.helpers import download_pdf, upload_pdf
import os

def register_pdf_parser(subparsers):
   # TODO: incomplete pdf parser. pdf download here means download from the `GDRIVE`
   pdf_parser = subparsers.add_parser('pdf', help='Used to download and upload pdfs')
   pdf_parser.add_argument('url', help='http url to upload/download the pdf')
   
   pdf_subparsers = pdf_parser.add_subparsers(dest='pdfcmd', help='pdf sub-commands', required=True)
   
   # pdf download subparser and two mutually exclusive arguments
   pdf_download_subparser = pdf_subparsers.add_parser('download', help='scrape pdfs from a url')
   
   # mutually exclusive argument for download subparser
   pdf_download_subparser_group1 = pdf_download_subparser.add_mutually_exclusive_group(required=True)
   pdf_download_subparser_group1.add_argument('-R', '--roll', metavar='[roll]', help='gets the pdf of the specified roll')
   pdf_download_subparser_group1.add_argument('-r', '--range', metavar='[start-end]', help='download and save pdf in range[start-end]')
   
   pdf_download_subparser.add_argument('-s', '--semester', help='specifies the [semester] for pdf fetch', required=True)
   # pdf upload subparser and two mutually exclusive arguments
   pdf_upload_subparser = pdf_subparsers.add_parser('upload', help='upload pdfs to servers')
   
   # mutually exclusive argument forupload subparser
   pdf_upload_subparser_group2 = pdf_upload_subparser.add_mutually_exclusive_group(required=True)   
   pdf_upload_subparser_group2.add_argument('-p', '--put', metavar='[FILE...]', help='upload pdfs', nargs='+')
   pdf_upload_subparser_group2.add_argument('-d', '--upload-dir', help='directory\'s pdfs to upload')
   
   return pdf_parser

def execute_pdf_cmd(args):
      # download command is called
   if args.pdfcmd == 'download':
      # get option used
      if args.get:
         try:
            download_pdf(args.get, args.url)
         except Exception as err:
            print(err.__class__.__name__, err)
            
      # range option used
      else:
         start, end = map(int, args.range.split('-'))
         
         for img_id in range(start, end+1):
            try:
               download_pdf(img_id, args.url)
            except Exception as err:
               print(err.__class__.__name__, err)
               
   # upload command is called
   else:
      # put option used
      if args.put:
         for filename in args.put:
            try:
               upload_pdf(filename, args.url)
            except Exception as err:
               print(err.__class__.__name__, err)
      # upload-dir options used
      else:
         filelist = os.listdir(args.upload_dir)
         
         for file in filelist:
            upload_pdf( os.path.join(args.upload_dir, file), args.url)