import requests
import re, os

PDF_DIR = 'pdfs'

def download_pdf(pdf_id, url):
   resp = requests.get(url.format(pdf_id))
   
   resp.raise_for_status()
   # image extension from content-type using regex for jpeg, png, jpg files
   # EXPECTING ONLY pdf file
   pdf_ext = re.match(r'^application/pdf$', resp.headers.get('content-type', 'unknown')).group(1)
   
   #TODO: add progress bar download support
   if not os.path.exists(PDF_DIR):
      os.makedirs(PDF_DIR)
   
   # save the image with proper extension
   open( os.path.join(PDF_DIR, pdf_id, '.'+pdf_ext), 'wb').write( resp.read() )
   

def upload_pdf(pdf_path, url):
   
   with open(pdf_path, 'rb') as fp:
      resp = requests.post(url, {'images': fp})
      resp.raise_for_status()