# for testing purpose
import urllib.parse
import requests, re, os, json, traceback, time
from yaspin import yaspin
from colorama import init, Fore, Back, Style
from string import Template
from clilogger import initiate_cli_logger

def download_image(image_id, url, log):
   
   try:
      url = urllib.parse.urljoin(url, str(image_id)+'.jpg')
      
      log.debug('Requesting url=%s', url)
      
      with requests.get( url, stream=True ) as resp:
         resp.raise_for_status()
         
         # expecting only `jpeg` and `png` file
         extension = re.match(r'image/([a-z]+)', resp.headers.get('content-type', 'image/jpeg')).group(1)
         
         # create image directory if not exists
         if not os.path.exists('images'):
            os.makedirs('images')
            
         filepath = os.path.join('images', image_id+'.'+extension)
         
         # save the image to the directory
         with open( filepath , 'wb') as fp:
            for chunk in resp.iter_content(chunk_size=1024):
                  fp.write(chunk)
      log.warning('Downloaded image with id=%s', image_id)
      
   except:
      log.error('Failed to download image with id=%s', image_id)

   
def upload_image(img_path, url, log):
   
   log.debug('Trying to upload %s', img_path)
   
   try:
      with open(img_path, 'rb') as fp:
         resp = requests.post(url, files={'image': fp})
         resp.raise_for_status()
      log.warning('Uploaded image %s', img_path)
      
   except:
      log.error('Failed to upload %s', img_path)
      
   